from logging import debug
from flask import Flask, request, render_template, redirect, url_for
import tensorflow
from tensorflow.keras.models import load_model
from skimage.transform import resize
import matplotlib.pyplot as plt
import os
import numpy as np
from werkzeug.utils import redirect, secure_filename

UPLOAD_FOLDER = "./static/images/UPLOAD_FOLDER"

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


model = load_model("model.h5")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# def upload_file(file):
#         if file and allowed_file(file.filename):
#             filename = secure_filename('image')
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


def resize_img(image):
    img = plt.imread(image)
    resize_image = resize(img, (32, 32, 3))
    return resize_image


@app.route("/", methods=["GET"])
def show_predict_page():
    return render_template("home.html")


@app.route("/", methods=["POST"])
def show_predict_result():
    if request.files:
        image = request.files["fileUpload"]
        # filename = secure_filename(image.filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], "image.jpg"))
        resize_i = resize_img(image)
        predictions = model.predict(np.array([resize_i]))
        list_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        x = predictions

        for i in range(10):
            for j in range(10):
                if x[0][list_index[i]] > x[0][list_index[j]]:
                    temp = list_index[i]
                    list_index[i] = list_index[j]
                    list_index[j] = temp

        classification = [
            "airplane",
            "automobile",
            "bird",
            "cat",
            "deer",
            "dog",
            "frog",
            "horse",
            "ship",
            "truck",
        ]
        result = classification[list_index[0]]
    # for i in range(len(classification)):
    #     result.append(classification[list_index[i]])
    #     print(result)
    # result = result[0]
    return render_template("home.html", result=result, image=image)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='images/UPLOAD_FOLDER/' + filename), code=301)


# def print_date_time():
#    print(time.strftime("%A,%d.%B %Y %I:%M:%S %p"))
if __name__ == "__main__":
    app.run()
