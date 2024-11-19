
import requests
import base64
from urllib.parse import urlparse
import uuid
from groq import Groq
import json


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
        model="llama3-8b-8192",
        messages=[{
            "role":"user",
            "content":prompt
        }],
        temperature=1,
        top_p=1,
    )
    
    return completion.choices[0].message.content

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
    
    
        
# def analyze_pr(repo_url, pr_number, github_token=None):
#     task_id=str(uuid.uuid4())
#     try:
#         pr_files=fetch_pr_files(repo_url, pr_number, github_token)
#         print(len(pr_files))
#         # save to json file
#         with open("pr_files.json","w") as f:
#             json.dump(pr_files,f)
#         analysis_results=[]
#         for file in pr_files:
#             print(file)
#             file_name=file["filename"]
#             print(file_name)
#             raw_content=fetch_file_content(repo_url, file_name, github_token)
#             analysis_result=analyze_code_with_llm(raw_content,file_name)
#             # print(analysis_result)
#             analysis_results.append({
#                 "results":analysis_result,
#                 "file_name":file_name
#             })
            
#             return {
#                 "task_id":task_id,
#                 "results":analysis_results,
#             }
#     except Exception as e:
#         print(f"Error analyzing PR: {e}")
#         return {
#             "task_id":task_id,
#             "results":[],
#         }
    
def analyze_pr(repo_url, pr_number, github_token=None):
    task_id = str(uuid.uuid4())
    try:
        pr_files = fetch_pr_files(repo_url, pr_number, github_token)
        print(len(pr_files))
        
        with open("pr_files.json", "w") as f:
            json.dump(pr_files, f)
        
        analysis_results = []
        for file in pr_files:
            print(file)
            file_name = file["filename"]
            print(file_name)
            raw_content = fetch_file_content(repo_url, file_name, github_token)
            analysis_result = analyze_code_with_llm(raw_content, file_name)
            
            # Append analysis result to the list
            analysis_results.append({
                "results": analysis_result,
                "file_name": file_name
            })
        
        # Move return statement outside the loop
        return {
            "task_id": task_id,
            "results": analysis_results,
        }
    except Exception as e:
        print(f"Error analyzing PR: {e}")
        return {
            "task_id": task_id,
            "results": [],
        }
result=analyze_pr("https://github.com/Abhi9868/AI-PR-Review-Checker",4,None)
# save to json file
with open("result.json","w") as f:
    json.dump(result,f)
# print(result)