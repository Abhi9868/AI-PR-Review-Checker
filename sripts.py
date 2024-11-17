import requests
import base64
from urllib.parse import urlparse

from urllib.parse import urlparse

def get_owner_repo(url):
    parsed_url = urlparse(url)
    if not parsed_url.path:
        raise ValueError("Invalid URL: Missing path component")
    path = parsed_url.path.strip("/")  # Remove leading and trailing slashes
    parts = path.split("/")
    if len(parts) < 2:
        return None, None
    
    owner, repo = parts[0], parts[1]
    return owner, repo


def fetch_pr_files(repo_url, pr_number, github_token=None):
    owner, repo = get_owner_repo(repo_url)
    url=f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"token {github_token}",
    } if github_token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_file_content(repo_url, file_path, github_token=None):
    owner, repo = get_owner_repo(repo_url)
    url=f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"token {github_token}",
    } if github_token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    content= response.json()
    return base64.b64decode(content["content"]).decode("utf-8")
    
    
        
