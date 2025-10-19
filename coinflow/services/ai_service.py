"""AI Assistant service using local Llama model via Ollama."""

import asyncio
from typing import Optional, List, Dict
import aiohttp
from ..utils.logger import setup_logger

logger = setup_logger('ai_service')


class AIService:
    """Service for AI assistant powered by Llama 3.2 3B."""
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama3.2:3b"):
        """
        Initialize AI service.
        
        Args:
            ollama_url: Ollama API endpoint
            model: Model name (default: llama3.2:3b)
        """
        self.ollama_url = ollama_url
        self.model = model
        self.available = False
        self.context_limit = 4096  # Token limit
        
        logger.info(f"AI Service initialized with model: {model}")
    
    async def check_availability(self) -> bool:
        """Check if Ollama is running and model is available."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_url}/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        data = await response.json()
                        models = [m['name'] for m in data.get('models', [])]
                        self.available = self.model in models
                        
                        if not self.available:
                            logger.warning(f"Model {self.model} not found. Available: {models}")
                            logger.info(f"Run: ollama pull {self.model}")
                        else:
                            logger.info(f"Model {self.model} is available")
                        
                        return self.available
        except Exception as e:
            logger.error(f"Ollama not available: {e}")
            self.available = False
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
    
    async def answer_question(self, question: str, context: str = None) -> str:
        """
        Answer user's question about finance/crypto.
        
        Args:
            question: User's question
            context: Optional context
        
        Returns:
            AI answer
        """
        system_prompt = (
            "You are a helpful financial assistant for CoinFlow Bot. "
            "Answer questions about cryptocurrencies, stocks, and financial markets. "
            "Be concise, accurate, and friendly. Always remind users that this is educational, not financial advice."
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
