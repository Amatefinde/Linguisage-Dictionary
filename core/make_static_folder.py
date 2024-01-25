import os
from core.config import settings
from os.path import join
from pathlib import Path


def make_static_folder():
    home_dictionary = Path(os.path.dirname(__file__)).parent
    os.chdir(home_dictionary)

    if not os.path.exists(settings.STATIC_PATH):
        os.mkdir(settings.STATIC_PATH)
    if not os.path.exists(join(settings.STATIC_PATH, "word_images")):
        os.mkdir(join(settings.STATIC_PATH, "word_images"))
    if not os.path.exists(join(settings.STATIC_PATH, "sense_images")):
        os.mkdir(join(settings.STATIC_PATH, "sense_images"))
    if not os.path.exists(join(settings.STATIC_PATH, "word_audio")):
        os.mkdir(join(settings.STATIC_PATH, "word_audio"))
