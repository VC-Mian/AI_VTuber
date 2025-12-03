'''
Allows meibo to speak in chat and in a separate thread. Picks random chatters comment to repsoned too. 

To be added:
Filters- curses, offensive language, etc.

'''

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
                
                # Try to find a female voice
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.voice_id = voice.id
                        break
                
                temp_engine.stop()
                del temp_engine
                
                print("TTS Engine initialized")
            except Exception as e:
                print(f"Failed to initialize TTS: {e}")
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
            # Run TTS in a separate thread so it doesn't block
            thread = threading.Thread(target=self._speak_thread, args=(text,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def _speak_thread(self, text):
        """Internal method to handle TTS in separate thread"""
        try:
            # Create a NEW engine instance for each speech
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
        """Set speech rate"""
        self.rate = rate
    
    def set_volume(self, volume):
        """Set speech volume (0.0 to 1.0)"""
        self.volume = volume
    
    def toggle(self):
        """Toggle TTS on/off"""
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        print(f"TTS {status}")
        return self.enabled