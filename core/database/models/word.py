from core.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sense import Sense


class Word(Base):
    word: Mapped[str]

    senses: Mapped[list["Sense"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
