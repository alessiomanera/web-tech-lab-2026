from flask import Flask

app = Flask(__name__)

@app.route("/<name>")
def hello_you(name):
    return "<html><head></head><body><p>Hello, {} </p></body></html>".format(name)

if __name__ == "__main__":
    app.run(debug=True)
