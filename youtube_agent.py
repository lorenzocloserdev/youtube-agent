import os
import sys
import whisper
from pytube import YouTube
from google.generativeai import GenerativeModel
import google.generativeai as genai
from dotenv import load_dotenv
import subprocess

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file.")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)
model = GenerativeModel('gemini-1.5-flash')

def search_youtube(query):
    """
    Search for a video on YouTube and return the first video URL.
    Note: For simplicity, this uses a basic search approach. 
    In a production app, you'd use the official Google API Client.
    """
    print(f"[*] Searching for: {query}...")
    # This is a placeholder for actual API logic. 
    # For now, let's assume the user provides a URL or we use a simplified search.
    # To keep it robust without heavy dependencies, we'll ask for a URL if query is not a URL.
    if "youtube.com" in query or "youtu.be" in query:
        return query
    else:
        print("[-] Simplified search not implemented. Please provide a direct YouTube URL.")
        return None

def download_audio(url):
    """Download audio from YouTube URL."""
    print(f"[*] Downloading audio from {url}...")
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        out_file = audio_stream.download(output_path=".", filename="temp_audio")
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        return new_file
    except Exception as e:
        print(f"[-] Error downloading: {e}")
        return None

def transcribe_audio(audio_path):
    """Transcribe audio using OpenAI Whisper."""
    print("[*] Transcribing (this may take a while)...")
    try:
        # Load the base model (good balance of speed/accuracy)
        whisper_model = whisper.load_model("base")
        result = whisper_model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"[-] Transcription error: {e}")
        return None

def summarize_text(text):
    """Summarize the transcript using Gemini."""
    print("[*] Summarizing with Gemini...")
    prompt = f"""
    Sei un assistente esperto in sintesi di contenuti video. 
    Leggi la seguente trascrizione di un video YouTube e forniscimi un riassunto strutturato in:
    1. Titolo sintetico
    2. Punti chiave (bullet points)
    3. Conclusione/Messaggio principale

    TRASCRIZIONE:
    {text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[-] Summarization error: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_agent.py <YouTube_URL_or_Query>")
        sys.exit(1)

    input_val = sys.argv[1]
    
    # 1. Get URL
    url = search_youtube(input_val)
    if not url:
        return

    # 2. Download
    audio_path = download_audio(url)
    if not audio_path:
        return

    # 3. Transcribe
    transcript = transcribe_audio(audio_path)
    
    # Clean up audio file
    if os.path.exists(audio_path):
        os.remove(audio_path)

    if not transcript:
        return

    # 4. Summarize
    summary = summarize_text(transcript)
    
    if summary:
        print("\n" + "="*50)
        print("RIASSUNTO VIDEO")
        print("="*50)
        print(summary)
        print("="*50)
        
        # Save to file
        with open("summary.txt", "w") as f:
            f.write(summary)
        print("[+] Summary saved to summary.txt")

if __name__ == "__main__":
    main()
