from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Marhaba!</h1><p>The Tunis by Night server is running perfectly.</p>"

if __name__ == '__main__':
    # We use port 5001 just in case 5000 is busy
    print("Checking... Server starting on http://127.0.0.1:5001")
    app.run(port=5001)