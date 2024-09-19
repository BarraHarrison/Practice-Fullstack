from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlalchemy
import pymysql

app = Flask(__name__)
CORS(app)


db = sqlalchemy.create_engine("mariadb+pymysql://root@localhost:3306/practiceDB", echo=True)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/comments', methods=['GET'])
def get_comments():
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT * FROM comments;"))
        comments = result.fetchall()  
        return jsonify([dict(row) for row in comments])


@app.route('/comments', methods=['POST'])
def add_comment():
    
    data = request.json
    username = data['username']
    comment_text = data['comment_text']


    
    with db.connect() as conn:
        conn.execute(sqlalchemy.text("""
            INSERT INTO comments (comment_id, username, comment_text)
            VALUES (NULL, :username, :comment_text);
        """), {
            "username": username,
            "comment_text": comment_text
        })
        
    return jsonify({"message": "Comment added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
