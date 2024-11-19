from fastapi import FastAPI,status
from pydantic  import BaseModel
from typing import Optional
import httpx

app = FastAPI()

class AnalyzePRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None

@app.post("/start_task/")
async def start_task_endpoint(task_request: AnalyzePRRequest):
    data={
        "repo_url":task_request.repo_url,
        "pr_number":task_request.pr_number,
        "github_token":task_request.github_token
    }
    async with httpx.AsyncClient() as client:
        response=await client.post("http://127.0.0.1:8000/start_task/",data=data)
        
        if response.status_code!=status.HTTP_200_OK:
            return {"error":"Failed to start task"}
    print(data)
    return {"task_id": "1234", "status": "task started"}



@app.get("/task_status/{task_id}/")
async def task_status_endpoint(task_id: str):
    async with httpx.AsyncClient() as client:
        response=await client.get(f"http://127.0.0.1:8000/task_status/{task_id}/")
        return response.json()
    
    return {"message":"something went wrong"}
    