from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    print("Handling request to home page.2")
    return "Hello, Azure!"
