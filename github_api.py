from github import Github
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)

def fetch_github_data(username):

    user = g.get_user(username)
    repos = user.get_repos()

    languages = {}
    for repo in repos:
        for lang, bytes_count in repo.get_languages().items():
            languages[lang] = languages.get(lang, 0) + bytes_count

    return {
        "username": user.login,
        "repos_count": repos.totalCount,
        "languages": languages,
    }
