# from twitchio.ext import commands
from queue import Queue
from src.config import Config
from src.ai_brain import AIBrain
from src.tts_engine import TTSEngine
from src.vtuber_controller import VTuberController

def __init__(self):
    # Initialize the bot with Twitch credentials
    super().__init__(
        token=Config.TWITCH_TOKEN,
        client_id=Config.TWITCH_CLIENT_ID,
        client_secret=Config.TWITCH_CLIENT_SECRET,
        bot_id=Config.TWITCH_BOT_ID,
        nick=Config.TWITCH_BOT_NICK,
        prefix='!',
        initial_channels=[Config.TWITCH_CHANNEL]
    )
    
    # Initialize AI and TTS
    self.ai_brain = AIBrain()
    self.tts_engine = TTSEngine()

        
    # Initialize VTuber controller
    self.vtuber = VTuberController()
    
    # Message queue for handling multiple requests
    self.message_queue = Queue()
    self.is_processing = False
    
    # Rate limiting
    self.last_response_time = 0
    self.response_cooldown = Config.RESPONSE_COOLDOWN
    
    print(f"Muei Bot initialized! Joining channel: {Config.TWITCH_CHANNEL}")