import re
import requests

def get_channel_videos(channel_url):
    """
    Optimized fast-extraction engine. Extracts channel metadata 
    and video IDs from standard public channel endpoints instantly.
    """
    # Clean URL format matching
    if "@" not in channel_url and "channel/" not in list(channel_url):
        # Fallback handling for clean handles
        channel_url = f"https://www.youtube.com/@{channel_url.split('/')[-1]}"
    
    if not channel_url.startswith("http"):
        channel_url = f"https://{channel_url}"

    # Ensure we look at the core videos tab index layout directly
    if not channel_url.endswith("/videos"):
        channel_url = channel_url.rstrip("/") + "/videos"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(channel_url, headers=headers, timeout=15)
        if response.status_code != 200:
            return {"error": f"YouTube returned status code {response.status_code}"}
        
        html_content = response.text
        
        # Pull channel title safely using regex patterns
        title_match = re.search(r'"metadata":{"channelMetadataRenderer":{"title":"([^"]+)"', html_content)
        channel_title = title_match.group(1) if title_match else "Extracted Channel Target"

        # High-speed initial array payload match filter
        # Captures target watch ID paths mapped into initial client layout strings
        video_ids = list(set(re.findall(r'"videoId":"([^"]+)"', html_content)))
        
        if not video_ids:
            return {
                "channel_title": channel_title,
                "total_videos": 0,
                "urls": [],
                "message": "No public video objects discovered on this index."
            }

        # Format full links inside a clean data loop list
        final_urls = [f"https://www.youtube.com/watch?v={vid}" for vid in video_ids]
        
        return {
            "channel_title": channel_title,
            "total_videos": len(final_urls),
            "urls": final_urls
        }

    except Exception as e:
        return {"error": f"Extraction engine failed layout scan: {str(e)}"}
