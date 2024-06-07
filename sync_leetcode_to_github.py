import os
import requests
from github import Github

# Configuration
LEETCODE_USERNAME = os.getenv('LEETCODE_USERNAME')
LEETCODE_PASSWORD = os.getenv('LEETCODE_PASSWORD')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPOSITORY')

# Log in to LeetCode and get cookies
session = requests.Session()
login_url = 'https://leetcode.com/accounts/login/'
login_data = {
    'login': LEETCODE_USERNAME,
    'password': LEETCODE_PASSWORD
}
session.post(login_url, data=login_data)

# Get user submissions
submissions_url = 'https://leetcode.com/api/submissions/?offset=0&limit=20&lastkey='
response = session.get(submissions_url)
submissions = response.json()['submissions_dump']

# Initialize GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

for submission in submissions:
    if submission['status_display'] == 'Accepted':
        problem_title = submission['title']
        code = submission['code']
        filename = f"leetcode_solutions/{problem_title.replace(' ', '_').lower()}.py"

        # Check if file already exists
        try:
            contents = repo.get_contents(filename)
            repo.update_file(contents.path, f"Update {problem_title} solution", code, contents.sha)
        except:
            repo.create_file(filename, f"Add {problem_title} solution", code)

print("LeetCode solutions have been pushed to GitHub.")
