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
    return re.findall(r"\[(\w*)\]\(https://github.com/(\S*)\)", resource)