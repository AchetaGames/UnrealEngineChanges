import os
from github import Github
import re

TOKEN = os.environ.get('TOKEN')
g = Github(TOKEN)

issues_repo = g.get_repo("AchetaGames/UnrealEngineChanges")

open_issues = issues_repo.get_issues(state='open')

for issue in open_issues:
    print(issue.title)
    pr = re.search("(?P<url>https?://[^\s]+)", issue.body).group("url")
    print("Link: {}".format(pr))
    r = re.search("/(?P<repo>[0-9a-zA-z]+/[0-9a-zA-z]+)/pull/(?P<id>[0-9]+)", pr)
    if r:
        pr_repo = g.get_repo(r.group("repo"))
        print("repo: {}".format(r.group("repo")))
        print("pr_id: {}".format(r.group("id")))
        request = pr_repo.get_pull(int(r.group("id")))
        for label in request.labels:
            if label.name=="Accepted":
                issue.add_to_labels(issues_repo.get_label("Accepted"))         
        if request.merged or request.closed_at:
            issue.edit(state="Closed")
            continue      
        if not request.mergeable:
            issue.add_to_labels(issues_repo.get_label("Merge Conflict"))
