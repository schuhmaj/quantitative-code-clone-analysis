import requests
import re


def _get_resource(url: str):
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
    resource = _get_resource(url)
    # Depending on the file the regex needs to be adapted
    # This solution works for all awesome lists examined in the paper, expect the 'C' file
    # For 'C' use the following regex r"https://github.com/(\S*)" without braces
    git_repos = re.findall(r"\(https://github.com/(\S*)\)", resource)
    return [(repo_full_name.replace('/', '_'), repo_full_name) for repo_full_name in git_repos]
