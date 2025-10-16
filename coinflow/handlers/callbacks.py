"""Callback query handlers for CoinFlow bot."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime
from ..localization import get_text
from ..utils.logger import setup_logger

logger = setup_logger('callbacks')


class CallbackHandlers:
    """Handlers for inline keyboard callbacks."""
    
    def __init__(self, bot):
        self.bot = bot
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main callback query handler."""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        data = query.data
        
        user = self.bot.db.get_or_create_user(user_id)
        
        # Category selection
        if data.startswith('cat_'):
            category = data.split('_')[1]
            keyboard = self.bot.get_currency_selection_keyboard(user.lang, category)
            await query.edit_message_reply_markup(reply_markup=keyboard)
        
        # Currency selection
        elif data.startswith('curr_'):
            currency = data.split('_')[1]
            await self.handle_currency_selection(query, context, user, currency)
        
        # Amount selection
        elif data.startswith('amt_'):
            if data == 'amt_custom':
                context.user_data['state'] = 'enter_amount'
                await query.edit_message_text(get_text(user.lang, 'enter_amount'), parse_mode='Markdown')
            else:
                amount = float(data.split('_')[1])
                await self.perform_conversion_callback(query, context, amount, user)
        
        # Favorite toggle
        elif data.startswith('fav_'):
            currency = data.split('_')[1]
            await self.toggle_favorite(query, user, currency)
        
        # Period selection for charts
        elif data.startswith('period_'):
            period = int(data.split('_')[1])
            pair = context.user_data.get('chart_pair', 'BTC')
            await self.generate_chart(query, user, pair, period)
        
        # Back to main
        elif data == 'back_main':
            await query.message.reply_text(
                get_text(user.lang, 'main_menu'),
                reply_markup=self.bot.get_main_menu_keyboard(user.lang),
                parse_mode='Markdown'
            )
    
    async def handle_currency_selection(self, query, context, user, currency):
        """Handle currency selection based on state."""
        state = context.user_data.get('state', 'select_from')
        
        if state == 'select_from':
            context.user_data['from_currency'] = currency
            context.user_data['state'] = 'select_to'
            await query.edit_message_text(
                get_text(user.lang, 'select_to_currency') + f" (From: {currency})",
                reply_markup=self.bot.get_currency_selection_keyboard(user.lang, 'popular'),
                parse_mode='Markdown'
            )
        elif state == 'select_to':
            context.user_data['to_currency'] = currency
            from_curr = context.user_data.get('from_currency', 'BTC')
            context.user_data['state'] = 'select_amount'
            await query.edit_message_text(
                get_text(user.lang, 'enter_amount') + f" ({from_curr} → {currency})",
                reply_markup=self.bot.get_amount_presets_keyboard(user.lang),
                parse_mode='Markdown'
            )
        elif state == 'select_chart':
            context.user_data['chart_pair'] = currency
            await self.show_period_selection(query, user, currency)
        elif state == 'select_prediction':
            await self.generate_prediction(query, user, currency)
        elif state == 'select_compare':
            await self.compare_rates(query, user, currency)
    
    async def start_conversion(self, update, user, context):
        """Start conversion flow."""
        context.user_data['state'] = 'select_from'
        await update.message.reply_text(
            get_text(user.lang, 'select_from_currency'),
            reply_markup=self.bot.get_currency_selection_keyboard(user.lang, 'popular'),
            parse_mode='Markdown'
        )
    
    async def start_chart_selection(self, update, user, context):
        """Start chart selection flow."""
        context.user_data['state'] = 'select_chart'
        await update.message.reply_text(
            get_text(user.lang, 'select_currency_chart'),
            reply_markup=self.bot.get_currency_selection_keyboard(user.lang, 'crypto'),
            parse_mode='Markdown'
        )
    
    async def start_prediction_selection(self, update, user, context):
        """Start prediction selection flow."""
        context.user_data['state'] = 'select_prediction'
        await update.message.reply_text(
            get_text(user.lang, 'select_currency_prediction'),
            reply_markup=self.bot.get_currency_selection_keyboard(user.lang, 'crypto'),
            parse_mode='Markdown'
        )
    
    async def start_comparison_selection(self, update, user, context):
        """Start comparison selection flow."""
        context.user_data['state'] = 'select_compare'
        await update.message.reply_text(
            get_text(user.lang, 'select_currency_compare'),
            reply_markup=self.bot.get_currency_selection_keyboard(user.lang, 'crypto'),
            parse_mode='Markdown'
        )
    
    async def perform_conversion(self, update, context, amount, user):
        """Perform currency conversion."""
        from_curr = context.user_data.get('from_currency')
        to_curr = context.user_data.get('to_currency')
        
        # Validate currencies
        if not from_curr or not to_curr:
            await update.message.reply_text(
                get_text(user.lang, 'error', msg='Please select currencies first'),
                parse_mode='Markdown',
                reply_markup=self.bot.get_main_menu_keyboard(user.lang)
            )
            context.user_data.clear()
            return
        
        result = self.bot.converter.convert(amount, from_curr, to_curr, user.telegram_id)
        
        if result:
            rate = self.bot.converter.get_rate(from_curr, to_curr, user.telegram_id)
            
            # Save to history
            self.bot.db.add_conversion(user.telegram_id, from_curr, to_curr, amount, result, rate)
            self.bot.metrics.log_conversion(user.telegram_id)
            
            await update.message.reply_text(
                get_text(user.lang, 'conversion_result',
                        amount=amount, from_curr=from_curr,
                        result=f"{result:.2f}", to_curr=to_curr,
                        rate=f"{rate:.6f}",
                        time=datetime.now().strftime('%H:%M')),
                parse_mode='Markdown',
                reply_markup=self.bot.get_main_menu_keyboard(user.lang)
            )
        else:
            await update.message.reply_text(
                get_text(user.lang, 'rate_unavailable'),
                reply_markup=self.bot.get_main_menu_keyboard(user.lang)
            )
        
        context.user_data.clear()
    
    async def perform_conversion_callback(self, query, context, amount, user):
        """Perform conversion from callback."""
        from_curr = context.user_data.get('from_currency')
        to_curr = context.user_data.get('to_currency')
        
        # Validate currencies
        if not from_curr or not to_curr:
            await query.edit_message_text(
                get_text(user.lang, 'error', msg='Please select currencies first'),
                parse_mode='Markdown'
            )
            context.user_data.clear()
            return
        
        result = self.bot.converter.convert(amount, from_curr, to_curr, user.telegram_id)
        
        if result:
            rate = self.bot.converter.get_rate(from_curr, to_curr, user.telegram_id)
            
            # Save to history
            self.bot.db.add_conversion(user.telegram_id, from_curr, to_curr, amount, result, rate)
            self.bot.metrics.log_conversion(user.telegram_id)
            
            await query.edit_message_text(
                get_text(user.lang, 'conversion_result',
                        amount=amount, from_curr=from_curr,
                        result=f"{result:.2f}", to_curr=to_curr,
                        rate=f"{rate:.6f}",
                        time=datetime.now().strftime('%H:%M')),
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(get_text(user.lang, 'rate_unavailable'))
        
        context.user_data.clear()
    
    async def show_period_selection(self, query, user, currency):
        """Show period selection for charts."""
        keyboard = [
            [InlineKeyboardButton('7 days', callback_data='period_7'),
             InlineKeyboardButton('30 days', callback_data='period_30')],
            [InlineKeyboardButton('90 days', callback_data='period_90'),
             InlineKeyboardButton('1 year', callback_data='period_365')],
            [InlineKeyboardButton(get_text(user.lang, 'back'), callback_data='back_main')]
        ]
        await query.edit_message_text(
            f"📊 **Chart for 1 {currency}**\n\nSelect time period:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def generate_chart(self, query, user, pair, period=30):
        """Generate chart for pair (price of 1 unit)."""
        await query.edit_message_text(f"📊 Generating chart for **1 {pair}**...\n\nPlease wait...", parse_mode='Markdown')
        
        chart_data, stats = self.bot.chart_generator.generate_chart(f"{pair}-USD", period)
        
        if chart_data and stats:
            # Format stats for 1 unit
            caption = (
                f"📊 **{pair}/USD Chart** ({period} days)\n\n"
                f"💰 Current price: **${stats.get('current', 0):.2f}**\n"
                f"📈 High: ${stats.get('high', 0):.2f}\n"
                f"📉 Low: ${stats.get('low', 0):.2f}\n"
                f"📊 Average: ${stats.get('avg', 0):.2f}\n\n"
                f"_Price shown for 1 {pair}_"
            )
            await query.message.reply_photo(
                photo=chart_data,
                caption=caption,
                parse_mode='Markdown'
            )
            self.bot.metrics.log_chart(user.telegram_id)
        else:
            await query.edit_message_text('❌ Chart generation failed. Please try again.', parse_mode='Markdown')
    
    async def generate_prediction(self, query, user, pair):
        """Generate prediction for pair (price of 1 unit)."""
        await query.edit_message_text(f"🔮 Generating AI forecast for **1 {pair}**...\n\nAnalyzing 90 days of data...", parse_mode='Markdown')
        
        model = user.prediction_model or 'arima'
        pred_data, stats = self.bot.prediction_generator.generate_prediction(f"{pair}-USD", model, 90)
        
        if pred_data and stats:
            # Format prediction for 1 unit
            caption = (
                f"🔮 **{pair}/USD Forecast** (7 days ahead)\n\n"
                f"📊 Model: {model.upper()}\n"
                f"💰 Current: **${stats.get('current', 0):.2f}**\n"
                f"🎯 Predicted: ${stats.get('predicted', 0):.2f}\n"
                f"📈 Change: {stats.get('change', 0):+.2f}%\n\n"
                f"_Forecast for 1 {pair}_\n"
                f"⚠️ Not financial advice"
            )
            await query.message.reply_photo(
                photo=pred_data,
                caption=caption,
                parse_mode='Markdown'
            )
            self.bot.metrics.log_prediction(user.telegram_id)
        else:
            await query.edit_message_text('❌ Forecast generation failed. Please try again.', parse_mode='Markdown')
    
    async def compare_rates(self, query, user, symbol):
        """Compare rates across exchanges (for 1 unit)."""
        await query.edit_message_text(f"⚖️ Comparing prices for **1 {symbol}**...\n\nChecking 5+ exchanges...", parse_mode='Markdown')
        
        rates = self.bot.converter.get_all_crypto_rates(symbol, 'USDT', user.telegram_id)
        
        if rates:
            rate_text = '\n'.join([f"• **{ex}:** ${rate:.2f}" for ex, rate in rates])
            prices = [r[1] for r in rates]
            avg = sum(prices) / len(prices)
            high = max(prices)
            low = min(prices)
            high_ex = [ex for ex, rate in rates if rate == high][0]
            low_ex = [ex for ex, rate in rates if rate == low][0]
            spread = ((high - low) / avg) * 100
            
            result_text = (
                f"⚖️ **{symbol}/USDT Price Comparison**\n\n"
                f"{rate_text}\n\n"
                f"📊 **Statistics for 1 {symbol}:**\n"
                f"💰 Average: **${avg:.2f}**\n"
                f"📈 Highest: ${high:.2f} ({high_ex})\n"
                f"📉 Lowest: ${low:.2f} ({low_ex})\n"
                f"📊 Spread: {spread:.2f}%\n\n"
                f"_Best price: {low_ex}_"
            )
            
            await query.edit_message_text(result_text, parse_mode='Markdown')
            self.bot.metrics.log_comparison(user.telegram_id)
        else:
            await query.edit_message_text('❌ No data available. Please try again.', parse_mode='Markdown')
    
    async def toggle_favorite(self, query, user, currency):
        """Toggle currency in favorites."""
        if self.bot.db.is_favorite(user.telegram_id, currency):
            self.bot.db.remove_favorite(user.telegram_id, currency)
            await query.answer(get_text(user.lang, 'favorite_removed', currency=currency))
        else:
            self.bot.db.add_favorite(user.telegram_id, currency)
            await query.answer(get_text(user.lang, 'favorite_added', currency=currency))
