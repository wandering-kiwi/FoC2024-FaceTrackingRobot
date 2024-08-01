from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def start():
   return render_template('index.html')

@app.route("/coords/<x>/<y>")
def coords(x, y):
   print(x, y)
   return 'okay'

if __name__=='__main__':
   app.run(debug=True, port=80, host='0.0.0.0', ssl_context='adhoc')