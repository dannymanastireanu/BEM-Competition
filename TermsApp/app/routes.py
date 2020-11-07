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
    i=0
    for p in paragraphs:
      #print(p)
      #apelat functia pentru paragraf
      i+=1
      dict[p]=0
      sumResult+=0
      phrases=p.split('.')
      print(len(phrases))
      if(len(phrases)>=2):
        less = '.'.join(phrases[:1])+". "
        more = '.'.join(phrases[1:])
      else:
        less = phrases[0]+". "
        more=""
      print(more)
      text=text+"<div><p>"+less+"<span id=\"dots"+str(i)+"\">...</span><span style=\"display: none;\"id=\"more"+str(i)+"\">"+more+"</br>Result:</br>"+str(0)+"</span></p></div><button onclick=\"myFunction(this)\" id=\"myBtn_"+str(i)+"\">Read more</button>"
    #print(dict)
    text+="</div>"
    return text

if __name__ == '__main__':
  app.run(debug=True)