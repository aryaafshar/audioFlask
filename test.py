import os
from flask import Flask,redirect

app = Flask(__name__)

@app.route('/')
def hello():
    return redirect("http://127.0.0.1:5000/result", code=302)
#new line
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)