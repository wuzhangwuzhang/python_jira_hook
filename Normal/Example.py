import re
from jira import JIRA

jira = JIRA(server="https://jira-pro.uuzu.com",token_auth = 'ODQxOTk4MDcxNjg4OtyE8CzhSnnGpWuY6sHvQjSasrfB')

# Get all projects viewable by anonymous users.
projects = jira.projects()
print(projects)


# Sort available project keys, then return the second, third, and fourth keys.
keys = sorted(project.key for project in projects)[2:5]

# Get an issue.
issue = jira.issue("SLPK-19897")
# Find all comments made by Atlassians on this issue.
print(issue.fields.comment.comments)

# Add a comment to the issue.
# jira.add_comment(issue, "Comment text")

# You can update the entire labels field like this
# issue.update(fields={"labels": ["GitLab", "GitLabLog"]})

comment = jira.add_comment('SLPK-19897', 'new comment')    # no Issue object required
# comment = jira.add_comment(issue, 'new comment', visibility={'type': 'role', 'value': 'zhwu'})  # for admins only

comment.update(body='updated comment body')
comment.update(body='updated comment body but no mail notification', notify=True)