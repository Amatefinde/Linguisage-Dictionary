from os.path import join


def write_one(data: bytes, filedir: str, filename) -> None:
    with open(join(filedir, filename), "wb") as file:
        file.write(data)


def write_many(payload: dict[str, bytes], filedir: str) -> None:
    """
    Payload should be a dict where each key is a filename (str),
    and each value is a bytes object
    Filedir is a path to directory where files are will write
    """
    for filename, data in payload.items():
        write_one(data, filedir, filename)
