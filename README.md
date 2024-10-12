# YouTube Quote Video Generator

This project extracts quotes from YouTube videos and creates short video clips for each quote, combining relevant background video and audio.

## Prerequisites

Before running this script, make sure you have the following installed:

- Python 3.7+
- FFmpeg
- ImageMagick (`brew install imagemagick` on macOS)

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install the required Python packages:
   ```
   pip install openai youtube_transcript_api moviepy cv2 numpy
   ```

3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

1. Prepare your input:
   - Ensure you have background videos in the `videos` directory.
   - Place background audio files in the `audioSamples` directory.

2. Run the script:
   ```
   python main.py
   ```

3. When prompted, enter the YouTube URL of the video you want to process.

4. The script will:
   - Extract the transcript from the YouTube video
   - Generate quotes using GPT-4
   - Create a CSV file with the quotes
   - Generate video clips for each quote, selecting relevant background video and audio
   - Save the output videos in the `output_videos/<video_id>` directory

## Configuration

- Modify the `GET_QUOTES_PROMPT` in `constants.py` to adjust how quotes are extracted.
- Adjust video generation parameters in the `create_video_from_quote` function.

## File Structure

- `main.py`: The main script
- `constants.py`: Contains the prompt for quote extraction
- `videos/`: Directory for background videos
- `audioSamples/`: Directory for background audio files
- `output_videos/`: Directory where generated videos are saved

## Notes

- This script uses the OpenAI API, which may incur costs. Make sure you understand the pricing before running the script.
- The script uses GPT-4 for quote extraction and content matching. Ensure your OpenAI account has access to this model.

## Troubleshooting

If you encounter issues with video or audio processing, make sure ImageMagick are correctly installed and accessible in your system's PATH.