import re

def extract_video_id(url):
    video_id_pattern = r"^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|shorts\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*"

    match = re.search(video_id_pattern, url)
    if match:
        return match.group(1)
    else:
        return ""