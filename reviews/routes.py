from flask import Flask, render_template, request, redirect, url_for
from reviews import app
import os
import uuid

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

#@app.route('/test')
#def test():
    # return app.send_static_file('test.html')
#    return render_template('login.html')

@app.route('/view_image')
def test():
    # return app.send_static_file('view_image.html')
    return render_template('view_image.html')

def setup_routes(app):
    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        uploaded_image = None
        if request.method == 'POST':
            file = request.files['image']
            print("Allowed File: ", allowed_file(file.filename))
            if file and allowed_file(file.filename):
                unique_id = str(uuid.uuid4())
                filename = f"{unique_id}_{file.filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                uploaded_image = filename  # Save the filename to display later
                return redirect(url_for('view_image', image_id=unique_id, image_name = uploaded_image))
                # return redirect(url_for('view_image', image_id=uploaded_image))
        return render_template('upload.html')

    @ app.route('/image/<image_id>')
    def view_image(image_id):
        uploaded_images = os.listdir(app.config['UPLOAD_FOLDER'])

        # Debug: Print available images
        print(f"Available images: {uploaded_images}")

        # Construct the expected filename based on the image_id
        image_name = next((img for img in uploaded_images if img.startswith(image_id)), None)

        # Debug: Print the name that is being looked for
        print(f"Looking for image with ID {image_id}: Found {image_name}")

        if image_name:
            return render_template('view_image.html', image_name=image_name)

        return "Image not found", 404


def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

if __name__ == "__main__":
    app.run()