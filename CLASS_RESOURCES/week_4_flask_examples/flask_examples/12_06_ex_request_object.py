from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main(): 
    if request.method == 'POST':
        return login()
    return render_template("login.html") 

def valid_login(username, password):
    return username == 'Alice' and password == '7'

def login():
    error = None
    username = request.form.get('username')
    password = request.form.get('password')
    
    if valid_login(username, password):
        return render_template('welcome.html', name=username)
    else:
        error = 'Invalid username/password'
    
    return render_template('login.html', error=error)

if __name__ == '__main__': 
    app.run(debug=True)
