"""Main bot class for CoinFlow."""

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from apscheduler.schedulers.background import BackgroundScheduler
import re
from .database import DatabaseRepository
from .services import CurrencyConverter, Calculator, ChartGenerator, PredictionGenerator, AlertManager
from .handlers import CommandHandlers, MessageHandlers, CallbackHandlers
from .config import config
from .utils import setup_logger, Metrics
from .localization import get_text

logger = setup_logger('bot', config.LOG_FILE, config.LOG_LEVEL, config.LOG_MAX_BYTES, config.LOG_BACKUP_COUNT)


class CoinFlowBot:
    """Main CoinFlow bot class."""
    
    def __init__(self):
        """Initialize bot with all services."""
        logger.info("Initializing CoinFlow Bot v2.0...")
        
        # Database
        self.db = DatabaseRepository(config.DATABASE_URL)
        logger.info("Database initialized")
        
        # Services
        self.converter = CurrencyConverter(cache_ttl=config.CACHE_TTL_SECONDS)
        self.converter.bot = self  # Circular reference for user settings
        
        self.calculator = Calculator(self.converter)
        self.chart_generator = ChartGenerator(dpi=config.CHART_DPI)
        self.prediction_generator = PredictionGenerator(dpi=config.CHART_DPI)
        self.alert_manager = AlertManager(self.db)
        
        # Metrics
        self.metrics = Metrics()
        
        # Handlers
        self.command_handlers = CommandHandlers(self)
        self.message_handlers = MessageHandlers(self)
        self.callback_handlers = CallbackHandlers(self)
        
        logger.info("All services initialized")
        
        # Currency lists
        self.popular_currencies = ['USD', 'EUR', 'RUB', 'CNY', 'GBP', 'JPY', 'BTC', 'ETH', 'USDT']
        self.fiat_currencies = [
            'USD', 'EUR', 'RUB', 'CNY', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'KRW',
            'INR', 'BRL', 'MXN', 'TRY', 'SEK', 'NOK', 'DKK', 'PLN', 'THB', 'IDR',
            'HUF', 'CZK', 'ILS', 'CLP', 'PHP', 'AED', 'SAR', 'MYR', 'RON', 'SGD'
        ]
        self.crypto_currencies = [
            'BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'DOT', 'MATIC',
            'SHIB', 'AVAX', 'TRX', 'LINK', 'UNI', 'ATOM', 'LTC', 'XLM', 'BCH', 'ALGO',
            'VET', 'FIL', 'HBAR', 'APE', 'NEAR', 'QNT', 'AAVE', 'GRT', 'XTZ', 'SAND'
        ]
    
    def get_main_menu_keyboard(self, lang: str) -> ReplyKeyboardMarkup:
        """Create main menu keyboard."""
        return ReplyKeyboardMarkup([
            [get_text(lang, 'quick_convert')],
            [get_text(lang, 'rate_charts'), get_text(lang, 'rate_prediction')],
            [get_text(lang, 'compare_rates'), get_text(lang, 'calculator')],
            [get_text(lang, 'notifications'), get_text(lang, 'favorites')],
            [get_text(lang, 'history'), get_text(lang, 'stats_btn')],
            [get_text(lang, 'settings'), get_text(lang, 'about_btn')]
        ], resize_keyboard=True)
    
    def get_currency_selection_keyboard(self, lang: str, selection_type: str = 'popular') -> InlineKeyboardMarkup:
        """Create currency selection inline keyboard."""
        keyboard = []
        
        # Category buttons
        keyboard.append([
            InlineKeyboardButton(get_text(lang, 'popular'), callback_data='cat_popular'),
            InlineKeyboardButton(get_text(lang, 'fiat'), callback_data='cat_fiat'),
            InlineKeyboardButton(get_text(lang, 'crypto'), callback_data='cat_crypto')
        ])
        
        # Currency list
        if selection_type == 'popular':
            currencies = self.popular_currencies
        elif selection_type == 'fiat':
            currencies = self.fiat_currencies[:20]
        elif selection_type == 'crypto':
            currencies = self.crypto_currencies[:20]
        else:
            currencies = self.popular_currencies
        
        # 3 currencies per row
        row = []
        for curr in currencies:
            row.append(InlineKeyboardButton(curr, callback_data=f'curr_{curr}'))
            if len(row) == 3:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        
        # Back button
        keyboard.append([InlineKeyboardButton(get_text(lang, 'back'), callback_data='back_main')])
        
        return InlineKeyboardMarkup(keyboard)
    
    def get_amount_presets_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        """Create amount preset keyboard."""
        keyboard = [
            [InlineKeyboardButton('10', callback_data='amt_10'),
             InlineKeyboardButton('50', callback_data='amt_50'),
             InlineKeyboardButton('100', callback_data='amt_100')],
            [InlineKeyboardButton('500', callback_data='amt_500'),
             InlineKeyboardButton('1000', callback_data='amt_1000'),
             InlineKeyboardButton('5000', callback_data='amt_5000')],
            [InlineKeyboardButton('💬 Custom', callback_data='amt_custom'),
             InlineKeyboardButton(get_text(lang, 'back'), callback_data='back_main')]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    async def inline_query(self, update, context):
        """Handle inline queries for quick conversions."""
        query = update.inline_query.query
        
        if not query:
            return
        
        # Parse: "100 USD to EUR"
        match = re.match(r'(\d+\.?\d*)\s*([A-Z]{3})\s*(?:to|in)\s*([A-Z]{3})', query, re.I)
        if match:
            amount, from_curr, to_curr = match.groups()
            amount = float(amount)
            from_curr = from_curr.upper()
            to_curr = to_curr.upper()
            
            result = self.converter.convert(amount, from_curr, to_curr)
            
            if result:
                results = [InlineQueryResultArticle(
                    id='1',
                    title=f'{amount} {from_curr} = {result:.2f} {to_curr}',
                    description=f'Current rate: 1 {from_curr} = {result/amount:.6f} {to_curr}',
                    input_message_content=InputTextMessageContent(
                        f'💱 {amount} {from_curr} = **{result:.2f} {to_curr}**',
                        parse_mode='Markdown'
                    )
                )]
                await update.inline_query.answer(results, cache_time=30)


def check_all_alerts(context, bot: CoinFlowBot):
    """Background task to check all price alerts."""
    try:
        logger.info("Checking price alerts...")
        
        # Get all unique alert pairs
        all_alerts = bot.alert_manager.get_all_alerts()
        pairs_to_check = {}
        
        for user_id, alert in all_alerts:
            pair = alert['pair']
            if pair not in pairs_to_check:
                pairs_to_check[pair] = []
            pairs_to_check[pair].append((user_id, alert))
        
        # Check each pair
        for pair, user_alerts in pairs_to_check.items():
            try:
                # Get current price
                if pair in bot.converter.crypto_symbols:
                    current_price = bot.converter.get_crypto_rate_aggregated(pair, 'USDT', user_alerts[0][0])
                    
                    if current_price:
                        # Check alerts for each user
                        for user_id, alert in user_alerts:
                            triggered = bot.alert_manager.check_alerts(user_id, pair, current_price)
                            
                            # Send notifications
                            for t_alert in triggered:
                                try:
                                    user = bot.db.get_user(user_id)
                                    if user:
                                        context.bot.send_message(
                                            chat_id=user_id,
                                            text=get_text(user.lang, 'alert_triggered',
                                                        pair=t_alert['pair'],
                                                        condition=t_alert['condition'],
                                                        target=t_alert['target'],
                                                        current=current_price),
                                            parse_mode='Markdown'
                                        )
                                        bot.metrics.log_alert(user_id)
                                        logger.info(f"Alert sent to user {user_id} for {pair}")
                                except Exception as e:
                                    logger.error(f"Error sending alert to user {user_id}: {e}")
            except Exception as e:
                logger.error(f"Error checking pair {pair}: {e}")
        
        logger.info("Alert check completed")
    except Exception as e:
        logger.error(f"Alert check error: {e}")


def setup_bot() -> Application:
    """Setup and configure the bot application."""
    # Create bot instance
    bot = CoinFlowBot()
    
    # Create application
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", bot.command_handlers.start))
    app.add_handler(CommandHandler("help", bot.command_handlers.help_command))
    app.add_handler(CommandHandler("stats", bot.command_handlers.stats_command))
    app.add_handler(CommandHandler("history", bot.command_handlers.history_command))
    app.add_handler(CommandHandler("favorites", bot.command_handlers.favorites_command))
    app.add_handler(CommandHandler("cancel", bot.command_handlers.cancel_command))
    
    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.message_handlers.handle_message))
    
    # Add callback query handler
    app.add_handler(CallbackQueryHandler(bot.callback_handlers.handle_callback))
    
    # Add inline query handler
    app.add_handler(InlineQueryHandler(bot.inline_query))
    
    # Setup background scheduler for alerts
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_all_alerts,
        'interval',
        minutes=config.ALERT_CHECK_INTERVAL,
        kwargs={'context': app, 'bot': bot}
    )
    scheduler.start()
    
    logger.info("Bot setup completed")
    
    return app
