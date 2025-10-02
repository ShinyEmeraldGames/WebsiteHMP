from flask import Flask, render_template
from reviews import app

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run()