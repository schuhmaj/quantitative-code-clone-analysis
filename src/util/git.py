from github import Github, GithubException

# TODO: Add my access token here!
GITHUB_ACCESS_TOKEN = ""


def get_github_info(repo_full_name: str):
    """
    Returns additional info for a GitHub Repository: the name of the default branch, and its last revision number.
    The method further checks if the project exists at all.

    Args:
        repo_full_name: the full name of the repository on GitHub

    Returns:
        tuple of default branch name (str) and last revision sha1 (str)

    Raises:
        RuntimeError if the referenced repo does not exist

    """
    try:
        g = Github(GITHUB_ACCESS_TOKEN)
        repo = g.get_repo(repo_full_name)
        default_branch_name = repo._default_branch.value
        return default_branch_name, repo.get_branch(default_branch_name).commit.sha
    except GithubException as e:
        raise RuntimeError(str(e))

