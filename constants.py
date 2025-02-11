import string

LANG_MAP = {
    "English": "en-IN",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta"
}
SUPPORT_LARGE_MODEL = False
WHISPER_MODEL = "large" if SUPPORT_LARGE_MODEL else "base"
WHISPER_LANGS = LANG_MAP.keys() if SUPPORT_LARGE_MODEL else ["English"]
RESOURCES_DIR = "resources"
STORIES_DIR = "stories"
INVALID_CHARS_PATTERN = r'[<>:"/\\|?*\n]'

AUDIO_FILE_NAME = "audio.mp3"
STORY_FILE_NAME = "story.txt"
WORDS_METADATA_FILE_NAME = "words.json"
LINES_METADATA_FILE_NAME = "lines.json"
VOCAB_DIRECTORY = "vocabulary"

CLEAN_WORD = lambda word: word.lower().strip(string.punctuation)
GET_UNIQUE_WORDS = lambda text: set(CLEAN_WORD(word) for word in text.split())