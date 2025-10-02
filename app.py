from flask import Flask
from reviews import app, routes

if __name__ == "__main__":
    app.run(debug=True)