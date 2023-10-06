import requests

if __name__ == '__main__':
    img_url = "http://sns-img-qc.xhscdn.com/be16c4bf-db73-3fd4-893d-ac323babb8f9"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    r = requests.get(img_url, headers)

    if r.ok:
        with open("img.png", "wb") as f:
            f.write(r.content)
