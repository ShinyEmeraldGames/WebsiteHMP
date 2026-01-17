from flask import Flask, session, request, render_template

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'secret'

username = "Derk"

@app.route('/')
def index():
    # Store the username in the session
    session['username'] = username  # Store the username directly in the session
    
    # Retrieve the session ID cookie from the request
    session_id = request.cookies.get('session')
    print("Session ID: ", session_id)

    return f"Session created for user: {session['username']} with Session ID: {session_id}"

if __name__ == '__main__':
    app.run(debug=True)
