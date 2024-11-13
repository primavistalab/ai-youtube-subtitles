from utils import extract_video_id


def run_test():
    urls = [
        "https://youtube.com/shorts/dQw4w9WgXcQ?feature=share",
        "//www.youtube-nocookie.com/embed/dQw4w9WgXcQ?rel=0",
        "http://www.youtube.com/user/Scobleizer#p/u/1/dQw4w9WgXcQ",
        "http://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=channel",
        "http://www.youtube.com/watch?v=dQw4w9WgXcQ&playnext_from=TL&videos=osPknwzXEas&feature=sub",
        "http://www.youtube.com/ytscreeningroom?v=dQw4w9WgXcQ",
        "http://www.youtube.com/user/SilkRoadTheatre#p/a/u/2/dQw4w9WgXcQ",
        "http://youtu.be/dQw4w9WgXcQ",
        "http://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be",
        "http://youtu.be/dQw4w9WgXcQ",
        "http://www.youtube.com/user/Scobleizer#p/u/1/dQw4w9WgXcQ?rel=0",
        "http://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=channel",
        "http://www.youtube.com/watch?v=dQw4w9WgXcQ&playnext_from=TL&videos=osPknwzXEas&feature=sub",
        "http://www.youtube.com/ytscreeningroom?v=dQw4w9WgXcQ",
        "http://www.youtube.com/embed/dQw4w9WgXcQ?rel=0",
        "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "http://youtube.com/v/dQw4w9WgXcQ?feature=youtube_gdata_player",
        "http://youtube.com/vi/dQw4w9WgXcQ?feature=youtube_gdata_player",
        "http://youtube.com/?v=dQw4w9WgXcQ&feature=youtube_gdata_player",
        "http://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtube_gdata_player",
        "http://youtube.com/?vi=dQw4w9WgXcQ&feature=youtube_gdata_player",
        "http://youtube.com/watch?v=dQw4w9WgXcQ&feature=youtube_gdata_player",
        "http://youtube.com/watch?vi=dQw4w9WgXcQ&feature=youtube_gdata_player",
        "http://youtu.be/dQw4w9WgXcQ?feature=youtube_gdata_player"
    ]

    for url in urls:
        video_id = extract_video_id(url)
        print(f"Testing... url='{url}', extracted video_id='{video_id}'")
        assert video_id == "dQw4w9WgXcQ"

    print("Tests done!")
