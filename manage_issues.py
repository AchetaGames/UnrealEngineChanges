import os
from github import Github
import re

TOKEN = os.environ.get('TOKEN')
g = Github(TOKEN)

issues_repo = g.get_repo("AchetaGames/UnrealEngineChanges")

open_issues = issues_repo.get_issues(state='open')
print("Checking issues against upstream Unreal Engine repository")
for issue in open_issues:
    print(issue.title)
    pr = re.search("(?P<url>https?://[^\s]+)", issue.body).group("url")
    r = re.search("/(?P<repo>[0-9a-zA-z]+/[0-9a-zA-z]+)/pull/(?P<id>[0-9]+)", pr)
    if r:
        pr_repo = g.get_repo(r.group("repo"))
        request = pr_repo.get_pull(int(r.group("id")))
        print("\tHas linked PR: {}/pull/{}".format(r.group("repo"), r.group("id")))
        for label in request.labels:
            if label.name == "Accepted":
                print("\tThe PR is Accepted")
                issue.add_to_labels(issues_repo.get_label("Accepted"))
        if request.merged or request.closed_at:
            print("\tThe PR is Accepted")
            issue.edit(state="Closed")
            issue.remove_from_labels(issues_repo.get_label("Waiting for Approval"))
            continue
        if not request.mergeable:
            print("\tPR is blocked")
            issue.add_to_labels(issues_repo.get_label("Merge Conflict"))
        else:
            print("\tPR is Waiting for Review")
            issue.add_to_labels(issues_repo.get_label("Waiting for Approval"))
    else:
        print("\tNo PR linked but there is a patch link")
        issue.add_to_labels(issues_repo.get_label("Patch"))
