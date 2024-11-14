import json
import logging

from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi

from unit_tests import run_test
from utils import extract_video_id

app = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d [%(threadName)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


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
    if not url:
        return http_400_error("'url' parameter is missing")

    logger.info("url=%s", url)
    video_id = extract_video_id(url)
    if not video_id or len(video_id) == 0:
        return http_400_error("Cannot extract video ID")
    logger.info("video_id=%s", video_id)

    list_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript_options = []
    for transcript in list_transcripts:
        option = TranscriptOption(transcript.video_id, transcript.language, transcript.language_code, transcript.is_generated, transcript.is_translatable, transcript.translation_languages)
        transcript_options.append(option)
        logger.debug(repr(option))
        # print()
    return json.dumps([option.__dict__ for option in transcript_options]), 200, {'Content-Type': 'application/json'}


def http_400_error(error_message):
    return {"status": "error", "message": error_message}, 400, {'Content-Type': 'application/json'}


@app.route('/api/v1/subtitles', methods=['GET'])
def get_subtitles():
    video_id = request.args.get('video_id')
    lang = request.args.get('lang')

    if not video_id:
        return http_400_error("'video_id' parameter is missing")
    if not lang:
        return http_400_error("'lang' parameter is missing")

    logger.info("video_id=%s, lang=%s", video_id, lang)
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])

    all_text = " ".join(item["text"] for item in transcript)
    return {"transcript": all_text}, 200, {'Content-Type': 'application/json'}

@app.route('/api/v1/subtitles/translates', methods=['GET'])
def get_translates():
    video_id = request.args.get('video_id')
    subtitles_lang = request.args.get('subtitles_lang')
    translate_lang = request.args.get('translate_lang')

    list_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = list_transcripts.find_transcript([subtitles_lang])
    translated_transcript = transcript.translate(translate_lang)
    translated = translated_transcript.fetch()

    all_text = " ".join(item["text"] for item in translated)
    return {"transcript": all_text}, 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    run_test()
    app.run(host='0.0.0.0', port=5000, debug=True)
