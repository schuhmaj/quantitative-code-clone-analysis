import requests
import re

AWESOME_CPP = "https://raw.githubusercontent.com/fffaraz/awesome-cpp/master/README.md"


def get_url_resource(url: str):
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


def parse_git_urls(url: str):
    """
    Parses the content of a given web-resource for GitHub Repos
    Args:
        url: web-resource accessible via GET

    Returns:
        list of tuples consisting of project name (str) and git url suffix (str)

    Examples:
        An example tuple could look like this:
            ("spdlog", "gabime/spdlog")

    """
    resource = get_url_resource(url)
    # TODO: Evaluate if the full git url is better?!
    # return re.findall(r"\[(\w*)\]\((https://github.com/\S*)\)", resource)
    return re.findall(r"\[(\w*)\]\(https://github.com/(\S*)\)", resource)

