import requests
import base64
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
    
    
        

def collect_files(url, files=None):
    if files is None:
        files = []

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for item in data:
            if item["type"] == "file":
                files.append({
                    "name": item["name"],
                    "path": item["path"],
                    "download_url": item["download_url"]
                })
            elif item["type"] == "dir":
                collect_files(item["url"], files)  # Recursive call
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    
    return files

if __name__ == "__main__":
    base_url = "https://api.github.com/repos/Abhi9868/AI-PR-Review-Checker/contents/"
    collected_files = collect_files(base_url)
    
    print(f"Total files collected: {len(collected_files)}")
    for file in collected_files:
        print(file)
