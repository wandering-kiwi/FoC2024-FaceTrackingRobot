from flask import Flask, render_template
from motors import *

app = Flask(__name__)

stop = False

@app.route('/')
def start():
   return render_template('index.html')

@app.route("/coords/<x>/<y>")
def coords(x, y):
   scaledX = float(x)/320 - 1
   if x == "False" or stop:
       forward(0)
       return
   if scaledX > -0.25:
       print("right")
       right(abs(scaledX)*60)
   elif scaledX < 0.25:
       print("left")
       left(abs(scaledX)*60)
   else:
       forward(0)
   return 'okay'

if __name__=='__main__':
   app.run(debug=True, port=80, host='0.0.0.0', ssl_context='adhoc')
