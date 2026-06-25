import re
import requests


def extract_urls(channel_url):
    """
    Extract video URLs from a YouTube channel.
    """

    if "@" not in channel_url and "channel/" not in channel_url:
        channel_url = f"https://www.youtube.com/@{channel_url.split('/')[-1]}"

    if not channel_url.startswith("http"):
        channel_url = f"https://{channel_url}"

    if not channel_url.endswith("/videos"):
        channel_url = channel_url.rstrip("/") + "/videos"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(
        channel_url,
        headers=headers,
        timeout=15
    )

    html = response.text

    video_ids = list(
        set(
            re.findall(
                r'"videoId":"([^"]+)"',
                html
            )
        )
    )

    return [
        f"https://www.youtube.com/watch?v={vid}"
        for vid in video_ids
    ]

