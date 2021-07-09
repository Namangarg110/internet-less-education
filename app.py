import base64
import cv2
import flask
from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

##################### AUTH ##########################################
apikey = 'rBzgSxh8n35Dlc7-hTC5UkzydJoXmgsEpfy7_apcGiDQ'
url = 'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/c2d65dda-b9cf-4270-97f8-0ac9c7af013a'
#####################################################################


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Welcome'

@app.route('/<path>')
def speach_to_text(path):
    path = os.path.join('./sample_audio', path)
    authenticator = IAMAuthenticator(apikey)
    stt = SpeechToTextV1(authenticator=authenticator)
    stt.set_service_url(url)
    with open(path, 'rb') as f:
        res = stt.recognize(audio=f, content_type='audio/mp3', model='en-US_NarrowbandModel', continuous=True).get_result()
    return res


@app.route('/<og_img_path>/<res_img_path>/<width>/<height>')
def image_to_String(og_img_path,res_img_path, width = None, height = None, inter = cv2.INTER_AREA):
    width = int(width)
    height = int(height)
    og_img_path  = os.path.join('./images/original_images', og_img_path)
    res_img_path = os.path.join('./images/resized_images', res_img_path)
    og_img = cv2.imread(og_img_path, 0)
    dim = None
    (h, w) = og_img.shape
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    res_img = cv2.resize(og_img, dim, interpolation = inter)
    cv2.imwrite(res_img_path, res_img)
    with open(res_img_path, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    return my_string
    


if __name__ == "__main__":
	app.run(debug=True)

