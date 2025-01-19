from flask import Flask, render_template, request, url_for, jsonify
from github_api import fetch_github_data
from graph_generator import generate_skill_matrix
import sqlite3
import json
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
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache (
                username TEXT PRIMARY KEY,
                data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    conn.commit()
    conn.close()

# Call the init_db function when the app starts
init_db()

# Helper function: Get cached data
def get_cached_data(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    result = cursor.execute("SELECT data FROM cache WHERE username = ?", (username,)).fetchone()
    conn.close()
    if result:
        return json.loads(result["data"])
    return None

# Helper function: Save data to cache
def save_to_cache(username, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO cache (username, data) VALUES (?, ?)", (username, json.dumps(data)))
    conn.commit()
    conn.close()



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        action = request.form.get("action", "generate")
        color = request.form.get("color", "magenta") # default to magenta
        opacity = float(request.form.get("opacity", "1.0")) #Default to full opacity
        size = request.form.get("size", "medium") # Default to medium size

        # Check cache first
        cached_data = get_cached_data(username)
        if cached_data:
            user_data = cached_data
            graph_regenerated = False
        else:
            # Fetch data from GitHub and save to cache
            try:
                user_data = fetch_github_data(username)
                save_to_cache(username, user_data)
                graph_regenerated = True
            except Exception as e:
                return render_template("index.html", error=f"Error fetching data for user '{username}': {e}", graph=False)

        # user_data = fetch_github_data(username)

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

# Helper function: Get DB connection
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

@app.route("/api/skill_matrix/<username>", methods=["GET"])
def get_skill_matrix(username):

    ##This is a REST API Endpoint: Fetch the skill matrix for a given GitHub username
    try:
        user_data = fetch_github_data(username) ##fetch data using our github-api function

        #check if user have public repo
        if user_data["repo_count"] == 0:
            return jsonify({"error": "No public repositories found for this user."}), 404

        #The Json response
        response = {
            "username": user_data["username"],
            "skills": user_data["languages"], ##Skills and their weighted scores
            "repo_count": user_data["repo_count"],
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=int(port))
