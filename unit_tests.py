from utils import extract_video_id


def run_test():
    urls = [
        "https://www.youtube.com/watch?v=abc123xyz",
        "https://youtu.be/abc123xyz",
        "https://www.youtube.com/embed/abc123xyz",
        "https://www.youtube.com/watch?v=abc123xyz&t=60s",
        "https://www.youtube.com/watch?v=abc123xyz&list=PLabc123xyz",
        "https://www.youtube.com/watch?v=abc123xyz&live=1",
        "https://m.youtube.com/watch?v=abc123xyz",
        # "https://www.youtube.com/watch?feature=player_embedded&v=abc123xyz",
        # "https://www.youtube.com/attribution_link?a=xyz&v=abc123xyz&u=%2Fwatch%3Fv%3Dabc123xyz",
    ]

    for url in urls:
        print(url)
        assert extract_video_id(url) == "abc123xyz"

    print("Tests done!")
