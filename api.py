# $~ python3 api.py path_video path_reference_img
# output: verified/notverified, timedout/nottimedout

import requests
import json
import sys

def api_face_match(video, img):
    url = 'http://127.0.0.1:5001/face_match'

    files = {'file1': open(video, 'r'),
             'file2': open(img, 'r')}     
    resp = requests.post(url, files=files)

    return json.dumps(resp.json())
    
if __name__ == '__main__':
    api_face_match(sys.argv[1], sys.argv[2])