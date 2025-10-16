"""Command handlers for CoinFlow bot."""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from ..localization import get_text
from ..utils.logger import setup_logger

logger = setup_logger('commands')


class CommandHandlers:
    """Handlers for bot commands."""
    
    def __init__(self, bot):
        self.bot = bot
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user_id = update.effective_user.id
        user = self.bot.db.get_user(user_id)
        
        if not user:
            # New user - show language selection
            keyboard = ReplyKeyboardMarkup([['English 🇬🇧', 'Русский 🇷🇺']], resize_keyboard=True)
            await update.message.reply_text(
                get_text('en', 'welcome_new'),
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            # Create user with default settings
            self.bot.db.create_user(user_id, lang='en')
            logger.info(f"New user: {user_id}")
        else:
            # Existing user - show main menu
            await update.message.reply_text(
                get_text(user.lang, 'welcome_back'),
                reply_markup=self.bot.get_main_menu_keyboard(user.lang),
                parse_mode='Markdown'
            )
            logger.info(f"User {user_id} started bot")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        user_id = update.effective_user.id
        user = self.bot.db.get_or_create_user(user_id)
        
        help_text = (
            "🆘 *CoinFlow Bot Help*\n\n"
            "*Commands:*\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/stats - Show your statistics\n"
            "/history - View conversion history\n"
            "/favorites - Manage favorites\n"
            "/cancel - Cancel current operation\n\n"
            "*Features:*\n"
            "• Quick currency conversion\n"
            "• Real-time crypto rates\n"
            "• Historical charts\n"
            "• AI price forecasting\n"
            "• Price alerts\n"
            "• Built-in calculator\n"
            "• Favorites & history\n\n"
            "Use the buttons below to navigate!"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command."""
        user_id = update.effective_user.id
        user = self.bot.db.get_or_create_user(user_id)
        
        stats = self.bot.db.get_user_stats(user_id)
        popular_pairs = self.bot.db.get_popular_pairs(user_id, days=30, limit=5)
        
        stats_text = (
            f"📊 *Your Statistics*\n\n"
            f"💱 Total conversions: {stats['total_conversions']}\n"
            f"🔔 Active alerts: {stats['total_alerts']}\n"
            f"⭐ Favorite currencies: {stats['favorites_count']}\n"
        )
        
        if popular_pairs:
            stats_text += "\n*Most used pairs (last 30 days):*\n"
            for from_curr, to_curr, count in popular_pairs:
                stats_text += f"• {from_curr} → {to_curr}: {count}x\n"
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /history command."""
        user_id = update.effective_user.id
        await self.bot.message_handlers.show_history(update, context)
    
    async def favorites_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /favorites command."""
        user_id = update.effective_user.id
        await self.bot.message_handlers.show_favorites(update, context)
    
    async def cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /cancel command."""
        user_id = update.effective_user.id
        user = self.bot.db.get_or_create_user(user_id)
        
        await update.message.reply_text(
            get_text(user.lang, 'main_menu'),
            reply_markup=self.bot.get_main_menu_keyboard(user.lang),
            parse_mode='Markdown'
        )
