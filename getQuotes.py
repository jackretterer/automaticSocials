from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from constants import GET_QUOTES_PROMPT  # Import the constant
import csv  # Import the csv module
import json  # Import json to parse the quotes
import os  # Import os to handle file paths
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import subprocess  # Import subprocess for executing ffmpeg command
import shlex
import textwrap
import cv2
import numpy as np

client = OpenAI()
print("Current working directory:", os.getcwd())

def get_transcript(url: str, language: str = 'en'):
    video_id = url.split('v=')[-1].split('&')[0]  # Extract video ID from URL
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return transcript
    except Exception as e:
        return str(e)  # Return the error message if transcript retrieval fails

def get_quotes(transcript):
    concatenated_transcript = ' '.join(line['text'] for line in transcript if line['text'].strip())
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                { "role": "system", "content": GET_QUOTES_PROMPT },
                {
                    "role": "user",
                    "content": concatenated_transcript,
                },
        ],
    );
    concatenated_quotes = completion.choices[0].message.content
    return concatenated_quotes

def create_spreadsheet(quotes_json, filename='quotes.csv'):
    quotes = json.loads(quotes_json)  # Parse the JSON string into a Python object
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Index', 'Title', 'Quote'])  # Write the header
        for index, quote in enumerate(quotes, start=1):
            writer.writerow([index, quote['title'], quote['quote']])  # Write each quote

def select_background_video(quote: str):
    video_directory = os.path.join(os.getcwd(), 'videos')  # Get the videos directory
    video_files = os.listdir(video_directory)  # List all video files in the directory
    
    # Use LLM to choose the most relevant video based on the quote
    video_titles = [os.path.splitext(video)[0] for video in video_files]  # Extract titles without extensions
    prompt = f"Choose the most relevant video title for the quote: '{quote}' from the following titles: {video_titles}. Only respond with the title. Do not include any other text. Just the title."
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    
    selected_video_title = completion.choices[0].message.content.strip()
    print(selected_video_title)
    selected_video = next((video for video in video_files if selected_video_title in video), None)
    
    return os.path.join(video_directory, selected_video) if selected_video else None

def select_background_audio(quote: str):
    audio_directory = os.path.join(os.getcwd(), 'audioSamples')  # Get the audioSamples directory
    audio_files = os.listdir(audio_directory)  # List all audio files in the directory
    
    # Use LLM to choose the most relevant audio based on the quote
    audio_titles = [os.path.splitext(audio)[0] for audio in audio_files]  # Extract titles without extensions
    prompt = f"Choose the most relevant audio title for the quote: '{quote}' from the following titles: {audio_titles}. Only respond with the title. Do not include any other text. Just the title."
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    
    selected_audio_title = completion.choices[0].message.content.strip()
    print(f"Selected audio: {selected_audio_title}")
    selected_audio = next((audio for audio in audio_files if selected_audio_title in audio), None)
    
    return os.path.join(audio_directory, selected_audio) if selected_audio else None

def create_video_from_quote(quote: str, video_path: str, audio_path: str, output_path: str):
    # Open the video file
    video = VideoFileClip(video_path)
    
    # Open the audio file
    audio = AudioFileClip(audio_path)
    
    # If the audio is shorter than the video, loop the audio
    if audio.duration < video.duration:
        audio = audio.loop(duration=video.duration)
    else:
        # If the audio is longer than the video, clip the audio
        audio = audio.subclip(0, video.duration)
    
    # Set the audio of the video to the adjusted audio
    video = video.set_audio(audio)
    
    # Calculate the width and height of the video
    width, height = video.w, video.h
    
    # Calculate the max width of the text box (90% of video width)
    max_text_width = int(width * 0.9)
    
    # Calculate the max font size (10% of video width)
    font_size = int(width * 0.05)
    
    # Wrap the text to fit within the max width
    wrapped_text = textwrap.fill(quote, width=30)  # Adjust width as needed
    
    # Create a function to generate text clip with background
    def create_text_clip(color, opacity=1):
        txt = TextClip(wrapped_text, fontsize=font_size, color=color, font='Arial-Bold', 
                       size=(max_text_width, None), method='caption')
        txt = txt.set_position('center').set_duration(video.duration)
        if opacity < 1:
            txt = txt.set_opacity(opacity)
        return txt

    # Create the background and foreground text clips
    txt_bg = create_text_clip('black', opacity=0.5)
    txt_fg = create_text_clip('white')

    # Create a single clip that combines background and foreground
    txt_clip = CompositeVideoClip([txt_bg, txt_fg])
    txt_clip = txt_clip.set_position('center')

    # Combine the clips
    final_clip = CompositeVideoClip([video, txt_clip])
    
    # Write the result to a file
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    # Close the clips to free up system resources
    video.close()
    audio.close()
    final_clip.close()

def get_video_id(url: str) -> str:
    return url.split('v=')[-1].split('&')[0]

# Example usage
if __name__ == "__main__":
    quotes_file = 'quotes.json'  # Assuming quotes are stored in a JSON file
    base_output_directory = 'output_videos'  # Base directory for all output videos

    url = 'https://www.youtube.com/watch?v=gG25Kq_3gmg&ab_channel=TheCounselingGroupPL'
    video_id = get_video_id(url)
    
    # Create a specific output directory for this video
    output_directory = os.path.join(base_output_directory, video_id)
    os.makedirs(output_directory, exist_ok=True)

    transcript = get_transcript(url)  # Change language as needed
    quotes = json.loads(get_quotes(transcript))
    print(quotes)

    for quote in quotes:
        video_path = select_background_video(quote['quote'])
        audio_path = select_background_audio(quote['quote'])
        print("Video path: ", video_path)
        print("Audio path: ", audio_path)
        if video_path and audio_path:
            output_path = os.path.join(output_directory, f"{quote['title']}.mp4")
            create_video_from_quote(quote['quote'], video_path, audio_path, output_path)
