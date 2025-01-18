from github import Github
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import math

# GitHub token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)

def fetch_repo_languages(repo):

    ## Fetch language data for a single repository.
    ## Normalize language usage to calculate the percentage of each language in the repo.

    try:
        repo_languages = repo.get_languages()
        total_bytes = sum(repo_languages.values())
        if total_bytes > 0:
            # Normalize language usage (percentage of total bytes in the repo)
            return {lang: bytes_count / total_bytes for lang, bytes_count in repo_languages.items()}
        return {}
    except Exception as e:
        print(f"Error fetching languages for {repo.full_name}: {e}")
        return {}

def fetch_github_data(username):

    # Fetch GitHub user data with multithreaded language fetching and apply a weighted algorithm.

    user = g.get_user(username)
    repos = list(user.get_repos())  # Convert to a list for iteration
    language_weights = {}
    repo_counts = {}

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor() as executor:
        future_to_repo = {executor.submit(fetch_repo_languages, repo): repo for repo in repos}

        for future in as_completed(future_to_repo):
            repo = future_to_repo[future]
            try:
                repo_languages = future.result()
                for lang, percentage in repo_languages.items():
                    # Sum percentages for each language across repositories
                    language_weights[lang] = language_weights.get(lang, 0) + percentage
                    repo_counts[lang] = repo_counts.get(lang, 0) + 1
            except Exception as e:
                print(f"Error processing {repo.full_name}: {e}")

    # Apply the weighted algorithm: Calculate the geometric mean for each language
    geometric_mean_languages = {}
    for lang, total_percentage in language_weights.items():
        # Avoid division by zero
        if repo_counts[lang] > 0:
            geometric_mean_languages[lang] = math.pow(total_percentage, 1 / repo_counts[lang])

    # Sort by geometric mean and take the top 10 languages
    sorted_languages = dict(sorted(geometric_mean_languages.items(), key=lambda x: x[1], reverse=True)[:10])

    return {
        "username": user.login,
        "repos_count": len(repos),
        "languages": sorted_languages,
    }
