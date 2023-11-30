"""add tables: word, sense, image, example, row_example

Revision ID: a132a194116a
Revises: 73403aef9650
Create Date: 2023-11-30 17:59:50.803995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a132a194116a"
down_revision: Union[str, None] = "73403aef9650"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "word",
        sa.Column("word", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sense",
        sa.Column(
            "lvl",
            sa.Enum("A1", "A2", "B1", "B2", "C1", "C2", native_enum=False),
            nullable=True,
        ),
        sa.Column("definition", sa.String(), nullable=False),
        sa.Column("short_cut", sa.String(), nullable=True),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["word_id"],
            ["word.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "example",
        sa.Column("sense_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["sense_id"],
            ["sense.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "image",
        sa.Column("img", sa.String(), nullable=False),
        sa.Column("sense_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["sense_id"],
            ["sense.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "row_example",
        sa.Column("sense_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["sense_id"],
            ["sense.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("row_example")
    op.drop_table("image")
    op.drop_table("example")
    op.drop_table("sense")
    op.drop_table("word")
    # ### end Alembic commands ###