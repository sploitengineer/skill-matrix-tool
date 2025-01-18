from github import Github
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# GitHub token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)

def fetch_repo_languages(repo):
    ## Fetch language data for a single repository.
    try:
        return repo.get_languages()
    except Exception as e:
        print(f"Error fetching languages for {repo.full_name}: {e}")
        return {}

def fetch_github_data(username):
    ##Fetch GitHub user data with multithreaded language fetching.
    user = g.get_user(username)
    repos = list(user.get_repos())  # Convert to a list for iteration
    languages = {}

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor() as executor:
        future_to_repo = {executor.submit(fetch_repo_languages, repo): repo for repo in repos}

        for future in as_completed(future_to_repo):
            repo = future_to_repo[future]
            try:
                repo_languages = future.result()
                for lang, bytes_count in repo_languages.items():
                    languages[lang] = languages.get(lang, 0) + bytes_count
            except Exception as e:
                print(f"Error processing {repo.full_name}: {e}")

    return {
        "username": user.login,
        "repos_count": len(repos),
        "languages": languages,
    }