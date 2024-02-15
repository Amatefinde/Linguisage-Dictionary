import asyncio
from collections_auto_downloader import find_many_and_save_to_db

my_list = ["Roach", "dwdwddw", "Winds"]

asyncio.run(find_many_and_save_to_db(my_list))
