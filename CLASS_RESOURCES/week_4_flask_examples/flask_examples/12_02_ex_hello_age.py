from flask import Flask
app = Flask(__name__)

@app.route("/<int:age>")
def hello_you(age):
    return "<html><head></head><body><p>Hello, I am {} years old.</p></body></html>".format(age)

if __name__ == "__main__":
    app.run(debug=True)
