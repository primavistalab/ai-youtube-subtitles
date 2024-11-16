import json
import logging
import os

from flask import Flask, request
from pydantic_core import ValidationError
from youtube_transcript_api import YouTubeTranscriptApi, CouldNotRetrieveTranscript

from db_logger import db_write_request
from http_param_validators import HttpTranslateParams, HttpSubtitleParams, HttpOptionParams
from http_utils import http_400_error
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
    db_write_request(request)
    try:
        url_param = HttpOptionParams(**request.args)
    except ValidationError as e:
        return http_400_error(e.errors())

    video_id = extract_video_id(url_param.url)
    if not video_id or len(video_id) == 0:
        return http_400_error("Cannot extract video ID")

    try:
        list_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    except CouldNotRetrieveTranscript as e:
        return http_400_error(e.cause)

    transcript_options = []
    for transcript in list_transcripts:
        option = TranscriptOption(transcript.video_id, transcript.language, transcript.language_code, transcript.is_generated, transcript.is_translatable, transcript.translation_languages)
        transcript_options.append(option)
    return json.dumps([option.__dict__ for option in transcript_options]), 200, {'Content-Type': 'application/json'}


@app.route('/api/v1/subtitles', methods=['GET'])
def get_subtitles():
    db_write_request(request)
    try:
        translate_params = HttpSubtitleParams(**request.args)
    except ValidationError as e:
        return http_400_error(e.errors())

    try:
        raw_subtitles = (YouTubeTranscriptApi
                         .get_transcript(translate_params.video_id, languages=[translate_params.lang]))
    except CouldNotRetrieveTranscript as e:
        return http_400_error(e.cause)

    subtitles = " ".join(item["text"] for item in raw_subtitles)
    return {"subtitles": subtitles}, 200, {'Content-Type': 'application/json'}


@app.route('/api/v1/subtitles/translates', methods=['GET'])
def get_translates():
    db_write_request(request)
    try:
        translate_params = HttpTranslateParams(**request.args)
    except ValidationError as e:
        return http_400_error(e.errors())

    try:
        translated = (YouTubeTranscriptApi
                      .list_transcripts(translate_params.video_id)
                      .find_transcript([translate_params.subtitles_lang])
                      .translate(translate_params.translate_lang)
                      .fetch())
    except CouldNotRetrieveTranscript as e:
        return http_400_error(e.cause)

    transcript = " ".join(item["text"] for item in translated)
    return {"translate": transcript}, 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        run_test()
    app.run(host='0.0.0.0', port=5000, debug=True)
