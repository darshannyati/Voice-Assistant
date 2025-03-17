import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai

# Initialize OpenAI Client
def setup_openai_client(api_key):
    return openai.OpenAI(api_key=api_key)

# Transcribe audio to text using OpenAI Whisper
def transcribe_audio(client, audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcript.text

# Get AI response from OpenAI GPT
def fetch_ai_response(client, input_text):
    messages = [{"role": "user", "content": input_text}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return response.choices[0].message.content

# Convert text to speech (TTS)
def text_to_audio(client, text, audio_path):
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=text
    )
    with open(audio_path, "wb") as f:
        f.write(response.content)

# Streamlit UI
def main():
    st.sidebar.title("API KEY CONFIGURATION")
    api_key = st.sidebar.text_input("Enter your API key", type="password")

    st.title("🎙️ Nyati 💬")
    st.write("Hi there! Click on the voice recorder to interact with me. How can I assist you today?")

    if api_key:
        client = setup_openai_client(api_key)

        recorded_audio = audio_recorder()
        if recorded_audio:
            audio_file = "audio.mp3"
            with open(audio_file, "wb") as f:
                f.write(recorded_audio)

            transcribed_text = transcribe_audio(client, audio_file)
            st.write("Transcribed Text:", transcribed_text)

            ai_response = fetch_ai_response(client, transcribed_text)
            st.write("AI Response:", ai_response)

            response_audio_file = "audio_response.mp3"
            text_to_audio(client, ai_response, response_audio_file)
            st.audio(response_audio_file)

if __name__ == "__main__":
    main()
