from flask import Flask, render_template, request, jsonify, redirect, url_for
import cx_Oracle
import base64
import time

app = Flask(__name__)

# Oracle Database configuration
dsn_tns = cx_Oracle.makedsn('hostname', 'port', sid='sid')  # update as needed
connection = cx_Oracle.connect(user='user', password='password', dsn=dsn_tns)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture')
def capture():
    username = request.args.get('username')
    if not username:
        return redirect(url_for('index'))
    return render_template('capture.html', username=username)

@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.get_json()
    username = data.get('username')
    image_data = data.get('image_data')

    if not username or not image_data:
        return jsonify({"error": "Username and image data are required"}), 400

    # Decode base64 image data
    img_data = base64.b64decode(image_data.split(',')[1])

    try:
        cursor = connection.cursor()
        
        # Insert image data into the database
        timestamp = int(time.time())
        cursor.execute(
            """
            INSERT INTO user_images (id, username, image_data, timestamp)
            VALUES (user_images_seq.NEXTVAL, :username, :image_data, :timestamp)
            """,
            {"username": username, "image_data": img_data, "timestamp": timestamp}
        )
        connection.commit()
        return jsonify({"message": f"Image saved for user {username}"}), 200
    except cx_Oracle.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
