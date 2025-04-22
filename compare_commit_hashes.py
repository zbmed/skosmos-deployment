import git
import argparse
from argparse import RawTextHelpFormatter
import shutil

parser = argparse.ArgumentParser(
    formatter_class=RawTextHelpFormatter,
    description="BEWARE: Running this script will delete a folder named 'log', should it exist.\n\nGiven a repository URL, a branch name and a reference commit hash, this script fetches the latest commit hash of the given repository's on the given branch. Afterwards, it outputs y if the commit hashes match, and n otherwise."
)
parser.add_argument("--repo_url", help="The URL of the git repository of interest")
parser.add_argument("--reference_commit", help="The reference commit hash to compare the latest commit hast of the given repository against")
parser.add_argument("--branch", help="The branch to fetch the latest commit hash from", default=None)

args = parser.parse_args()

# clone the repository
shutil.rmtree('./log', ignore_errors=True)
repo = git.Repo.clone_from(args.repo_url, './log', depth=1, branch=args.branch)

# get the latest commit
latest_commit = str(repo.head.commit)

# print y if commit hashes match, no otherwise
print('y' if latest_commit == args.reference_commit else 'n')

shutil.rmtree('./log')