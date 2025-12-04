"""
AI Brain Module - Handles LLM integration and response generation

CUSTOMIZATION GUIDE:
1. Update trigger words in should_respond() method (bottom of file)
2. Adjust max_history if needed (default: 10 messages)
3. Modify max_tokens in _generate_claude_response() for longer/shorter responses
"""

import anthropic
from src.config import Config

class AIBrain:
    """Handles AI processing and response generation"""
    
    def __init__(self):
        self.provider = Config.AI_PROVIDER
        self.conversation_history = []
        self.max_history = 10  # Keep last 10 messages for context
        
        # Initialize Claude client
        if self.provider == 'claude':
            self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            self.model = "claude-sonnet-4-20250514"
        else:
            raise ValueError(f"Unknown AI provider: {self.provider}")
        
        print(f"AI Brain initialized with provider: {self.provider}")
    
    def generate_response(self, username, message, language='en'):
        """
        Generate a response to a chat message
        
        Args:
            username: The user who sent the message
            message: The message content
            language: Language code (for future multilingual support)
        
        Returns:
            Generated response string
        """
        try:
            # Add user message to history
            user_prompt = f"{username}: {message}"
            
            return self._generate_claude_response(user_prompt)
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, my connection is a bit glitchy right now... try again?"
    
    def _generate_claude_response(self, user_prompt):
        """Generate response using Claude API"""
        # Build conversation history
        messages = self.conversation_history + [
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=300,  # Adjust this to control response length
            system=Config.PERSONALITY_PROMPT,
            messages=messages
        )
        
        assistant_message = response.content[0].text
        
        # Update conversation history
        self._update_history(user_prompt, assistant_message)
        
        return assistant_message
    
    def _update_history(self, user_message, assistant_message):
        """Update conversation history with size limit"""
        # Add messages to history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        
        # Keep only recent messages to avoid context overflow
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-(self.max_history * 2):]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("Conversation history cleared")
    
    def should_respond(self, message):
        """
        Determine if the bot should respond to a message
        
        Args:
            message: The chat message
        
        Returns:
            Boolean indicating whether to respond
        """
        # =====================================================================
        # CUSTOMIZE YOUR BOT'S TRIGGER WORDS HERE
        # =====================================================================
        # The bot will respond when ANY of these words appear in chat
        # Make them case-insensitive by converting message to lowercase
        
        triggers = [
            'yourbot',      # Replace with your bot's main name
            'botname',      # Add nicknames or variations
            'nickname',     # Add as many as you want
            '!yourbot'      # Command version
        ]
        
        # Convert message to lowercase for case-insensitive matching
        message_lower = message.lower()
        
        # Return True if any trigger word is found in the message
        return any(trigger in message_lower for trigger in triggers)