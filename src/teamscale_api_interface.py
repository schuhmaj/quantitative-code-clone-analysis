import requests
from requests.auth import HTTPBasicAuth
import json
from types import SimpleNamespace

TEAMSCALE_BASE_URL = "http://192.168.2.104:8080/"
TEAMSCALE_API_URL = "api/v8.0.3/"
TEAMSCALE_REST_URL = TEAMSCALE_BASE_URL + TEAMSCALE_API_URL

TEAMSCALE_USERNAME = "admin"
TEAMSCALE_ACCESS_TOKEN = "SBiAKGLJ8HFMHGy4kDlmWZi0kNwet9Y8"
TEAMSCALE_AUTHENTICATION = HTTPBasicAuth(TEAMSCALE_USERNAME, TEAMSCALE_ACCESS_TOKEN)


def get_findings(project_id: str, path: str = '', filter_findings: [str] = None, invert: bool = True, truncate: bool = True):
    """
    Get the findings of a projects.

    Args:
        project_id: The project id
        path: The general path were the findings shall be located inside the project
        filter_findings: Applies a filter and removes the elements listed in the filter
        invert: Inverts the filter, default true
        truncate: no truncation to the result

    Returns:
        Objects of the type findings

    Examples:
        If one only wants the code clones, then use the function in the following way:

            get_findings("project_name", filter_findings="Redundancy")

    """
    if filter_findings is None:
        filter_findings = []
    response = requests.get(TEAMSCALE_REST_URL + f"projects/{project_id}/findings/list", auth=TEAMSCALE_AUTHENTICATION,
                            params={
                                "uniform-path": f"{path}",
                                "filter": f"{filter_findings}",
                                "invert": f"{invert}",
                                "all": f"{truncate}"
                            })
    objects = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
    return objects


m = get_findings("breakup-model-cpp", filter_findings="Redundancy")
print(len(m))
