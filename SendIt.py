import requests

if __name__ == '__main__':
    data = {
        'id': "image",
        'url': "http://sns-img-hw.xhscdn.com/1000g00824mhtqhkfi0104aq7uq5uk8qkve3rik8"
    }

    response = requests.post(url='http://localhost:21564', json=data)
