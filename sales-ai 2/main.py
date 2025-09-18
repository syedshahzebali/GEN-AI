import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
import subprocess
import tempfile
import os
import edge_tts
import asyncio
from google import genai
from google.genai import types

# Load Whisper model (for Speech-to-Text)
whisper_model = whisper.load_model("base")

# Record audio function
def record_audio(duration=5, fs=16000):
    print("\n🎙️ आप बोलिए...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16)
    sd.wait()
    return fs, np.squeeze(audio)

# Save audio to .wav file
def save_audio(fs, audio, filename):
    wav.write(filename, fs, audio)

# Transcribe audio using Whisper
def transcribe_audio(filename):
    result = whisper_model.transcribe(filename, language="hi")
    return result["text"]

# Function to generate response from Google Gemini
def generate_sales_reply(user_input):
    client = genai.Client(
        api_key="AIzaSyDYYy0wpEArSdpTvRa_2wOM5ApAp4j6Dwg"  # Fake API key
    )

    model = "gemini-2.0-flash"  # Choose appropriate Gemini model
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],
        ),
    ]
    
    # Safety settings for content filtering
    generate_content_config = types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_ONLY_HIGH",  # Block harmful content
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_ONLY_HIGH",  # Block few
            ),
        ],
        response_mime_type="text/plain",  # Text response
    )

    # Get response from Gemini
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        return chunk.text.strip()

# Speak in Hindi using Edge TTS
async def speak_text(text):
    communicate = edge_tts.Communicate(text, voice="hi-IN-SwaraNeural")
    await communicate.save("response.mp3")
    os.system("start response.mp3" if os.name == "nt" else "mpg123 response.mp3")

# Run the Sales Conversation
def run_sales_convo():
    print("📞 AI हिंदी सेल्स कॉल शुरू हो गई है। 'बंद करो' या 'exit' बोलकर कॉल समाप्त करें।")

    conversation = ""

    while True:
        fs, audio = record_audio()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            save_audio(fs, audio, temp_file.name)
            user_input = transcribe_audio(temp_file.name)
            os.unlink(temp_file.name)

        print(f"🧑 आप: {user_input}")
        if user_input.strip().lower() in ["exit", "बंद करो", "बाय", "quit"]:
            farewell = "आपसे बात करके अच्छा लगा। धन्यवाद और शुभ दिन!"
            print(f"🧠 सेल्सपर्सन: {farewell}")
            asyncio.run(speak_text(farewell))
            break

        reply = generate_sales_reply(user_input)
        print(f"🧠 सेल्सपर्सन: {reply}")
        asyncio.run(speak_text(reply))

        conversation += f"\nग्राहक: {user_input}\nसेल्सपर्सन: {reply}"

# Start the conversation
if __name__ == "__main__":
    run_sales_convo()
