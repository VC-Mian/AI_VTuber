#!/usr/bin/env python3
"""
Project Muei - AI VTuber Bot
Entry point for the application
"""

import sys
from src.config import Config
from src.chat_reader import Bot

def main():
    """Main entry point"""
    print("=" * 50)
    print("PROJECT MUEI - AI VTUBER BOT")
    print("=" * 50)
    
    try:
        # Validate configuration
        Config.validate()
        print("✓ Configuration validated")
        
        # Create and run the bot
        bot = Bot()
        print("✓ Bot initialized")
        print("\nStarting bot... Press Ctrl+C to stop")
        print("=" * 50)
        
        bot.run()
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        print("Refer to .env for the required configuration.")
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nShutting down Muei bot...")
        print("Goodbye! 👋")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()