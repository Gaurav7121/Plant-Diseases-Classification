import os
from uuid import uuid4
import pickle
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)
# app = Flask(__name__, static_folder="images")

#Loading Key:Value Pair
key_list = pickle.load(open('key_list', 'rb'))
val_list = pickle.load(open('val_list', 'rb'))

#Creating a path to upload Images
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#Creating a path to home page
@app.route("/")
def index():
    return render_template("index.html")

#Creating a path to Upload.
@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
        #import tensorflow as tf
        import numpy as np
        from keras.preprocessing import image

        from keras.models import load_model
        new_model = load_model('AlexNetModel.hdf5')

        new_model.summary()
        test_image = image.load_img(destination,target_size=(224,224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        test_image = test_image/255
        result = new_model.predict(test_image)
        ans = np.argmax(result)
        print(ans)
        ans = key_list[val_list.index(ans)]
        print(ans)
            
    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("template.html",image_name=filename, text=ans)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(debug=False)
