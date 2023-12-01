def split_on_batches(array: list, batch_size=5) -> list[list]:
    return [
        array[i : i + batch_size] for i in range(0, len(array), batch_size)
    ]
