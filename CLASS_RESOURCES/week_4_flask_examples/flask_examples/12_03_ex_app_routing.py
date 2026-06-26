from flask import Flask 

app = Flask(__name__) 

@app.route('/') 
def index(): 
    return "<html><head></head><body>This is the homepage</body></html>"

@app.route('/hello') 
def hello(): 
    return "<html><head></head><body>Hello</body></html>"

@app.route('/user/<username>') 
def show_user(username): 
    return "<html><head></head><body>My name is {}.</body></html>".\
        format(username)

@app.route('/age/<int:age>') 
def show_post(age): 
    return "<html><head></head><body>I am {} years old.</body></html>".\
        format(age)

if __name__ == "__main__": 
    app.run(debug=True)