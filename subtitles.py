import json

from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi

from unit_tests import run_test
from utils import extract_video_id

app = Flask(__name__)


class TranscriptOption:
    def __init__(self, video_id, language, language_code, is_generated, is_translatable, translation_languages):
        self.video_id = video_id
        self.language = language
        self.language_code = language_code
        self.is_generated = is_generated
        self.is_translatable = is_translatable
        self.available_translations = translation_languages

    def __repr__(self):
        return str(self.__dict__)


@app.route('/api/v1/subtitles/options', methods=['GET'])
def get_options():
    url = request.args.get('url')

    if url:
        print("Получен URL:", url)
        video_id = extract_video_id(url)
        list_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

        transcript_options = []
        for transcript in list_transcripts:
            option = TranscriptOption(transcript.video_id, transcript.language, transcript.language_code, transcript.is_generated, transcript.is_translatable, transcript.translation_languages)
            transcript_options.append(option)
            print(repr(option))
        return json.dumps([option.__dict__ for option in transcript_options]), 200, {'Content-Type': 'application/json'}
    else:
        return {"status": "error", "message": "URL parameter is missing"}, 400, {'Content-Type': 'application/json'}


@app.route('/api/v1/subtitles', methods=['GET'])
def get_subtitles():
    video_id = request.args.get('video_id')
    lang = request.args.get('lang')

    if video_id and lang:
        print("Запрос:", video_id, lang)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        all_text = " ".join(item["text"] for item in transcript)
        return {"transcript": all_text}, 200, {'Content-Type': 'application/json'}
    else:
        return {"status": "error", "message": "URL parameter is missing"}, 400, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    run_test()
    app.run(host='0.0.0.0', port=5000, debug=True)
