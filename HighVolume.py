import os
import time
import json
import random

import requests
from PIL import Image

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

if __name__ == '__main__':
    count = 0
    cache = []

    note_visited = r"T:\DataStore\note_visited_by_image_original.json"

    if os.path.exists(note_visited):
        with open(note_visited, mode='r', encoding='utf-8') as file:
            cache = json.load(file)
            print(f"Loaded: {cache}")

    note_page_root = r"T:\DataStore\raw\api\sns\v1\note\feed"

    for note_id in os.listdir(note_page_root):
        time_start = time.time()
        img_size = 0

        if note_id in cache:
            print(f"[Note] Existed: {note_id}")
            continue

        file_path = fr'{note_page_root}\{note_id}\{note_id}.json'
        if os.path.exists(file_path):
            with open(file_path, mode='r', encoding='utf-8') as file:
                json_data = json.load(file)
                for item in json_data:
                    if 'note_list' in item.keys():
                        for note in item['note_list']:
                            if 'images_list' in note.keys():
                                for img in note['images_list']:
                                    img_id = img['fileid']

                                    target_file = fr"T:\DataStore\image_original\{img_id}.jpg"
                                    if os.path.exists(target_file):
                                        try:
                                            im = Image.open(target_file)
                                            im.verify()
                                            im.close()
                                            print(f"[Image] Verified and Skipped: {img_id}.jpg")
                                            continue
                                        except Exception as e:
                                            print(e)
                                            pass

                                    img_url = f"{img['original']}"
                                    try:
                                        with requests.get(img_url, headers) as r:
                                            print(f"[Image] Requested: {img_url}")

                                            if r.ok:
                                                with open(fr"T:/DataStore/image_original/{img_id}.jpg", "wb") as f:
                                                    f.write(r.content)
                                                    img_size += len(r.content)
                                                    print(f"[Image] Downloaded: {img_id}.jpg")
                                            else:
                                                print(r.content)
                                    except:
                                        print(f"[Image] Error and Skipped: {img_url}")
                                        continue

        cache.append(note_id)
        print(f"[Note] Visited: {note_id}")

        count += 1

        if count == 100:
            with open(note_visited, "w", encoding='UTF-8') as file:
                json.dump(
                    cache,
                    file,
                    indent=4,
                    ensure_ascii=False
                )
            count = 0

        num = random.randint(200, 1000) * 0.001
        time.sleep(num)
        print(f"[Info] Slept: {num} s")

        time_interval = time.time() - time_start

        print(f"[Info] Rate: {(img_size / time_interval) / (1024 * 1024)} MB/s")
