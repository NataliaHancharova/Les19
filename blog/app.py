from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('home.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.execute("SELECT * FROM comments WHERE post_id = %s", (post_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('post.html', post=post, comments=comments)

@app.route('/create', methods=('GET', 'POST'))
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    return render_template('create_post.html')

@app.route('/post/<int:post_id>/edit', methods=('GET', 'POST'))
def edit_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (title, content, post_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('post', post_id=post_id))

    cursor.close()
    conn.close()
    return render_template('create_post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=('POST',))
def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home'))

@app.route('/post/<int:post_id>/comment', methods=('POST',))
def add_comment(post_id):
    author = request.form['author']
    content = request.form['content']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (post_id, author, content) VALUES (%s, %s, %s)", (post_id, author, content))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('post', post_id=post_id))

if __name__ == '__main__':
    app.run(debug=True)

