from flask import Flask, render_template, request, jsonify

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds
import numpy as np

app = Flask(__name__)

def load_model(filename):
    hubies_model = "https://hub.tensorflow.google.cn/google/tf2-preview/nnlm-en-dim128/1"
    hub_layer = hub.KerasLayer(hubies_model, output_shape=[128], input_shape=[],
                               dtype=tf.string, trainable=True)
    model = tf.keras.models.load_model(filename, custom_objects={'KerasLayer': hub_layer})
    return model


model = load_model("./model-057.h5")

comunity_help = []

print("Success load the model")

def choose_color(predicted_value):
    if predicted_value >= 0.6:
        return 'green'
    elif predicted_value <= 0.4:
        return 'red'
    else:
        return 'gray'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/help_us')
def help_us():
    return render_template('help_us.html')

@app.route('/help', methods=['POST'])
def help_submit():
    m = request.form
    comunity_help.append({'tc': m["terms"], 'option': m["optionTm"]})
    print(comunity_help)
    return render_template('home.html')



@app.route('/check/terms', methods=['POST'])
def check():
    m = request.json
    dict = {}
    paragraphs = m["text"].split('\n\n')
    text = "<div>"
    sumResult = 0
    i = 0
    for p in paragraphs:
        # print(p)
        # apelat functia pentru paragraf
        i += 1
        dict[p] = 0
        phrases = p.split('.')
        print(len(phrases))
        if (len(phrases) >= 2):
            less = '.'.join(phrases[:1]) + ". "
            more = '.'.join(phrases[1:])
        else:
            less = phrases[0] + ". "
            more = ""
        print(more)
        print(p)
        predicted_value = model.predict(np.array([p]))[0][0] * 100
        sumResult += predicted_value
        text = text + "<div><p>" + less + "<span id=\"dots" + str(
            i) + "\">...</span><span style=\"display: none;\"id=\"more" + str(
            i) + "\">" + more + "</br>Result:</br>" + str(round(predicted_value, 4)) + "%" + "</span></p></div><button onclick=\"myFunction(this)\" id=\"myBtn_" + str(i) + "\">Read more</button>"

    # print(dict)
    final_result = sumResult / i
    text += "</div>"
    return text + '<p style="color:' + choose_color(final_result) + ';"> Termenii si conditiile sunt convenabile in proportie de: ' + str(round(final_result, 4)) + '%</p>'


if __name__ == '__main__':
    app.run()

