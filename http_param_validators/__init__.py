from pydantic import BaseModel


class HttpTranslateParams(BaseModel):
    video_id: str
    subtitles_lang: str
    translate_lang: str


class HttpSubtitleParams(BaseModel):
    video_id: str
    lang: str


class HttpOptionParams(BaseModel):
    url: str
