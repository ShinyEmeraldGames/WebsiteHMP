from flask import Flask
from reviews.routes import setup_routes, app  # Adjusted import

# app = Flask(__name__, static_folder='static')


# Set up routes
setup_routes(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
