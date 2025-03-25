 
import telebot  
from gtts import gTTS  
import os  
import requests  
import json  
from flask import Flask  
import threading  

app = Flask(__name__)

@app.route('/')
def home():
    return "X_Misty_Bot is running 24/7!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# ✅ Get API Keys from Secrets
API_TOKEN = os.getenv("API_TOKEN")  
ELEVENLABS_API = os.getenv("ELEVENLABS_API")  

bot = telebot.TeleBot(API_TOKEN)  

# ✅ Language Mapping (Odia Included!)
LANGUAGES = {
    "hi": "Hindi 🇮🇳",
    "en": "English 🇺🇸",
    "bn": "Bengali 🇧🇩",
    "ta": "Tamil 🇮🇳",
    "te": "Telugu 🇮🇳",
    "ur": "Urdu 🇵🇰",
    "mr": "Marathi 🇮🇳",
    "or": "Odia (ଓଡିଆ) 🇮🇳"  # Odia Language Added
}

VOICES = {
    "male": "Matthew",
    "female": "Joanna",
    "deep": "Brian",
    "robotic": "Amy",
    "odia": "Gopal"  # Custom Odia Voice
}

# ✅ Start Message
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "👋 Namaskar! I am **X_Misty_Bot**, your AI voice assistant! 

"
                                      "🎙 Send me any text, and I will convert it into voice! 

"
                                      "🗣 Available Languages: Odia, Hindi, English, Bengali, Tamil, Urdu, Marathi
"
                                      "🔊 Type `/setvoice male/female/deep/robotic/odia` to change voice.")

# ✅ Change Voice Command
current_voice = "odia"

@bot.message_handler(commands=['setvoice'])
def set_voice(message):
    global current_voice
    voice = message.text.split(" ")[1].lower()
    if voice in VOICES:
        current_voice = voice
        bot.send_message(message.chat.id, f"✅ Voice changed to **{voice.capitalize()}**!")
    else:
        bot.send_message(message.chat.id, "❌ Invalid voice! Choose from: male, female, deep, robotic, odia")

# ✅ Convert Text to Speech (Odia Support Added!)
@bot.message_handler(func=lambda message: True)  
def text_to_speech(message):  
    text = message.text  
    if any("଀" <= char <= "୿" for char in text):  # Check if Odia text
        lang_code = "or"
    else:
        lang_code = "hi" if message.text[0] in "अआइईउऊएऐओऔ" else "en"

    # 🏆 Use ElevenLabs API for Ultra-Realistic Voice
    url = "https://api.elevenlabs.io/v1/text-to-speech"
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API
    }
    data = {
        "voice": VOICES[current_voice],
        "text": text
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        filename = "voice.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)

    except:
        # 🆘 If ElevenLabs Fails, Use gTTS
        tts = gTTS(text, lang=lang_code)
        filename = "voice.mp3"
        tts.save(filename)

    with open(filename, "rb") as voice:
        bot.send_voice(message.chat.id, voice)

    os.remove(filename)  

# ✅ Keep Flask Running for 24/7 Uptime
threading.Thread(target=run_flask).start()
bot.polling()
