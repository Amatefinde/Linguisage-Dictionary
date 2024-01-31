from typing import NewType, Literal

level_type = NewType("lvl", Literal["A1", "A2", "B1", "B2", "C1", "C2"])
main_pos = ["noun", "verb", "adjective", "adverb"]
main_pos_type = NewType("part_of_speech", Literal[*main_pos])
