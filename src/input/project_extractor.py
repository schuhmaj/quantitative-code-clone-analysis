import requests
import re
from github import Github

AWESOME_CPP = "https://raw.githubusercontent.com/fffaraz/awesome-cpp/master/README.md"


def get_resource(url: str):
    """
    Returns the content of the resource located at the given url.
    Args:
        url: web-resource accessible via GET

    Returns:
        string containing the response

    Raises:
        An exception if the resource could not be acquired

    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise "Could not acquire the ressource at the given URL"


def parse_git_repos(url: str):
    """
    Parses the content of a given web-resource for GitHub Repos
    Args:
        url: web-resource accessible via GET

    Returns:
        list of tuples consisting of project name (str) and full repository name on GitHub (str)

    Examples:
        An example tuple could look like this:
            ("spdlog", "gabime/spdlog")

    """
    resource = get_resource(url)
    return re.findall(r"\[(\w*)\]\(https://github.com/(\S*)\)", resource)


def get_defaults(repo_full_name: str):
    """
    Returns the name of the default branch of a given GitHub Repository
    Args:
        repo_full_name: the full name of the repository on GitHub

    Returns:
        tuple of default branch name (str) and last revision sha1 (str)

    """
    g = Github()
    repo = g.get_repo(repo_full_name)
    default_branch_name = repo._default_branch.value
    return default_branch_name, repo.get_branch(default_branch_name).commit.sha

