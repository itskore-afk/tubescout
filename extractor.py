import re
import requests

def extract_urls(channel_url):
"""
Extract video URLs from a YouTube channel.
"""

```
# Handle @username format
if "@" not in channel_url and "channel/" not in channel_url:
    channel_url = f"https://www.youtube.com/@{channel_url.split('/')[-1]}"

if not channel_url.startswith("http"):
    channel_url = f"https://{channel_url}"

if not channel_url.endswith("/videos"):
    channel_url = channel_url.rstrip("/") + "/videos"

headers = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(
    channel_url,
    headers=headers,
    timeout=15
)

if response.status_code != 200:
    raise Exception(
        f"YouTube returned status code {response.status_code}"
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
```
