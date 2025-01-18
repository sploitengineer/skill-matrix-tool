from flask import Flask, render_template, request, url_for
from github_api import fetch_github_data
from graph_generator import generate_skill_matrix
import sqlite3
import os

##Reminder this is only for Render. Normally just initialize init_db.py on local testing
# Initialize the database and create the table if it doesn't exist
def init_db():
    conn = sqlite3.connect('database.db')  # Database file
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            graph_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call the init_db function when the app starts
init_db()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        action = request.form.get("action", "generate")
        color = request.form.get("color", "magenta") # default to magenta
        opacity = float(request.form.get("opacity", "1.0")) #Default to full opacity
        size = request.form.get("size", "medium") # Default to medium size

        user_data = fetch_github_data(username)

        # Check if the user has public repositories
        if user_data["repos_count"] == 0:
            return render_template("index.html", error="No public repositories found for this user.", graph=False)

        # Generate the skill matrix graph for the specific user
        interactive_filename = f"static/{username}_skill_graph.html"
        static_filename = f"static/{username}_skill_graph.png"
        generate_skill_matrix(user_data["languages"], static_filename, interactive_filename, color, opacity, size)

        # Generate a unique URL for both versions of the graph
        interactive_graph_url = url_for("static", filename=f"{username}_skill_graph.html")
        static_graph_url = url_for("static", filename=f"{username}_skill_graph.png")

        # Save/update user graph data in the database
        conn = get_db_connection()
        user_data_db = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user_data_db:
            conn.execute("UPDATE users SET graph_url = ? WHERE username = ?", (interactive_graph_url, username))
        else:
            conn.execute("INSERT INTO users (username, graph_url) VALUES (?, ?)", (username, interactive_graph_url))
        conn.commit()
        conn.close()

        # Generate the Markdown snippet for embedding
        markdown_snippet = f"![Skill Matrix](https://skill-matrix-tool.onrender.com{static_graph_url})"

        return render_template(
            "index.html",
            username=username,
            graph=True,
            static_graph_url=static_graph_url,
            interactive_graph_url=interactive_graph_url,
            markdown_snippet=markdown_snippet,
            existing=bool(user_data_db)  # Indicating if the graph is being regenerated
        )


    return render_template("index.html", graph=False)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


if __name__ == "__main__":
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=int(port))
