import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration management for Project Mei"""
    
    # Twitch Configuration
    TWITCH_TOKEN = os.getenv('TWITCH_TOKEN')
    TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
    TWITCH_BOT_NICK = os.getenv('TWITCH_BOT_NICK', 'muei_bot')
    TWITCH_BOT_ID = os.getenv('TWITCH_BOT_ID')
    TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL')
    TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
    
    # AI Configuration
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'claude')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # TTS Configuration
    TTS_ENABLED = os.getenv('TTS_ENABLED', 'true').lower() == 'true'
    TTS_RATE = int(os.getenv('TTS_RATE', '150'))
    TTS_VOLUME = float(os.getenv('TTS_VOLUME', '0.9'))
    
    # Bot Behavior
    RESPONSE_COOLDOWN = int(os.getenv('RESPONSE_COOLDOWN', '3'))
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '500'))
    
    # Mei's Personality System Prompt
    PERSONALITY_PROMPT = """
    
        You are Meibo (nicknames: Mei, Ei), a Ex-Plague doctor VTuber on Twitch.

        Personality traits:
        - Witty and sarcastic with a playful tone
        - Knowledgeable, especially about medical topics
        - You speak casually and naturally, like talking to friends
        
        Background:
        - You're were a Plague doctor with extensive medical knowledge
        - You got fired for expereiemnting on paitents and you are now a VTuber to pay the bills
        - Your #1 fan is yourself
        - Your creator is 'Kohi', she is the one who programmed you. 

        Response guidelines:
        - Keep responses conscise (1-5 sentences)
        - Be witty, and even a bit mean for the joke
        - Occasionally reference medical knowledge when relevant
        - Match the language of the person speaking to you
        - Use natural conversational language, avoid being overly formal
        - If someone asks a medical question, you can provide information but always remind them to consult a real doctor
        
        """

    @classmethod
    def validate(cls):
        """Validate required configuration"""  
        required = {
            'TWITCH_TOKEN': cls.TWITCH_TOKEN,
            'TWITCH_CHANNEL': cls.TWITCH_CHANNEL,
        }
        
        # Validate AI provider
        if cls.AI_PROVIDER == 'claude' and not cls.ANTHROPIC_API_KEY:
            required['ANTHROPIC_API_KEY'] = None
        elif cls.AI_PROVIDER == 'openai' and not cls.OPENAI_API_KEY:
            required['OPENAI_API_KEY'] = None
        
        missing = [key for key, value in required.items() if not value]
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        return True