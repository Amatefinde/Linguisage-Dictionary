import os
from os.path import join
from pprint import pprint
from typing import Any

from loguru import logger
from sqladmin import ModelView
from sqlalchemy.orm import selectinload
from starlette.requests import Request

from core.database import db_helper
from core.database.models import Word, Sense, Alias, Example


def _get_all_field_names(model) -> list[str]:
    return list(model.__table__.c.keys())


class WordAdmin(ModelView, model=Word):
    column_list = [Word.aliases, Word.word, Word.id, Word.senses]
    can_view_details = True
    column_searchable_list = [Word.word]
    column_sortable_list = _get_all_field_names(Word)

    async def delete_model(self, request: Request, pk: Any) -> None:
        async with db_helper.session_factory() as db_session:
            db_word = await db_session.get(
                Word,
                int(pk),
                options=[
                    selectinload(Word.word_images),
                    selectinload(Word.senses),
                    selectinload(Word.senses, Sense.sense_images),
                ],
            )
            for image in db_word.word_images:
                image_path = join("static", "word_images", image.img)
                os.remove(image_path)
            for sense in db_word.senses:
                for image in sense.sense_images:
                    image_path = join("static", "sense_images", image.img)
                    os.remove(image_path)
        await super().delete_model(request, pk=pk)


class SenseAdmin(ModelView, model=Sense):
    column_list = [Sense.word] + _get_all_field_names(Sense) + [Sense.examples]
    can_view_details = True
    column_sortable_list = _get_all_field_names(Sense)
    column_default_sort = ("id", True)
    column_searchable_list = [Sense.definition]

    async def delete_model(self, request: Request, pk: Any) -> None:
        async with db_helper.session_factory() as db_session:
            db_sense = await db_session.get(
                Sense, int(pk), options=[selectinload(Sense.sense_images)]
            )
            for image in db_sense.sense_images:
                image_path = join("static", "sense_images", image.img)
                os.remove(image_path)
        await super().delete_model(request, pk=pk)


class AliasAdmin(ModelView, model=Alias):
    column_list = _get_all_field_names(Alias)
    can_view_details = True
    column_sortable_list = _get_all_field_names(Alias)
    column_default_sort = ("id", True)
    column_searchable_list = [Alias.alias]


class ExampleAdmin(ModelView, model=Example):
    column_list = [column.name for column in Example.__table__.c.values()]
    can_view_details = True
    column_sortable_list = [column.name for column in Example.__table__.c.values()]
    column_default_sort = ("id", True)
    column_searchable_list = [Example.example]
