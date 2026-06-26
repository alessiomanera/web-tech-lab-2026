from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello/<value>')

def hello(value=None):
    return render_template('home.html', name=value)

if __name__ == '__main__': 
	app.run(debug=True)