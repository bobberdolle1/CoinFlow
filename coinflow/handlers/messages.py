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
            await self.bot.callback_handlers.start_conversion(update, user)
        elif text == get_text(user.lang, 'rate_charts'):
            await self.bot.callback_handlers.start_chart_selection(update, user)
        elif text == get_text(user.lang, 'rate_prediction'):
            await self.bot.callback_handlers.start_prediction_selection(update, user)
        elif text == get_text(user.lang, 'compare_rates'):
            await self.bot.callback_handlers.start_comparison_selection(update, user)
        elif text == get_text(user.lang, 'calculator'):
            await update.message.reply_text(
                get_text(user.lang, 'calculator_mode'),
                parse_mode='Markdown'
            )
            context.user_data['state'] = 'calculator'
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
        """Show user statistics."""
        user_id = update.effective_user.id
        user = self.bot.db.get_user(user_id)
        
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
    
    async def show_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show settings menu."""
        user_id = update.effective_user.id
        user = self.bot.db.get_user(user_id)
        
        # Global bot stats
        bot_stats = self.bot.metrics.get_stats_text()
        
        await update.message.reply_text(
            get_text(user.lang, 'settings_menu') + "\n\n" + bot_stats,
            parse_mode='Markdown'
        )
