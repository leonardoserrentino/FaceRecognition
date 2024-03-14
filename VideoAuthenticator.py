import cv2
from deepface import DeepFace
from test import test  
from flask import Flask, request
import json  

def verification(video, img):
    cap = cv2.VideoCapture(video)
    reference_img = img
    counter = 0

    face_match = False
    verifylog = False

    while counter<300:
        ret, frame = cap.read()

        if ret:
            if counter % 30 == 0:
                label = test(image=frame, model_dir='resources/anti_spoof_models', device_id=0)
                if int(label)==1:
                    try:
                        verifylog = DeepFace.verify(frame, reference_img)
                        face_match = verifylog["verified"]
                    except ValueError:
                        face_match = False

            counter = counter + 1

            if face_match:
                break
            cv2.imshow("video", frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    timed_out = (counter >= 299)
    
    # Data to be written
    dictionary = {
        "verified": str(face_match),
        "timed_out": str(timed_out)
    }

    json_object = json.dumps(dictionary, indent=4)
    with open("outcome.json", "w") as outfile:
        outfile.write(json_object)
    if verifylog:
        with open("log.log", "w") as logfile:
            logfile.write(str(verifylog))
    
    return dictionary, verifylog


app = Flask(__name__)

@app.route('/face_match', methods=['POST'])
def face_match():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('video' in request.files) and ('img' in request.files):        
            video = request.files.get('video')
            img = request.files.get('img') 

            outcome, verifylog = verification(video, img)  

            outcomeJson = json.dumps(outcome)
            logJson = json.dumps(verifylog)

            return outcomeJson, logJson       
    
app.run(host='0.0.0.0', port='5001', debug=True)
