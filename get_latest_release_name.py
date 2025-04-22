import git
import requests
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(
    formatter_class=RawTextHelpFormatter,
    description=""
)
parser.add_argument("--repo_name", help="The name of the git repository of interest")

args = parser.parse_args()

release_url = f"https://api.github.com/repos/{args.repo_name}/releases/latest"
response = requests.get(release_url)

print(response.json()['name'].removeprefix('Release '))