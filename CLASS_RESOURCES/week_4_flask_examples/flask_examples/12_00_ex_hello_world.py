from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<html><head></head><body><p>Hello World!</p></body></html>"

if __name__ == "__main__":
    app.run(debug=True)
