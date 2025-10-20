"""AI Assistant service using Qwen3-8B model via Ollama for intelligent bot control."""

import asyncio
import json
import re
from typing import Optional, List, Dict, Tuple, Any
import aiohttp
from ..utils.logger import setup_logger

logger = setup_logger('ai_service')


class AIService:
    """Service for AI assistant powered by Qwen3-8B with bot command interpretation."""
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "qwen3:8b"):
        """
        Initialize AI service with Qwen3-8B.
        
        Args:
            ollama_url: Ollama API endpoint
            model: Model name (default: qwen3:8b)
        """
        self.ollama_url = ollama_url
        self.model = model
        self.available = False
        self.context_limit = 8192  # Qwen3-8B has larger context
        self.conversation_history = {}  # Store conversation per user
        
        logger.info(f"AI Service initialized with Qwen3-8B model: {model}")
    
    async def check_availability(self, auto_pull: bool = True) -> bool:
        """
        Check if Ollama service is available and optionally pull model.
        
        Args:
            auto_pull: Automatically pull model if not found
        
        Returns:
            True if available, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_url}/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        # Check if model is available
                        data = await response.json()
                        models = data.get('models', [])
                        model_names = [m.get('name', '') for m in models]
                        
                        # If model not found, try to pull it
                        if self.model not in model_names:
                            if auto_pull:
                                logger.warning(f"Model {self.model} not found locally. Starting automatic download...")
                                logger.warning(f"This may take 5-10 minutes for first-time setup. Please wait...")
                                pulled = await self._pull_model()
                                self.available = pulled
                                if pulled:
                                    logger.info(f"✅ Model {self.model} downloaded and ready!")
                                else:
                                    logger.error(f"❌ Failed to download model {self.model}. Please run: ollama pull {self.model}")
                            else:
                                logger.warning(f"Model {self.model} not found. Run: ollama pull {self.model}")
                                self.available = False
                        else:
                            logger.info(f"✅ Model {self.model} is available")
                            self.available = True
                        
                        return self.available
                    else:
                        logger.error(f"Ollama API returned status {response.status}")
                        return False
        except aiohttp.ClientConnectorError:
            logger.error(f"Cannot connect to Ollama at {self.ollama_url}. Is Ollama running?")
            logger.error(f"Install Ollama from https://ollama.ai and start the service.")
            self.available = False
            return False
        except Exception as e:
            logger.error(f"Error checking Ollama availability: {e}")
            self.available = False
            return False
    
    async def _pull_model(self) -> bool:
        """
        Pull the model from Ollama.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"📥 Downloading {self.model} model...")
            logger.info(f"⏳ This will take 5-10 minutes (model size ~5GB). Please be patient...")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_url}/api/pull",
                    json={'name': self.model},
                    timeout=aiohttp.ClientTimeout(total=900)  # 15 minutes for download
                ) as response:
                    if response.status == 200:
                        # Show progress by reading stream
                        last_status = None
                        async for line in response.content:
                            try:
                                # Try to parse progress info
                                import json
                                data = json.loads(line.decode('utf-8'))
                                status = data.get('status', '')
                                if status and status != last_status:
                                    logger.info(f"📦 {status}")
                                    last_status = status
                            except:
                                pass
                        
                        logger.info(f"✅ Model {self.model} downloaded successfully!")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Failed to pull model (HTTP {response.status}): {error_text}")
                        return False
        except asyncio.TimeoutError:
            logger.error(f"❌ Model download timeout. Please check your internet connection.")
            return False
        except Exception as e:
            logger.error(f"❌ Error pulling model: {e}")
            logger.error(f"💡 Try manually: ollama pull {self.model}")
            return False
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                      temperature: float = 0.7, max_tokens: int = 500) -> Dict:
        """
        Generate response from AI model.
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Max tokens to generate
        
        Returns:
            Response dict with text and metadata
        """
        if not self.available:
            await self.check_availability()
            if not self.available:
                return {
                    'success': False,
                    'error': 'AI service not available',
                    'message': 'Ollama is not running or model not installed'
                }
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        return {
                            'success': True,
                            'text': data.get('response', '').strip(),
                            'model': data.get('model'),
                            'total_duration': data.get('total_duration', 0) / 1e9,  # Convert to seconds
                            'eval_count': data.get('eval_count', 0)
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Ollama API error: {error_text}")
                        return {
                            'success': False,
                            'error': f"API error: {response.status}",
                            'message': error_text
                        }
        
        except asyncio.TimeoutError:
            logger.error("Ollama request timeout")
            return {
                'success': False,
                'error': 'timeout',
                'message': 'Request took too long'
            }
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return {
                'success': False,
                'error': 'exception',
                'message': str(e)
            }
    
    async def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict:
        """
        Chat with AI using conversation history.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
        
        Returns:
            Response dict
        """
        if not self.available:
            await self.check_availability()
            if not self.available:
                return {
                    'success': False,
                    'error': 'AI service not available'
                }
        
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_url}/api/chat",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        return {
                            'success': True,
                            'message': data.get('message', {}),
                            'text': data.get('message', {}).get('content', '').strip(),
                            'total_duration': data.get('total_duration', 0) / 1e9
                        }
                    else:
                        return {
                            'success': False,
                            'error': f"API error: {response.status}"
                        }
        
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def analyze_market(self, asset: str, price: float, change_24h: float, 
                           user_query: str = None) -> str:
        """
        Analyze market data for an asset.
        
        Args:
            asset: Asset symbol
            price: Current price
            change_24h: 24h change percentage
            user_query: Optional user question
        
        Returns:
            AI analysis text
        """
        system_prompt = (
            "You are a financial assistant helping users understand cryptocurrency and stock markets. "
            "Provide brief, clear explanations. Be helpful but remind users this is not financial advice."
        )
        
        prompt = f"""Analyze this market data:
Asset: {asset}
Current Price: ${price:,.2f}
24h Change: {change_24h:+.2f}%

"""
        if user_query:
            prompt += f"User question: {user_query}\n\n"
        
        prompt += "Provide a brief analysis (2-3 sentences)."
        
        result = await self.generate(prompt, system_prompt=system_prompt, temperature=0.5, max_tokens=200)
        
        if result.get('success'):
            return result['text']
        else:
            return "AI analysis unavailable."
    
    async def analyze_portfolio(self, portfolio_data: Dict, user_query: str = None) -> str:
        """
        Analyze user's portfolio.
        
        Args:
            portfolio_data: Portfolio information
            user_query: Optional user question
        
        Returns:
            AI analysis text
        """
        system_prompt = (
            "You are a financial portfolio advisor. Provide helpful insights about portfolio composition, "
            "diversification, and risk. Keep responses concise. Remind users this is not financial advice."
        )
        
        total_value = portfolio_data.get('total_value', 0)
        items = portfolio_data.get('items', [])
        
        prompt = f"""Analyze this portfolio:
Total Value: ${total_value:,.2f}
Number of Assets: {len(items)}

Assets breakdown:
"""
        for item in items[:10]:  # Limit to top 10
            prompt += f"- {item['symbol']}: ${item.get('value', 0):,.2f} ({item.get('percentage', 0):.1f}%)\n"
        
        if user_query:
            prompt += f"\nUser question: {user_query}\n"
        
        prompt += "\nProvide brief portfolio analysis (3-4 sentences)."
        
        result = await self.generate(prompt, system_prompt=system_prompt, temperature=0.6, max_tokens=300)
        
        if result.get('success'):
            return result['text']
        else:
            return "AI analysis unavailable."
    
    async def interpret_user_message(self, message: str, user_lang: str = 'en') -> Dict[str, Any]:
        """
        Interpret user message and extract command or provide text response.
        
        Args:
            message: User's message
            user_lang: User's language (en/ru)
        
        Returns:
            Dict with 'type' ('command' or 'text'), 'action', 'params', and 'response'
        """
        system_prompt = (
            "You are an intelligent assistant for CoinFlow Bot. Your job is to interpret user requests and either:\n"
            "1. Extract a bot command if user wants to use a feature (forecast, chart, convert, compare, etc.)\n"
            "2. Provide a helpful text response if they're asking a general question\n\n"
            "Available bot commands:\n"
            "- FORECAST <symbol>: Show AI price forecast for cryptocurrency (e.g., BTC, ETH)\n"
            "- CHART <symbol> <days>: Show price chart (days: 7, 30, 90, 365)\n"
            "- CONVERT <amount> <from> <to>: Convert currency\n"
            "- COMPARE <symbol>: Compare prices across exchanges\n"
            "- STATS: Show user statistics\n"
            "- NEWS: Show crypto news\n"
            "- HELP: Show help information\n\n"
            "If user wants to use a feature, respond with JSON: {\"command\": \"FORECAST\", \"symbol\": \"BTC\"}\n"
            "If user asks a question, respond normally without JSON.\n\n"
            "Be concise and helpful. Language: " + ('Russian' if user_lang == 'ru' else 'English')
        )
        
        result = await self.generate(message, system_prompt=system_prompt, temperature=0.3, max_tokens=300)
        
        if not result.get('success'):
            return {'type': 'error', 'response': 'AI service unavailable'}
        
        response_text = result['text']
        
        # Try to parse JSON command
        command = self._extract_command(response_text)
        
        if command:
            return {
                'type': 'command',
                'action': command.get('command', '').upper(),
                'params': command,
                'response': None
            }
        else:
            return {
                'type': 'text',
                'action': None,
                'params': None,
                'response': response_text
            }
    
    def _extract_command(self, text: str) -> Optional[Dict]:
        """
        Extract JSON command from AI response.
        
        Args:
            text: AI response text
        
        Returns:
            Parsed command dict or None
        """
        try:
            # Try to find JSON in response
            json_match = re.search(r'\{[^}]+\}', text)
            if json_match:
                command = json.loads(json_match.group())
                if 'command' in command:
                    return command
        except:
            pass
        
        # Fallback: pattern matching for common requests
        text_lower = text.lower()
        
        # Forecast patterns
        if any(word in text_lower for word in ['forecast', 'прогноз', 'prediction', 'predict']):
            symbols = re.findall(r'\b(BTC|ETH|BNB|SOL|XRP|ADA|DOGE|MATIC|DOT|AVAX)\b', text.upper())
            if symbols:
                return {'command': 'FORECAST', 'symbol': symbols[0]}
        
        # Chart patterns
        if any(word in text_lower for word in ['chart', 'график', 'graph']):
            symbols = re.findall(r'\b(BTC|ETH|BNB|SOL|XRP|ADA|DOGE|MATIC|DOT|AVAX|CNY|USD|EUR|RUB)\b', text.upper())
            days_match = re.search(r'(\d+)\s*(day|days|дней|день)', text_lower)
            days = int(days_match.group(1)) if days_match else 30
            if symbols:
                return {'command': 'CHART', 'symbol': symbols[0], 'days': days}
        
        # Compare patterns
        if any(word in text_lower for word in ['compare', 'сравни', 'comparison']):
            symbols = re.findall(r'\b(BTC|ETH|BNB|SOL|XRP|ADA|DOGE)\b', text.upper())
            if symbols:
                return {'command': 'COMPARE', 'symbol': symbols[0]}
        
        # Convert patterns
        convert_match = re.search(r'(\d+\.?\d*)\s*([A-Z]{3})\s*(?:to|в|in)\s*([A-Z]{3})', text.upper())
        if convert_match:
            return {
                'command': 'CONVERT',
                'amount': float(convert_match.group(1)),
                'from': convert_match.group(2),
                'to': convert_match.group(3)
            }
        
        return None
    
    async def explain_forecast(self, symbol: str, forecast_data: Dict, model_type: str = 'ARIMA', 
                               user_lang: str = 'en') -> str:
        """
        Explain ARIMA/LinReg forecast in simple terms using Qwen3-8B.
        
        Args:
            symbol: Cryptocurrency symbol
            forecast_data: Forecast statistics from prediction service
            model_type: 'ARIMA' or 'LINEAR'
            user_lang: User language
        
        Returns:
            AI explanation text
        """
        system_prompt = (
            "You are a financial education assistant. Explain cryptocurrency price forecasts in simple, "
            "easy-to-understand language. Your audience may not know technical analysis. "
            f"Language: {'Russian' if user_lang == 'ru' else 'English'}. "
            "Keep explanations to 3-4 sentences. Always end with a disclaimer."
        )
        
        current = forecast_data.get('current', 0)
        predicted = forecast_data.get('predicted', 0)
        change = forecast_data.get('change', 0)
        trend = forecast_data.get('trend', 'Unknown')
        confidence = forecast_data.get('confidence', 'medium')
        days_analyzed = forecast_data.get('days_analyzed', 90)
        
        model_description = (
            "ARIMA (AutoRegressive Integrated Moving Average) - a statistical model that identifies patterns in time series"
            if model_type == 'ARIMA' else
            "Linear Regression - a mathematical model that finds trends in historical data"
        )
        
        prompt = f"""Explain this {symbol} price forecast:

Model: {model_type} ({model_description})
Current Price: ${current:,.2f}
7-Day Forecast: ${predicted:,.2f}
Expected Change: {change:+.2f}%
Trend: {trend}
Confidence: {confidence}
Data analyzed: {days_analyzed} days of historical prices

Explain:
1. Why the model predicts this trend (in simple terms)
2. What this means for {symbol}
3. Key disclaimer

Keep it brief and educational."""
        
        result = await self.generate(prompt, system_prompt=system_prompt, temperature=0.6, max_tokens=250)
        
        if result.get('success'):
            return result['text']
        else:
            return (
                f"The {model_type} model analyzed {days_analyzed} days of {symbol} price history and "
                f"predicts a {change:+.2f}% change over the next 7 days. This is based on statistical patterns, "
                f"not financial advice."
            )
    
    async def answer_question(self, question: str, context: str = None, user_lang: str = 'en') -> str:
        """
        Answer user's question about finance/crypto.
        
        Args:
            question: User's question
            context: Optional context
            user_lang: User language
        
        Returns:
            AI answer
        """
        system_prompt = (
            "You are a helpful financial assistant for CoinFlow Bot. "
            "Answer questions about cryptocurrencies, stocks, and financial markets. "
            "Be concise, accurate, and friendly. Always remind users that this is educational, not financial advice. "
            f"Language: {'Russian' if user_lang == 'ru' else 'English'}."
        )
        
        prompt = question
        if context:
            prompt = f"Context: {context}\n\nQuestion: {question}"
        
        result = await self.generate(prompt, system_prompt=system_prompt, temperature=0.7, max_tokens=400)
        
        if result.get('success'):
            return result['text']
        else:
            return "Sorry, I couldn't generate a response. Please try again."
    
    async def suggest_action(self, user_intent: str, bot_features: List[str]) -> str:
        """
        Suggest bot actions based on user intent.
        
        Args:
            user_intent: What user wants to do
            bot_features: Available bot features
        
        Returns:
            Suggestion text
        """
        system_prompt = (
            "You are an assistant helping users navigate CoinFlow Bot. "
            "Suggest which bot features to use based on what the user wants to do. "
            "Be brief and direct."
        )
        
        prompt = f"""User wants to: {user_intent}

Available features: {', '.join(bot_features)}

Suggest 1-2 most relevant features and explain briefly how they help."""
        
        result = await self.generate(prompt, system_prompt=system_prompt, temperature=0.5, max_tokens=150)
        
        if result.get('success'):
            return result['text']
        else:
            return "Try using the main menu buttons to explore bot features."
