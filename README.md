# Project_MEI_AI_VTuber

Project MEI is an AI-powered VTuber that interacts with Twitch viewers in real-time. 
Inspired by Vedal who programed the AI Vtuber on Twutch, Neruo-sama, this project demonstrates the integration of large language models, real-time chat processing, 
and character animation to create an engaging streaming experience. 

## Features
1. Real-time AI responses using Claude API
2. Custom personality
3. Twitch chat integration with message queue system
4. Automated lip-sync animation via VTube Studio API
5. Text-to-speech voice synthesis
6. Auto-reconnection handling for stable streaming

## Tech Stack
**Core Technologies**
-Language: Python 3.x
-AI/ML: Claude API (Anthropic Sonnet 4)
-Framework: asyncio for asynchronous processing

**APIs & Libraries**

-TwitchIO 2.9.1 - Twitch chat integration
-pyvts - VTube Studio WebSocket API
-pyttsx3 - Text-to-speech engine
-python-dotenv - Environment configuration

**Tools & Platforms**

-VTube Studio - Live2D character rendering
-OBS Studio - Stream broadcasting (Optional)
-Git - Version control

## Running it
**Prerequisites**
What you need installed:

-Python 3.8 or higher
-VTube Studio
-OBS Studio (optional, for streaming)
-Twitch account
-Claude API key (or OpenAI API key)

Installation

Clone the repository

```bash
   git clone https://github.com/yourusername/project-muei.git
   cd project-muei
```
Create virtual environment

bash   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate

Install dependencies

bash   pip install -r requirements.txt

Set up environment variables
Copy .env.example to .env:

bash   cp .env.example .env
Fill in your credentials:
env   TWITCH_TOKEN=your_oauth_token
   TWITCH_CLIENT_ID=your_client_id
   TWITCH_CLIENT_SECRET=your_client_secret
   TWITCH_BOT_ID=your_bot_id
   TWITCH_CHANNEL=your_channel_name
   
   ANTHROPIC_API_KEY=your_claude_api_key

Get Twitch credentials

OAuth Token: https://twitchtokengenerator.com/
Client ID/Secret: https://dev.twitch.tv/console/apps
Bot ID: https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/


Set up VTube Studio

Open VTube Studio
Go to Settings → General Settings
Enable "Start API"
Note the port (default: 8001)


Running the Project

Start VTube Studio (must be running first)
Run the bot

bash   python main.py

Test in Twitch chat

Go to your Twitch channel
Type: hey muei, how are you?
The bot should respond!
