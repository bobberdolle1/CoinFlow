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
    
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages."""
        user_id = update.effective_user.id
        user = self.bot.db.get_user(user_id)
        
        # Check if voice service is available
        if not self.bot.voice_service.is_available():
            await update.message.reply_text(
                "❌ **Voice Recognition Not Available**\n\n"
                "Required libraries are not installed.\n\n"
                "Install with: `pip install SpeechRecognition pydub`\n\n"
                "Also install ffmpeg for audio processing.",
                parse_mode='Markdown'
            )
            return
        
        try:
            # Show processing message
            processing_msg = await update.message.reply_text(
                "🎤 Processing voice message..."
            )
            
            # Get voice file
            voice = update.message.voice
            voice_file = await context.bot.get_file(voice.file_id)
            
            # Download voice data
            voice_bytes = await voice_file.download_as_bytearray()
            
            # Process voice message
            result = await self.bot.voice_service.process_voice_message(
                bytes(voice_bytes),
                language=user.lang
            )
            
            if not result.get('success'):
                error_msg = result.get('message', 'Unknown error')
                await processing_msg.edit_text(
                    f"❌ **Recognition Failed**\n\n{error_msg}",
                    parse_mode='Markdown'
                )
                return
            
            # Get recognized text
            recognized_text = result.get('text', '')
            
            # Try to parse as conversion command
            command = self.bot.voice_service.parse_conversion_command(recognized_text)
            
            if command:
                # Execute conversion
                await processing_msg.edit_text(
                    f"🎤 Recognized: *{recognized_text}*\n\n"
                    f"⏳ Converting {command['amount']} {command['from_currency']} to {command['to_currency']}...",
                    parse_mode='Markdown'
                )
                
                try:
                    # Get conversion rate
                    rate = self.bot.converter.get_rate(
                        command['from_currency'],
                        command['to_currency']
                    )
                    
                    if not rate:
                        await processing_msg.edit_text(
                            f"🎤 Recognized: *{recognized_text}*\n\n"
                            f"❌ Unable to get rate for {command['from_currency']}/{command['to_currency']}",
                            parse_mode='Markdown'
                        )
                        return
                    
                    result_amount = command['amount'] * rate
                    
                    # Save to history
                    self.bot.db.add_conversion(
                        user_id,
                        command['from_currency'],
                        command['to_currency'],
                        command['amount'],
                        result_amount,
                        rate
                    )
                    
                    # Send result
                    await processing_msg.edit_text(
                        f"🎤 **Voice Command Executed**\n\n"
                        f"🗣 Recognized: _{recognized_text}_\n\n"
                        f"💱 **{command['amount']:,.2f} {command['from_currency']}** = "
                        f"**{result_amount:,.2f} {command['to_currency']}**\n\n"
                        f"📉 Rate: {rate:,.6f}",
                        parse_mode='Markdown'
                    )
                    
                    self.bot.metrics.log_conversion(user_id)
                    logger.info(f"Voice conversion executed: {command['amount']} {command['from_currency']} -> {command['to_currency']}")
                    
                except Exception as e:
                    logger.error(f"Error executing voice conversion: {e}")
                    await processing_msg.edit_text(
                        f"🎤 Recognized: *{recognized_text}*\n\n"
                        f"❌ Error: {str(e)}",
                        parse_mode='Markdown'
                    )
            else:
                # Just show recognized text
                await processing_msg.edit_text(
                    f"🎤 **Recognized Text:**\n\n"
                    f"_{recognized_text}_\n\n"
                    f"ℹ️ I couldn't parse this as a conversion command.\n\n"
                    f"Try: _'100 USD to EUR'_ or _'convert 50 bitcoin to dollars'_",
                    parse_mode='Markdown'
                )
        
        except Exception as e:
            logger.error(f"Error handling voice message: {e}")
            await update.message.reply_text(
                f"❌ Error processing voice message: {str(e)}",
                parse_mode='Markdown'
            )
    
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
        elif text == get_text(user.lang, 'news'):
            await self.bot.news_handler.show_news_menu(update, context)
        elif text == get_text(user.lang, 'reports_btn'):
            await self.bot.report_handler.show_report_menu(update, context)
        elif text == get_text(user.lang, 'dashboard_btn'):
            await self.bot.dashboard_handler.show_dashboard_menu(update, context)
        elif text == get_text(user.lang, 'ai_assistant'):
            await self.bot.ai_handler.show_ai_menu(update, context)
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
            await self.show_about(update, context)
        else:
            # Check if user is in AI conversation mode
            temp_data = self.bot.temp_storage.get(user_id)
            if temp_data and temp_data.get('action') == 'ai_question':
                await self.bot.ai_handler.process_question(update, text)
                del self.bot.temp_storage[user_id]
                return
            elif temp_data and temp_data.get('action') == 'ai_suggest':
                await self.bot.ai_handler.process_suggestion_request(update, text)
                del self.bot.temp_storage[user_id]
                return
            
            # Unknown command - show help
            await update.message.reply_text(
                get_text(user.lang, 'unknown_command'),
                parse_mode='Markdown'
            )
    
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
        
        # Add model accuracy comparison
        stats_text += "\n\n🎯 **Forecast Model Accuracy:**\n"
        
        # Get accuracy for BTC (most commonly predicted)
        accuracy_stats = self.bot.prediction_generator.get_accuracy_comparison('BTC', days=30)
        
        if accuracy_stats:
            arima = accuracy_stats.get('arima', {})
            linreg = accuracy_stats.get('linreg', {})
            
            if arima.get('count', 0) > 0:
                stats_text += f"\n📊 **ARIMA Model** (BTC)\n"
                stats_text += f"• Predictions: {arima['count']}\n"
                stats_text += f"• Avg Error: ${arima['avg_mae']:.2f}\n"
                stats_text += f"• Accuracy: {100 - arima['avg_mape']:.1f}%\n"
            
            if linreg.get('count', 0) > 0:
                stats_text += f"\n📊 **Linear Regression** (BTC)\n"
                stats_text += f"• Predictions: {linreg['count']}\n"
                stats_text += f"• Avg Error: ${linreg['avg_mae']:.2f}\n"
                stats_text += f"• Accuracy: {100 - linreg['avg_mape']:.1f}%\n"
            
            if arima.get('count', 0) > 0 and linreg.get('count', 0) > 0:
                # Show which is better
                better = 'ARIMA' if arima['avg_mape'] < linreg['avg_mape'] else 'Linear Regression'
                stats_text += f"\n🏆 **Best Model:** {better}\n"
        else:
            stats_text += "_No forecast history yet. Generate predictions to see accuracy stats!_\n"
        
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
