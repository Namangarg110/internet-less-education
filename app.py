import base64
import cv2
import flask
from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route('/<width>/<height>')
def image_to_String(width = None, height = None, inter = cv2.INTER_AREA):
    width = int(width)
    height = int(height)
    og_img_path = "2.jpg"
    res_img_path = "2new.jpg"
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


if __name__ == '__main__':
    app.run(debug=True)
