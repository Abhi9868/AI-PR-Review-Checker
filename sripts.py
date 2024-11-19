# import requests
import base64
# from urllib.parse import urlparse
from groq import Groq

key='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'

def analyze_code_with_llm(file_content,file_name):
    prompt=f"""
         Aalyze the following code for :
         - code style and formatting issues
         - potential bugs and errors
         - performance improvements
         - best practices
    
    File : {file_name}
    Content: {file_content}
    
    provide a detailed json output with structure"
    {{
            "issues":[
                {{
                "type":"<style|error|performance|best_practice>",
                "line": <line_number>,
                "description": "<description>",
                "suggestion": "<suggestion>"
            }}
            ]
    }}
    ```json
    """
    
    client = Groq(api_key=key)
    completion=client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{
            "role":"user",
            "content":prompt
        }],
        temperature=1,
        top_p=1,
    )
    print(completion.choices[0].message.content)  

code_str="ZnJvbSBmYXN0YXBpIGltcG9ydCBGYXN0QVBJLHN0YXR1cwpmcm9tIHB5ZGFu\ndGljICBpbXBvcnQgQmFzZU1vZGVsCmZyb20gdHlwaW5nIGltcG9ydCBPcHRp\nb25hbAoKYXBwID0gRmFzdEFQSSgpCgpjbGFzcyBBbmFseXplUFJSZXF1ZXN0\nKEJhc2VNb2RlbCk6CiAgICByZXBvX3VybDogc3RyCiAgICBwcl9udW1iZXI6\nIGludAogICAgZ2l0aHViX3Rva2VuOiBPcHRpb25hbFtzdHJdID0gTm9uZQoK\nQGFwcC5wb3N0KCIvc3RhcnRfdGFzay8iKQphc3luYyBkZWYgc3RhcnRfdGFz\na19lbmRwb2ludCh0YXNrX3JlcXVlc3Q6IEFuYWx5emVQUlJlcXVlc3QpOgog\nICAgZGF0YT17CiAgICAgICAgInJlcG9fdXJsIjp0YXNrX3JlcXVlc3QucmVw\nb191cmwsCiAgICAgICAgInByX251bWJlciI6dGFza19yZXF1ZXN0LnByX251\nbWJlciwKICAgICAgICAiZ2l0aHViX3Rva2VuIjp0YXNrX3JlcXVlc3QuZ2l0\naHViX3Rva2VuCiAgICB9CiAgICBwcmludChkYXRhKQogICAgcmV0dXJuIHsi\ndGFza19pZCI6ICIxMjM0IiwgInN0YXR1cyI6ICJ0YXNrIHN0YXJ0ZWQifQoK\n" 

analyze_code_with_llm((base64.b64decode(code_str).decode("utf-8")),"script.py")

# def get_owner_repo(url):
#     parsed_url = urlparse(url)
#     if not parsed_url.path:
#         raise ValueError("Invalid URL: Missing path component")
#     path = parsed_url.path.strip("/")  # Remove leading and trailing slashes
#     parts = path.split("/")
#     if len(parts) < 2:
#         return None, None
    
#     owner, repo = parts[0], parts[1]
#     return owner, repo


# def fetch_pr_files(repo_url, pr_number, github_token=None):
#     owner, repo = get_owner_repo(repo_url)
#     url=f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
#     headers = {
#         "Authorization": f"token {github_token}",
#     } if github_token else {}
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     return response.json()

# def fetch_file_content(repo_url, file_path, github_token=None):
#     owner, repo = get_owner_repo(repo_url)
#     url=f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
#     headers = {
#         "Authorization": f"token {github_token}",
#     } if github_token else {}
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     content= response.json()
#     return base64.b64decode(content["content"]).decode("utf-8")
    
    
        

# def collect_files(url, files=None):
#     if files is None:
#         files = []

#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()

#         for item in data:
#             if item["type"] == "file":
#                 files.append({
#                     "name": item["name"],
#                     "path": item["path"],
#                     "download_url": item["download_url"]
#                 })
#             elif item["type"] == "dir":
#                 collect_files(item["url"], files)  # Recursive call
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
    
#     return files

# if __name__ == "__main__":
#     base_url = "https://api.github.com/repos/Abhi9868/AI-PR-Review-Checker/contents/"
#     collected_files = collect_files(base_url)
    
#     print(f"Total files collected: {len(collected_files)}")
#     for file in collected_files:
#         print(file)
