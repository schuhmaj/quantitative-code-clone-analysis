import requests

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
        print(response.text)
    else:
        raise "Could not acquire the ressource at the given URL"


def parse_git_url(url: str):
    """
    Parses the content of a given web-resource for GitHub Repos
    Args:
        url: web-resource accessible via GET

    Returns:
        list of git urls

    """
    return get_url_resource(url)


parse_git_url(AWESOME_CPP)
