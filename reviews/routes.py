from flask import Flask, render_template, request, redirect, url_for
from reviews import app, db, Images, Users, Comments
from datetime import datetime, timezone
import os
import uuid
from sqlalchemy import text, Column, DateTime
from sqlalchemy.exc import SQLAlchemyError

@app.route('/')
def home():
    cookie = request.cookies.get('name')
    return render_template('home.html', cookie=cookie)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        message = ""
        message_category = ""
        
        print("Username: ", username)
        print("Password: ", password)
        
        if username is None or isinstance(username,str) is False or len(username) < 3:
            message = "Invalid username format"
            message_category = "danger"
            return render_template("login.html", message=message, category=message_category)
        
        if password is None or isinstance(password,str) is False or len(password) < 3:
            print("something wrong2")
            message = "Invalid password format"
            message_category = "danger"
            return render_template("login.html", message=message, category=message_category)
        
        qstmt = f"select * from users where username='{username}' and password='{password}'"
        print(qstmt)
        result = db.session.execute(text(qstmt))
        user = result.fetchall()
    
        if not user:
            print("something wrong3")
            message=f"Username or password wrong."
            message_category="danger"
            return render_template("login.html", message=message, category=message_category)
        
        print("forwarding")
        print("Login successfull")
        resp = redirect('/')
        resp.set_cookie('name', username)
        return resp
    
    return render_template("login.html", cookie=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get('email_address')
        username = request.form.get('Username')
        password = request.form.get('Password')
        password_repeat = request.form.get('Password Repeat')
        message = ""
        message_category = "" 
        
        print("Email: ", email)
        print("Username: ", username)
        print("Password: ", password)
        print("Password repeat: ", password_repeat)
        
        if username is None or isinstance(username,str) is False or len(username) <= 3:
            message = "Invalid username format"
            message_category = "danger"
            return render_template("register.html", message=message, category=message_category)
        
        if password is None or isinstance(password,str) is False or len(password) <= 3:
            message = "Invalid password format"
            message_category = "danger"
            return render_template("register.html", message=message, category=message_category)
        
        if password_repeat is None or isinstance(password_repeat,str) is False or len(password_repeat) <= 3:
            message = "Invalid password format"
            message_category = "danger"
            return render_template("register.html", message=message, category=message_category)
        
        if email is None or isinstance(email, str) is False and not email_exists_in_db(email):
            print("Something wrong4")
            message = "Invalid email format"
            message_category = "danger"
            return render_template("register.html", message=message, category=message_category)
        
        if password != password_repeat:
            message = "Passwords do not match"
            message_category = "danger"
            return render_template("register.html", message=message, category=message_category)
        
        qstmt = f"INSERT INTO users (username, password, email_address) VALUES ('{username}', '{password}', '{email}');" # query statement
        print(qstmt)
        db.session.execute(text(qstmt))
        try:
            db.session.commit()
            print("commit")
        except SQLAlchemyError as e:
            db.session.rollback()
            print("rollback")
            return render_template("register.html")
    
        print("forwarding")
        print("Register successfull")
        resp = redirect('register') # wo alles drinsteht aus der db
        return resp
        
    return render_template('register.html', cookie=None)

@app.route('/view_image')
def test():
    cookie = request.cookies.get('name')
    if not request.cookies.get('name'):
        return redirect(url_for('view_image'), cookie=None)
    return render_template('view_image.html', cookie=cookie)

@app.route('/logout')
def logout():
    resp = redirect('/') # wo alles drinsteht aus der db
    resp.set_cookie('name', '', expires=0)
    return resp

def setup_routes(app):
    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        cookie = request.cookies.get('name')
        if not request.cookies.get('name'):
            return redirect(url_for('upload'), cookie=None)
        uploaded_image = None
        if request.method == 'POST':
            file = request.files['image']
            print("Allowed File: ", allowed_file(file.filename))
            if file and allowed_file(file.filename):
                unique_id = str(uuid.uuid4())
                filename = f"{unique_id}_{file.filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                uploaded_image = filename  # Save the filename to display later
                
                # get user_id based on cookie
                qstmt_userid = f"select id from users where username='{cookie}' LIMIT 1;"
                result = db.session.execute(text(qstmt_userid))
                print(result)
                
                user_id = None
                for row in result:
                    user_id = row[0]  # Get the first column value from the row

                # Make sure user_id is not None and convert it to an integer
                if user_id is not None:
                    user_id = int(user_id)  # Convert to integer only if valid
                else:
                    raise ValueError("No user found")
                
                print("Cookie:", cookie)
                qstmt_username = f"select username from users where id='{user_id}';"
                print(qstmt_username)
                username = db.session.execute(text(qstmt_username))
                new_image = Images(
                    user_id=user_id,
                    image_url=filename,
                )
                db.session.add(new_image)
                db.session.commit()  # Commit the changes to the database

                # Redirect to the view image page
                return redirect(url_for('view_image', image_id=new_image.id, image_name=filename))
            
                # return redirect(url_for('view_image', image_id=unique_id, image_name = uploaded_image, cookie=cookie))
                # return redirect(url_for('view_image', image_id=uploaded_image))
        return render_template('upload.html', cookie=cookie)

    @ app.route('/image/<image_id>', methods=['GET', 'POST'])
    def view_image(image_id):
        cookie = request.cookies.get('name')
        uploaded_images = os.listdir(app.config['UPLOAD_FOLDER'])
        if request.method == 'POST':
            rating = request.form['rating']
            comment = request.form['comment']
            
            # get user_id based on cookie
            qstmt_userid = f"select id from users where username='{cookie}' LIMIT 1;"
            result = db.session.execute(text(qstmt_userid))
            print(result)
            
            user_id = None
            for row in result:
                user_id = row[0]

            # Make sure user_id is not None and convert it to an integer
            if user_id is not None:
                user_id = int(user_id)
            else:
                raise ValueError("No user found")
            
            print("Cookie:", cookie)
            qstmt_username = f"select username from users where id='{user_id}';"
            print(qstmt_username)
            username = db.session.execute(text(qstmt_username))
            
            new_comment = Comments(
                image_id = image_id,
                user_id = user_id,
                comment_text = comment,
                rating = rating
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('view_image', image_id=image_id))  # Redirect to clear form

        # Debug: Print available images
        print(f"Available images: {uploaded_images}")

        # Construct the expected filename based on the image_id
        image_name = next((img for img in uploaded_images if img.startswith(image_id)), None)

        # Debug: Print the name that is being looked for
        print(f"Looking for image with ID {image_id}: Found {image_name}")

        if image_name:
            # Fetch comments for the image
            comments_query = f"SELECT rating, comment_text FROM comments WHERE image_id='{image_id}';"
            comments_result = db.session.execute(text(comments_query))
            
            # Extract comments
            comments = [{'rating': row[0], 'comment': row[1]} for row in comments_result]

            return render_template('view_image.html', image_name=image_name, cookie=cookie, comments=comments)

        return "Image not found", 404

@app.route('/feed', methods=['POST', 'GET'])
def feed():
    cookie = request.cookies.get('name')
    message = ""
    message_category = ""
    
    if request.method == 'GET':
        username = request.args.get('Search_Button')

        if username is not None:
            images_query = f"""
                SELECT i.id, i.image_url, i.upload_date, i.rating
                FROM images i
                JOIN users u ON i.user_id = u.id
                WHERE u.username = '{username}';
            """
            
            images_result = db.session.execute(text(images_query))
            images = images_result.fetchall()
            
            if images:
                message = f"Search successful: {images}"
                message_category = "successful"

            images_by_user = [
                {'id': row[0], 'url': row[1], 'upload_date': row[2], 'average_rating': row[3]} 
                for row in images
            ]
            
            return render_template('feed.html', images=images, message=message, message_category=message_category, cookie=cookie)

    return render_template('feed.html', message=message, message_category=message_category, cookie=None)

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def email_exists_in_db(email):
    result = db.execute("SELECT COUNT(*) FROM users WHERE email_address = ?", (email,)).fetchone()
    return result[0] > 0

if __name__ == "__main__":
    app.run()