def join_url(*args):
    return "/".join(map(lambda x: x.strip("/\\"), args))
