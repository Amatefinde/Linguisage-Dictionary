from loguru import logger
from sqladmin import ModelView

from core.database.models import Word, Sense, Alias, Example


def _get_all_field_names(model) -> list[str]:
    return list(model.__table__.c.keys())


class WordAdmin(ModelView, model=Word):
    column_list = [Word.id, Word.word, Word.senses, Word.aliases]
    can_view_details = True


class SenseAdmin(ModelView, model=Sense):
    column_list = _get_all_field_names(Sense) + [Sense.word]
    can_view_details = True
    column_sortable_list = _get_all_field_names(Sense)
    column_default_sort = ("id", True)


class AliasAdmin(ModelView, model=Alias):
    column_list = _get_all_field_names(Alias)
    can_view_details = True
    column_sortable_list = _get_all_field_names(Alias)
    column_default_sort = ("id", True)


class ExampleAdmin(ModelView, model=Example):
    column_list = [column.name for column in Example.__table__.c.values()]
    can_view_details = True
    column_sortable_list = [column.name for column in Example.__table__.c.values()]
    column_default_sort = ("id", True)
