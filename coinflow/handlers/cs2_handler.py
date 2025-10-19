"""Handler for CS2 market features."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime
from ..localization import get_text
from ..utils.logger import setup_logger

logger = setup_logger('cs2_handler')


class CS2Handler:
    """Handler for CS2 item market queries."""
    
    def __init__(self, bot):
        self.bot = bot
        self.cs2_service = bot.cs2_service
    
    async def show_cs2_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show main CS2 items menu."""
        user_id = update.effective_user.id
        user = self.bot.db.get_or_create_user(user_id)
        
        keyboard = [
            [InlineKeyboardButton('🔪 ' + get_text(user.lang, 'cs2_knives'), callback_data='cs2_cat_knives')],
            [InlineKeyboardButton('🧤 ' + get_text(user.lang, 'cs2_gloves'), callback_data='cs2_cat_gloves')],
            [InlineKeyboardButton('🔫 ' + get_text(user.lang, 'cs2_rifles'), callback_data='cs2_cat_rifles')],
            [InlineKeyboardButton('🎯 ' + get_text(user.lang, 'cs2_snipers'), callback_data='cs2_cat_snipers')],
            [InlineKeyboardButton('🔫 ' + get_text(user.lang, 'cs2_pistols'), callback_data='cs2_cat_pistols')],
            [InlineKeyboardButton('⚡ ' + get_text(user.lang, 'cs2_smgs'), callback_data='cs2_cat_smgs')],
            [InlineKeyboardButton(get_text(user.lang, 'back'), callback_data='back_main')]
        ]
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                get_text(user.lang, 'cs2_menu'),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                get_text(user.lang, 'cs2_menu'),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
    
    async def show_category_items(self, query, user, category: str):
        """Show items in a specific category."""
        items = self.cs2_service.get_items_by_category(category)
        
        if not items:
            await query.edit_message_text(
                get_text(user.lang, 'cs2_no_items'),
                parse_mode='Markdown'
            )
            return
        
        keyboard = []
        for item_id in items:
            item_info = self.cs2_service.POPULAR_ITEMS[item_id]
            # Shorten name for button
            short_name = item_info['name'].split('|')[1].strip() if '|' in item_info['name'] else item_info['name']
            if len(short_name) > 20:
                short_name = short_name[:20] + '...'
            
            keyboard.append([InlineKeyboardButton(
                short_name,
                callback_data=f'cs2_item_{item_id}'
            )])
        
        keyboard.append([InlineKeyboardButton(get_text(user.lang, 'back'), callback_data='cs2_menu')])
        
        category_name = get_text(user.lang, f'cs2_{category}')
        await query.edit_message_text(
            get_text(user.lang, 'cs2_select_item', category=category_name),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def show_item_prices(self, query, user, item_id: str):
        """Show prices for a specific CS2 item."""
        await query.edit_message_text(
            f"💎 {get_text(user.lang, 'loading')}...\n\n{get_text(user.lang, 'cs2_fetching_prices')}",
            parse_mode='Markdown'
        )
        
        # Get item prices
        price_data = self.cs2_service.get_item_prices(item_id)
        
        if not price_data:
            await query.edit_message_text(
                get_text(user.lang, 'cs2_price_error', item=item_id),
                parse_mode='Markdown'
            )
            return
        
        # Format marketplace prices
        price_lines = []
        for marketplace, price in price_data['prices'].items():
            marketplace_name = marketplace.capitalize()
            if marketplace == price_data['min_marketplace']:
                price_lines.append(f"✅ **{marketplace_name}:** ${price:.2f} _← Best price!_")
            elif marketplace == price_data['max_marketplace']:
                price_lines.append(f"⚠️ **{marketplace_name}:** ${price:.2f}")
            else:
                price_lines.append(f"• **{marketplace_name}:** ${price:.2f}")
        
        prices_text = '\n'.join(price_lines)
        
        # Create detailed message
        message = (
            f"💎 **{price_data['name']}**\n"
            f"🏷️ Quality: {price_data['quality']}\n"
            f"📦 Category: {price_data['category']}\n\n"
            f"💰 **Prices:**\n"
            f"{prices_text}\n\n"
            f"📊 **Statistics:**\n"
            f"💵 Average: **${price_data['avg_price']:.2f}**\n"
            f"📈 Highest: ${price_data['max_price']:.2f} ({price_data['max_marketplace'].capitalize()})\n"
            f"📉 Lowest: ${price_data['min_price']:.2f} ({price_data['min_marketplace'].capitalize()})\n"
            f"📊 Spread: {price_data['spread_pct']:.2f}% (${price_data['spread_usd']:.2f})\n\n"
        )
        
        # Add recommendation
        if len(price_data['prices']) > 1:
            savings = price_data['max_price'] - price_data['min_price']
            message += (
                f"💡 **Recommendation:**\n"
                f"Buy on **{price_data['min_marketplace'].capitalize()}** "
                f"to save ${savings:.2f}!\n\n"
            )
        
        message += f"⏰ Updated: {datetime.fromisoformat(price_data['timestamp']).strftime('%H:%M')}"
        
        # Find category for back button
        item_info = self.cs2_service.POPULAR_ITEMS[item_id]
        category = item_info['category'].lower()
        if category == 'knife':
            category = 'knives'
        elif category == 'gloves':
            category = 'gloves'
        elif category == 'rifle':
            category = 'rifles'
        elif category == 'sniper':
            category = 'snipers'
        elif category == 'pistol':
            category = 'pistols'
        elif category == 'smg':
            category = 'smgs'
        
        keyboard = [
            [InlineKeyboardButton(
                '🔄 ' + get_text(user.lang, 'refresh'),
                callback_data=f'cs2_item_{item_id}'
            )],
            [InlineKeyboardButton(
                get_text(user.lang, 'back'),
                callback_data=f'cs2_cat_{category}'
            )]
        ]
        
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        
        # Log metrics
        self.bot.metrics.log_cs2_query(user.telegram_id)
    
    async def handle_cs2_callback(self, query, user, data: str):
        """Handle CS2-related callbacks."""
        if data == 'cs2_menu':
            # Create update-like object for show_cs2_menu
            class FakeUpdate:
                callback_query = query
                effective_user = query.from_user
                message = query.message
            
            await self.show_cs2_menu(FakeUpdate(), None)
        
        elif data.startswith('cs2_cat_'):
            category = data.replace('cs2_cat_', '')
            await self.show_category_items(query, user, category)
        
        elif data.startswith('cs2_item_'):
            item_id = data.replace('cs2_item_', '')
            await self.show_item_prices(query, user, item_id)
