# Version Bump
Simple Python Bot for Automation Bump Version Microservice in your repository hosting


## Run in docker
- docker run -d -v $(pwd)/config.yaml:/etc/version-bump/config.yaml -p 5000:5000 javid907/bump-version-bot:0.1.0


## Webhook POST request:
Example:
  - http://127.0.0.1:5000/bot_bump_version?repo_name=repo-owner/repo-name

If you want bot to merge you need to add `merge=True` parameter in your webhook request
Example:
  - http://127.0.0.1:5000/bot_bump_version?repo_name=repo-owner/repo-name&merge=True
