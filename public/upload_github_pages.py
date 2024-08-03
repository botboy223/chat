import os
import base64
import requests

# Replace these variables with your specific details
GITHUB_TOKEN = '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'
REPO_OWNER = 'botboy223'
REPO_NAME = 'repository-chat'
WORKFLOW_FILE = '.github/workflows/main.yml'
BRANCH = 'main'

# Define the path to your local directory containing the web page files
LOCAL_DIRECTORY = '/path/to/your/local/directory'

def upload_file_to_github(file_path, repo_owner, repo_name, branch, token):
    # Get the relative file path
    rel_path = os.path.relpath(file_path, LOCAL_DIRECTORY)
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{rel_path}'

    with open(file_path, 'rb') as file:
        content = base64.b64encode(file.read()).decode('utf-8')

    # Get the SHA of the existing file if it exists
    response = requests.get(url, headers={
        'Authorization': f'token {token}'
    })
    sha = response.json().get('sha')

    data = {
        'message': f'Add {rel_path}',
        'content': content,
        'branch': branch
    }
    if sha:
        data['sha'] = sha

    response = requests.put(url, json=data, headers={
        'Authorization': f'token {token}'
    })

    if response.status_code == 201 or response.status_code == 200:
        print(f'Successfully uploaded {rel_path}')
    else:
        print(f'Failed to upload {rel_path}: {response.json()}')

def upload_directory_to_github(local_directory, repo_owner, repo_name, branch, token):
    for root, _, files in os.walk(local_directory):
        for file in files:
            file_path = os.path.join(root, file)
            upload_file_to_github(file_path, repo_owner, repo_name, branch, token)

def trigger_github_workflow(repo_owner, repo_name, workflow_file, token, branch):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/{workflow_file}/dispatches'
    response = requests.post(url, json={"ref": branch}, headers={
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    })

    if response.status_code == 204:
        print(f'Successfully triggered workflow {workflow_file}')
    else:
        print(f'Failed to trigger workflow {workflow_file}: {response.json()}')

# Upload files
upload_directory_to_github(LOCAL_DIRECTORY, REPO_OWNER, REPO_NAME, BRANCH, GITHUB_TOKEN)

# Trigger GitHub workflow
trigger_github_workflow(REPO_OWNER, REPO_NAME, WORKFLOW_FILE, GITHUB_TOKEN, BRANCH)

print("Files uploaded and workflow triggered successfully!")
