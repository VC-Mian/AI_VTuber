"""
TTS Engine Module - Handles text-to-speech conversion

This module:
- Converts AI responses to speech
- Runs in separate thread to avoid blocking
- Automatically selects female voice if available
- Allows runtime toggling of TTS

Future improvements:
- Upgrade to ElevenLabs for better voice quality
- Add multilingual support
- Implement custom voice profiles
"""

import pyttsx3
import threading
from src.config import Config

class TTSEngine:
    """Handles text-to-speech conversion"""
    
    def __init__(self):
        self.enabled = Config.TTS_ENABLED
        self.rate = Config.TTS_RATE
        self.volume = Config.TTS_VOLUME
        self.voice_id = None
        
        if self.enabled:
            try:
                # Initialize once to find the best voice
                temp_engine = pyttsx3.init()
                voices = temp_engine.getProperty('voices')
                
                # Try to find a female voice (customize this if needed)
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.voice_id = voice.id
                        break
                
                temp_engine.stop()
                del temp_engine
                
                print("✓ TTS Engine initialized")
            except Exception as e:
                print(f"⚠ Failed to initialize TTS: {e}")
                print("  Bot will continue without TTS.")
                self.enabled = False
        else:
            print("TTS is disabled")
    
    def speak(self, text):
        """
        Convert text to speech
        
        Args:
            text: The text to speak
        """
        if not self.enabled:
            return
        
        try:
            # Run TTS in a separate thread so it doesn't block the bot
            thread = threading.Thread(target=self._speak_thread, args=(text,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def _speak_thread(self, text):
        """
        Internal method to handle TTS in separate thread
        
        Creates a new engine instance for each speech operation to avoid
        threading conflicts with pyttsx3.
        """
        try:
            # Create a NEW engine instance for each speech operation
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)
            
            if self.voice_id:
                engine.setProperty('voice', self.voice_id)
            
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            del engine  # Clean up
        except Exception as e:
            print(f"TTS Thread Error: {e}")
    
    def set_rate(self, rate):
        """
        Set speech rate
        
        Args:
            rate: Words per minute (typical: 150-200)
        """
        self.rate = rate
    
    def set_volume(self, volume):
        """
        Set speech volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = volume
    
    def toggle(self):
        """
        Toggle TTS on/off
        
        Returns:
            Boolean indicating new state (True = enabled)
        """
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        print(f"TTS {status}")
        return self.enabled