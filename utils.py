import re

def extract_video_id(url):
    video_id_pattern = (
        r"(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be|m\.youtube\.com|youtube-nocookie\.com)"
        r"(?:/watch\?v=|/embed/|/v/|/live/|/shorts/|/playlist\?v=|/user/[^/]+/|/|/watch\?feature=player_embedded&v=|/watch\?.*v=|/attribution_link\?.*v=|/watch_videos\?.*video_ids=)"
        r"([^#&?\/\s]+)"
    )

    match = re.search(video_id_pattern, url)
    if match:
        return match.group(1)
    else:
        return ""