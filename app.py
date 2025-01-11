from flask import Flask, render_template, request, url_for
from github_api import fetch_github_data
from graph_generator import generate_skill_matrix
import sqlite3
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        user_data = fetch_github_data(username)

        # Check if the user has public repositories
        if user_data["repos_count"] == 0:
            return render_template("index.html", error="No public repositories found for this user.", graph=False)

        # Generate the skill matrix graph for the specific user
        interactive_filename = f"static/{username}_skill_graph.html"
        static_filename = f"static/{username}_skill_graph.png"
        generate_skill_matrix(user_data["languages"], static_filename, interactive_filename)

        # Generate a unique URL for both version of graph
        interactive_graph_url = url_for("static", filename=f"{username}_skill_graph.html")
        static_graph_url = url_for("static", filename=f"{username}_skill_graph.png")

        # Save or update user graph data in the database
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO users (username, graph_url)
            VALUES (?, ?)
            ON CONFLICT(username) DO UPDATE SET graph_url = excluded.graph_url
        """, (username, interactive_graph_url))
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
        )
    return render_template("index.html", graph=False)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


if __name__ == "__main__":
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=int(port))
