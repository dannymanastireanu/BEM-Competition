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
    dict={}
    paragraphs = m["text"].split('\n\n')
    text="<div>"
    sumResult=0
    for p in paragraphs:
      print(p)
      #apelat functia pentru paragraf
      dict[p]=0
      sumResult+=0
      text=text+"<div><p>"+p+"</p><label>Result:</label><p>"+str(0)+"</p></div>"
    print(dict)
    text+="</div>"
    return text

if __name__ == '__main__':
  app.run(debug=True)