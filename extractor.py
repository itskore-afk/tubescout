import sys
import subprocess
import json

def run_extractor():
    if len(sys.argv) < 2:
        print("Error: Missing target link parameter.")
        return

    channel_url = sys.argv[1]
    
    # Clean up common variants to make sure yt-dlp parses the video feed smoothly
    if "/videos" not in channel_url and "/shorts" not in channel_url and "/streams" not in channel_url:
        # Check if it's a handle style link
        if "@" in channel_url:
            base_url = channel_url.split("?")[0]
            channel_url = f"{base_url}/videos"

    try:
        # Run yt-dlp to rapidly extract video data in flat-playlist JSON format
        command = [
            'yt-dlp',
            '--flat-playlist',
            '--dump-single-json',
            '--playlist-end', '100',  # Grabs up to the first 100 videos for optimal speed
            channel_url
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        playlist_data = json.loads(result.stdout)
        
        if 'entries' in playlist_data:
            for entry in playlist_data['entries']:
                if entry and 'id' in entry:
                    # Construct a pristine, clickable watch link for the interface
                    print(f"https://www.youtube.com/watch?v={entry['id']}")
                    
    except Exception as e:
        # Fallback just in case standard extraction faces network blocks
        print(f"Error executing live extraction: {str(e)}")

if __name__ == '__main__':
    run_extractor()
