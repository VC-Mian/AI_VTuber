"""
VTuber Controller Module - Handles VTube Studio API integration

This module controls:
- Connection to VTube Studio via WebSocket
- Lip-sync animation during speech
- Auto-reconnection if connection drops
- Future: Facial expressions and emotions

OPTIONAL: Bot works without VTube Studio. If not connected, it will skip animation.
"""

import asyncio
import pyvts

class VTuberController:
    """Controls VTube Studio model for lip-sync and expressions"""
    
    def __init__(self):
        self.vts = None
        self.connected = False
        self.plugin_name = "AI VTuber Bot"  # CUSTOMIZE: Your bot's name
        self.plugin_developer = "YourName"  # CUSTOMIZE: Your name
        self.reconnecting = False
        
    async def connect(self):
        """Connect to VTube Studio"""
        try:
            self.vts = pyvts.vts(
                plugin_info={
                    "plugin_name": self.plugin_name,
                    "developer": self.plugin_developer,
                    "authentication_token_path": "token.txt"
                },
                port=8001  # Default VTube Studio API port
            )
            
            await self.vts.connect()
            await self.vts.request_authenticate_token()
            await self.vts.request_authenticate()
            
            self.connected = True
            self.reconnecting = False
            print("✓ Connected to VTube Studio!")
            return True
            
        except Exception as e:
            print(f"⚠ Failed to connect to VTube Studio: {e}")
            print("  Bot will continue without VTube Studio animation.")
            print("  Make sure VTube Studio is running with API enabled!")
            self.connected = False
            return False
    
    async def reconnect(self):
        """Attempt to reconnect to VTube Studio"""
        if self.reconnecting:
            return
        
        self.reconnecting = True
        print("[VTUBER] Connection lost, attempting to reconnect...")
        
        try:
            if self.vts:
                await self.vts.close()
        except:
            pass
        
        await asyncio.sleep(1)
        await self.connect()
    
    async def trigger_mouth_open(self, duration=0.5):
        """
        Open mouth for lip-sync effect
        
        Args:
            duration: How long to keep mouth open (seconds)
        """
        if not self.connected:
            return
        
        try:
            # Trigger mouth open parameter
            await self.vts.request(
                self.vts.vts_request.requestSetParameterValue(
                    parameter="MouthOpen",
                    value=1.0
                )
            )
            
            # Wait for duration
            await asyncio.sleep(duration)
            
            # Close mouth
            await self.vts.request(
                self.vts.vts_request.requestSetParameterValue(
                    parameter="MouthOpen",
                    value=0.0
                )
            )
        except Exception as e:
            print(f"[VTUBER] Error controlling mouth: {e}")
            self.connected = False
            await self.reconnect()

    async def simulate_talking(self, text):
        """
        Simulate talking animation based on text length
        
        Args:
            text: The text being spoken (used to calculate duration)
        """
        # If not connected, try to reconnect
        if not self.connected and not self.reconnecting:
            await self.reconnect()
        
        # If still not connected, skip animation
        if not self.connected:
            print("[VTUBER] Not connected, skipping animation")
            return
        
        # Estimate speaking duration based on word count
        word_count = len(text.split())
        duration = word_count / 2.5  # ~2.5 words per second
        
        # Animate mouth opening/closing
        try:
            intervals = int(duration * 4)  # Open/close 4 times per second
            for i in range(intervals):
                if not self.connected:
                    print("[VTUBER] Connection lost during animation")
                    break
                
                await self.trigger_mouth_open(0.125)
                await asyncio.sleep(0.125)
                
        except Exception as e:
            print(f"[VTUBER] Error during talking animation: {e}")
            self.connected = False
            await self.reconnect()
    
    async def disconnect(self):
        """Disconnect from VTube Studio"""
        if self.vts:
            try:
                await self.vts.close()
            except:
                pass
            self.connected = False
            print("Disconnected from VTube Studio")