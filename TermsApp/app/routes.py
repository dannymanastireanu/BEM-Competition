from flask import Flask, render_template, request, jsonify
import json  
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')
  
@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/check/terms', methods=['POST'])
def check():
    m = request.json
    print(m["url"])
    print(m["text"])
    return m["url"]+m["text"]


if __name__ == '__main__':
  app.run(debug=True)