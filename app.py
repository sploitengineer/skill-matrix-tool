from flask import Flask, render_template, request, url_for
from github_api import fetch_github_data
from graph_generator import generate_skill_matrix
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
        filename = f"static/{username}_skill_graph.png"
        generate_skill_matrix(user_data["languages"], filename)

        # Generate a unique URL for the graph
        graph_url = url_for("static", filename=f"{username}_skill_graph.png")

        # Generate the Markdown snippet for embedding
        markdown_snippet = f"![Skill Matrix](https://skill-matrix-tool.onrender.com{graph_url})"

        return render_template(
            "index.html",
            username=username,
            graph=True,
            graph_url=graph_url,
            markdown_snippet=markdown_snippet,
        )
    return render_template("index.html", graph=False)

if __name__ == "__main__":
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=int(port))
