"""Message handlers for CoinFlow bot."""

from telegram import Update
from telegram.ext import ContextTypes
from ..localization import get_text
from ..utils.logger import setup_logger

logger = setup_logger('messages')


class MessageHandlers:
    """Handlers for text messages."""
    
    def __init__(self, bot):
        self.bot = bot
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages."""
        user_id = update.effective_user.id
        text = update.message.text
        
        user = self.bot.db.get_or_create_user(user_id)
        
        # Language selection
        if 'English' in text:
            self.bot.db.update_user(user_id, lang='en')
            user = self.bot.db.get_user(user_id)
            await update.message.reply_text(
                get_text('en', 'language_set'),
                reply_markup=self.bot.get_main_menu_keyboard('en'),
                parse_mode='Markdown'
            )
            return
        elif 'Русский' in text:
            self.bot.db.update_user(user_id, lang='ru')
            user = self.bot.db.get_user(user_id)
            await update.message.reply_text(
                get_text('ru', 'language_set'),
                reply_markup=self.bot.get_main_menu_keyboard('ru'),
                parse_mode='Markdown'
            )
            return
        
        # Main menu items
        if text == get_text(user.lang, 'quick_convert'):
            await self.bot.callback_handlers.start_conversion(update, user, context)
        elif text == get_text(user.lang, 'rate_charts'):
            await self.bot.callback_handlers.start_chart_selection(update, user, context)
        elif text == get_text(user.lang, 'rate_prediction'):
            await self.bot.callback_handlers.start_prediction_selection(update, user, context)
        elif text == get_text(user.lang, 'compare_rates'):
            await self.bot.callback_handlers.start_comparison_selection(update, user, context)
        elif text == get_text(user.lang, 'calculator'):
            await update.message.reply_text(
                get_text(user.lang, 'calculator_mode'),
                parse_mode='Markdown'
            )
            context.user_data['state'] = 'calculator'
        elif text == get_text(user.lang, 'stocks'):
            await self.bot.stocks_handler.show_stocks_menu(update, context)
        elif text == get_text(user.lang, 'cs2_skins'):
            await self.bot.cs2_handler.show_cs2_menu(update, context)
        elif text == get_text(user.lang, 'portfolio'):
            await self.bot.portfolio_handler.show_portfolio_menu(update, context)
        elif text == get_text(user.lang, 'export'):
            await self.bot.export_handler.show_export_menu(update, context)
        elif text == get_text(user.lang, 'notifications'):
            await self.show_alerts(update, context)
        elif text == get_text(user.lang, 'favorites'):
            await self.show_favorites(update, context)
        elif text == get_text(user.lang, 'history'):
            await self.show_history(update, context)
        elif text == get_text(user.lang, 'stats_btn'):
            await self.show_stats(update, context)
        elif text == get_text(user.lang, 'settings'):
            await self.show_settings(update, context)
        elif text == get_text(user.lang, 'about_btn'):
            await update.message.reply_text(
                get_text(user.lang, 'about_text'),
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        elif context.user_data.get('state') == 'calculator':
            # Calculator mode
            result = self.bot.calculator.calculate(text, user_id)
            if result:
                await update.message.reply_text(get_text(user.lang, 'calc_result', result=result))
                self.bot.metrics.log_calculation(user_id)
            else:
                await update.message.reply_text(get_text(user.lang, 'error', msg='Invalid expression'))
        elif context.user_data.get('state') == 'enter_amount':
            # Amount entry for conversion
            try:
                amount = float(text.replace(',', '.'))
                await self.bot.callback_handlers.perform_conversion(update, context, amount, user)
            except:
                await update.message.reply_text(get_text(user.lang, 'invalid_amount'))
    
    async def show_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show conversion history."""
        user_id = update.effective_user.id
        user = self.bot.db.get_user(user_id)
        
        history = self.bot.db.get_conversion_history(user_id, limit=10)
        
        if not history:
            await update.message.reply_text(get_text(user.lang, 'history_empty'))
            return
        
        history_text = ""
        for h in history:
            history_text += f"• {h.amount} {h.from_currency} → {h.result:.2f} {h.to_currency}\n"
            history_text += f"  _{h.timestamp.strftime('%d.%m.%Y %H:%M')}_\n\n"
        
        await update.message.reply_text(
            get_text(user.lang, 'history_list', history=history_text),
            parse_mode='Markdown'
        )
    
    async def show_favorites(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show favorite currencies."""
        user_id = update.effective_user.id
        user = self.bot.db.get_user(user_id)
        
        favorites = self.bot.db.get_favorites(user_id)
        
        if not favorites:
            await update.message.reply_text(get_text(user.lang, 'favorites_empty'))
            return
        
        favorites_text = ", ".join(favorites)
        await update.message.reply_text(
            get_text(user.lang, 'favorites_list', favorites=favorites_text),
            parse_mode='Markdown'
        )
    
    async def show_alerts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show active alerts."""
        user_id = update.effective_user.id
        user = self.bot.db.get_user(user_id)
        
        alerts = self.bot.alert_manager.get_alerts(user_id)
        
        if not alerts:
            await update.message.reply_text(get_text(user.lang, 'no_alerts'))
            return
        
        alert_text = '\n'.join([
            f"{i+1}. {a['pair']} {a['condition']} ${a['target']}"
            for i, a in enumerate(alerts)
        ])
        
        await update.message.reply_text(
            get_text(user.lang, 'alerts_list', alerts=alert_text),
            parse_mode='Markdown'
        )
    
    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user statistics and crypto market data."""
        user_id = update.effective_user.id
        user = self.bot.db.get_user(user_id)
        
        # Get user stats
        stats = self.bot.db.get_user_stats(user_id)
        popular_pairs = self.bot.db.get_popular_pairs(user_id, days=30, limit=5)
        
        stats_text = (
            f"📊 **Your Statistics**\n\n"
            f"💱 Total conversions: {stats['total_conversions']}\n"
            f"🔔 Active alerts: {stats['total_alerts']}\n"
            f"⭐ Favorite currencies: {stats['favorites_count']}\n"
        )
        
        if popular_pairs:
            stats_text += "\n**Most used pairs (last 30 days):**\n"
            for from_curr, to_curr, count in popular_pairs:
                stats_text += f"• {from_curr} → {to_curr}: {count}x\n"
        
        # Add crypto market data
        stats_text += "\n\n📈 **Live Crypto Prices:**\n"
        
        # Fetch prices for popular cryptos
        popular_cryptos = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP']
        crypto_data = []
        
        for crypto in popular_cryptos:
            try:
                price = self.bot.converter.get_crypto_rate_aggregated(crypto, 'USDT', user_id)
                if price and price > 0:
                    crypto_data.append(f"• **{crypto}:** ${price:,.2f}")
            except Exception as e:
                logger.debug(f"Error fetching price for {crypto}: {e}")
        
        if crypto_data:
            stats_text += "\n".join(crypto_data)
            stats_text += "\n\n_Real-time prices from major exchanges_"
        else:
            stats_text += "_Unable to fetch crypto prices at the moment_\n"
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def show_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show settings menu with interactive options."""
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        
        user_id = update.effective_user.id
        user = self.bot.db.get_user(user_id)
        
        # Get user preferences
        current_lang = user.lang if user else 'en'
        lang_emoji = '🇬🇧' if current_lang == 'en' else '🇷🇺'
        
        # Get chart theme
        current_theme = user.chart_theme if user and hasattr(user, 'chart_theme') else 'light'
        theme_emoji = '☀️' if current_theme == 'light' else '🌙' if current_theme == 'dark' else '🔄'
        
        # Get alerts count
        alerts = self.bot.alert_manager.get_alerts(user_id)
        alerts_count = len(alerts) if alerts else 0
        
        # Create settings menu
        settings_text = (
            f"⚙️ **Settings & Preferences**\n\n"
            f"👤 **User ID:** `{user_id}`\n"
            f"🌍 **Language:** {lang_emoji} {current_lang.upper()}\n"
            f"🎨 **Chart Theme:** {theme_emoji} {current_theme.title()}\n"
            f"🔔 **Active Alerts:** {alerts_count}\n\n"
            f"**Available Options:**\n"
            f"• Change language\n"
            f"• Change chart theme\n"
            f"• Manage alerts\n"
            f"• View bot statistics\n\n"
            f"Select an option below:"
        )
        
        # Create inline keyboard
        keyboard = [
            [
                InlineKeyboardButton('🇬🇧 English', callback_data='settings_lang_en'),
                InlineKeyboardButton('🇷🇺 Русский', callback_data='settings_lang_ru')
            ],
            [
                InlineKeyboardButton('🎨 Chart Theme', callback_data='settings_theme')
            ],
            [
                InlineKeyboardButton('🔔 Manage Alerts', callback_data='settings_alerts'),
                InlineKeyboardButton('📊 Bot Stats', callback_data='settings_stats')
            ],
            [
                InlineKeyboardButton('ℹ️ About', callback_data='settings_about'),
                InlineKeyboardButton('◀️ Back to Menu', callback_data='back_main')
            ]
        ]
        
        await update.message.reply_text(
            settings_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
