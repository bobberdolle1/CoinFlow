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
            [InlineKeyboardButton('🔍 ' + get_text(user.lang, 'cs2_search'), callback_data='cs2_search')],
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
    
    async def show_category_items(self, query, user, category: str, page: int = 0):
        """Show items in a specific category with pagination."""
        items = self.cs2_service.get_items_by_category(category)
        
        if not items:
            await query.edit_message_text(
                get_text(user.lang, 'cs2_no_items'),
                parse_mode='Markdown'
            )
            return
        
        # Pagination settings
        items_per_page = 8
        total_pages = (len(items) + items_per_page - 1) // items_per_page
        start_idx = page * items_per_page
        end_idx = min(start_idx + items_per_page, len(items))
        
        # Create keyboard with items on current page
        keyboard = []
        for item_id in items[start_idx:end_idx]:
            item_info = self.cs2_service.POPULAR_ITEMS[item_id]
            # Shorten name for button
            short_name = item_info['name'].split('|')[1].strip() if '|' in item_info['name'] else item_info['name']
            if len(short_name) > 20:
                short_name = short_name[:20] + '...'
            
            keyboard.append([InlineKeyboardButton(
                short_name,
                callback_data=f'cs2_item_{item_id}'
            )])
        
        # Add pagination buttons if needed
        if total_pages > 1:
            nav_buttons = []
            if page > 0:
                nav_buttons.append(InlineKeyboardButton(
                    '◀️ ' + get_text(user.lang, 'previous'),
                    callback_data=f'cs2_cat_{category}_page_{page-1}'
                ))
            if page < total_pages - 1:
                nav_buttons.append(InlineKeyboardButton(
                    get_text(user.lang, 'next') + ' ▶️',
                    callback_data=f'cs2_cat_{category}_page_{page+1}'
                ))
            if nav_buttons:
                keyboard.append(nav_buttons)
        
        keyboard.append([InlineKeyboardButton(get_text(user.lang, 'back'), callback_data='cs2_menu')])
        
        category_name = get_text(user.lang, f'cs2_{category}')
        page_info = f" ({page+1}/{total_pages})" if total_pages > 1 else ""
        await query.edit_message_text(
            get_text(user.lang, 'cs2_select_item', category=category_name) + page_info,
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
    
    async def start_search(self, query, user):
        """Start CS2 item search."""
        # Set user state to awaiting search
        self.bot.temp_storage[user.telegram_id] = {
            'state': 'awaiting_cs2_search'
        }
        
        keyboard = [[InlineKeyboardButton(get_text(user.lang, 'back'), callback_data='cs2_menu')]]
        
        await query.edit_message_text(
            get_text(user.lang, 'cs2_search_prompt'),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def handle_search_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE, search_query: str):
        """Handle CS2 item search query."""
        user_id = update.effective_user.id
        user = self.bot.db.get_or_create_user(user_id)
        
        # Search items
        results = self.cs2_service.search_items(search_query, limit=10)
        
        if not results:
            keyboard = [[InlineKeyboardButton(get_text(user.lang, 'back'), callback_data='cs2_menu')]]
            await update.message.reply_text(
                get_text(user.lang, 'cs2_search_no_results', query=search_query),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            return
        
        # Display results
        keyboard = []
        for item_id in results:
            item_info = self.cs2_service.POPULAR_ITEMS[item_id]
            keyboard.append([InlineKeyboardButton(
                item_info['name'],
                callback_data=f'cs2_item_{item_id}'
            )])
        
        keyboard.append([InlineKeyboardButton(get_text(user.lang, 'back'), callback_data='cs2_menu')])
        
        await update.message.reply_text(
            get_text(user.lang, 'cs2_search_results', query=search_query, count=len(results)),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def handle_cs2_callback(self, query, user, data: str):
        """Handle CS2-related callbacks."""
        if data == 'cs2_menu':
            # Create update-like object for show_cs2_menu
            class FakeUpdate:
                callback_query = query
                effective_user = query.from_user
                message = query.message
            
            await self.show_cs2_menu(FakeUpdate(), None)
        
        elif data == 'cs2_search':
            await self.start_search(query, user)
        
        elif data.startswith('cs2_cat_'):
            # Handle pagination: cs2_cat_rifles_page_1 or cs2_cat_rifles
            parts = data.replace('cs2_cat_', '').split('_page_')
            category = parts[0]
            page = int(parts[1]) if len(parts) > 1 else 0
            await self.show_category_items(query, user, category, page)
        
        elif data.startswith('cs2_item_'):
            item_id = data.replace('cs2_item_', '')
            await self.show_item_prices(query, user, item_id)
