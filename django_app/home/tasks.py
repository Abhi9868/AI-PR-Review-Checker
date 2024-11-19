from celery import Celery
from celery import shared_task
from home.utils.github import analyze_pr
 
app=Celery("django_app")
app.config_from_object("django.conf:settings",namespace="CELERY")

@shared_task
def analyze_repo_task(repo_url, pr_number, github_token=None):
    result= analyze_pr(repo_url, pr_number, github_token)
    return result