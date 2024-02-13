import os
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

client = openai.OpenAI()

def get_video_id(url):
    if 'youtu.be' in url:
        return url.split('/')[-1]
    elif 'youtube.com' in url:
        return url.split('v=')[-1].split('&')[0]

def fetch_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([t['text'] for t in transcript_list])
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def summarize_transcript(transcript):
    response = client.completions.create(
      model="gpt-3.5-turbo",
      prompt=f"Summarize the following transcript into bullet points:\n\n{transcript}",
      temperature=0.5,
      max_tokens=300,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )

    summary_text = response.choices[0].text.strip()
    return summary_text

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python summarize_youtube_openai.py <YouTube URL>")
        sys.exit(1)

    video_url = sys.argv[1]
    video_id = get_video_id(video_url)
    transcript = fetch_transcript(video_id)
    
    if transcript:
        summary = summarize_transcript(transcript)
        print("Summary:\n", summary)
    else:
        print("Failed to fetch transcript.")

