"""Export handler for CoinFlow bot."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from io import BytesIO
from ..localization import get_text
from ..utils.logger import setup_logger

logger = setup_logger('export_handler')


class ExportHandler:
    """Handler for data export."""
    
    def __init__(self, bot):
        """Initialize export handler."""
        self.bot = bot
    
    async def show_export_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show export menu."""
        user_id = update.effective_user.id
        user = self.bot.db.get_user(user_id)
        
        keyboard = [
            [InlineKeyboardButton(get_text(user.lang, 'export_portfolio'), callback_data='export_portfolio')],
            [InlineKeyboardButton(get_text(user.lang, 'export_alerts'), callback_data='export_alerts')],
            [InlineKeyboardButton(get_text(user.lang, 'export_history'), callback_data='export_history')],
            [InlineKeyboardButton(get_text(user.lang, 'export_all'), callback_data='export_all')],
            [InlineKeyboardButton(get_text(user.lang, 'back'), callback_data='back_main')]
        ]
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                get_text(user.lang, 'export_menu'),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                get_text(user.lang, 'export_menu'),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
    
    async def handle_export_portfolio(self, query, user):
        """Export portfolio to CSV."""
        await query.answer()
        await query.edit_message_text(get_text(user.lang, 'export_generating'))
        
        try:
            # Get portfolio data
            portfolio_data = self.bot.portfolio_service.get_portfolio(user.telegram_id)
            
            if not portfolio_data:
                await query.edit_message_text(
                    get_text(user.lang, 'portfolio_empty'),
                    parse_mode='Markdown'
                )
                return
            
            # Generate CSV
            csv_data = self.bot.export_service.export_portfolio_csv(user.telegram_id, portfolio_data)
            
            if not csv_data:
                await query.edit_message_text(
                    get_text(user.lang, 'export_error', error='Failed to generate CSV'),
                    parse_mode='Markdown'
                )
                return
            
            # Send file
            filename = self.bot.export_service.get_export_filename(user.telegram_id, 'portfolio')
            file_buffer = BytesIO(csv_data.encode('utf-8'))
            file_buffer.name = filename
            
            await query.edit_message_text(get_text(user.lang, 'export_ready'))
            await query.message.reply_document(
                document=file_buffer,
                filename=filename,
                caption=f"📊 {get_text(user.lang, 'export_portfolio')}"
            )
            
            logger.info(f"Exported portfolio for user {user.telegram_id}")
            
        except Exception as e:
            logger.error(f"Error exporting portfolio: {e}")
            await query.edit_message_text(
                get_text(user.lang, 'export_error', error=str(e)),
                parse_mode='Markdown'
            )
    
    async def handle_export_alerts(self, query, user):
        """Export alerts to CSV."""
        await query.answer()
        await query.edit_message_text(get_text(user.lang, 'export_generating'))
        
        try:
            # Generate CSV
            csv_data = self.bot.export_service.export_alerts_csv(user.telegram_id)
            
            if not csv_data or csv_data == "Pair,Condition,Target Price,Created Date\n":
                await query.edit_message_text(
                    get_text(user.lang, 'no_alerts'),
                    parse_mode='Markdown'
                )
                return
            
            # Send file
            filename = self.bot.export_service.get_export_filename(user.telegram_id, 'alerts')
            file_buffer = BytesIO(csv_data.encode('utf-8'))
            file_buffer.name = filename
            
            await query.edit_message_text(get_text(user.lang, 'export_ready'))
            await query.message.reply_document(
                document=file_buffer,
                filename=filename,
                caption=f"🔔 {get_text(user.lang, 'export_alerts')}"
            )
            
            logger.info(f"Exported alerts for user {user.telegram_id}")
            
        except Exception as e:
            logger.error(f"Error exporting alerts: {e}")
            await query.edit_message_text(
                get_text(user.lang, 'export_error', error=str(e)),
                parse_mode='Markdown'
            )
    
    async def handle_export_history(self, query, user):
        """Export conversion history to CSV."""
        await query.answer()
        await query.edit_message_text(get_text(user.lang, 'export_generating'))
        
        try:
            # Generate CSV
            csv_data = self.bot.export_service.export_history_csv(user.telegram_id)
            
            if not csv_data or csv_data == "From Currency,To Currency,Amount,Result,Rate,Timestamp\n":
                await query.edit_message_text(
                    get_text(user.lang, 'history_empty'),
                    parse_mode='Markdown'
                )
                return
            
            # Send file
            filename = self.bot.export_service.get_export_filename(user.telegram_id, 'history')
            file_buffer = BytesIO(csv_data.encode('utf-8'))
            file_buffer.name = filename
            
            await query.edit_message_text(get_text(user.lang, 'export_ready'))
            await query.message.reply_document(
                document=file_buffer,
                filename=filename,
                caption=f"📜 {get_text(user.lang, 'export_history')}"
            )
            
            logger.info(f"Exported history for user {user.telegram_id}")
            
        except Exception as e:
            logger.error(f"Error exporting history: {e}")
            await query.edit_message_text(
                get_text(user.lang, 'export_error', error=str(e)),
                parse_mode='Markdown'
            )
    
    async def handle_export_all(self, query, user):
        """Export all data to ZIP archive."""
        await query.answer()
        await query.edit_message_text(get_text(user.lang, 'export_generating'))
        
        try:
            # Get portfolio data for ZIP
            portfolio_data = self.bot.portfolio_service.get_portfolio(user.telegram_id)
            
            # Generate ZIP
            zip_data = self.bot.export_service.create_export_zip(user.telegram_id, portfolio_data)
            
            if not zip_data:
                await query.edit_message_text(
                    get_text(user.lang, 'export_error', error='Failed to generate ZIP'),
                    parse_mode='Markdown'
                )
                return
            
            # Send file
            filename = self.bot.export_service.get_export_filename(user.telegram_id, 'all')
            file_buffer = BytesIO(zip_data)
            file_buffer.name = filename
            
            await query.edit_message_text(get_text(user.lang, 'export_ready'))
            await query.message.reply_document(
                document=file_buffer,
                filename=filename,
                caption=f"📦 {get_text(user.lang, 'export_all')}\n\nContents: Portfolio, Alerts, History, Favorites, User Info"
            )
            
            logger.info(f"Exported all data for user {user.telegram_id}")
            
        except Exception as e:
            logger.error(f"Error exporting all data: {e}")
            await query.edit_message_text(
                get_text(user.lang, 'export_error', error=str(e)),
                parse_mode='Markdown'
            )
