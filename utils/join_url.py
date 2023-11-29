def join_url(*args: str) -> str:
    return "/".join(map(lambda x: x.strip("/\\"), args))
