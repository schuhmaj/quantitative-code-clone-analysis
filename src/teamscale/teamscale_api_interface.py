import requests
from requests.auth import HTTPBasicAuth
import json

# The Base URL of the Teamscale client
TEAMSCALE_BASE_URL = "http://192.168.2.104:8080/"
# The API Suffix which is appended to the client BASE URL
TEAMSCALE_API_URL = "api/v8.0.3/"
# The full base URL
TEAMSCALE_REST_URL = TEAMSCALE_BASE_URL + TEAMSCALE_API_URL

# The Teamscale username
TEAMSCALE_USERNAME = "admin"
# The access token for the Teamscale user
TEAMSCALE_ACCESS_TOKEN = "SBiAKGLJ8HFMHGy4kDlmWZi0kNwet9Y8"
# The concrete authentication payload for REST requests
TEAMSCALE_AUTHENTICATION = HTTPBasicAuth(TEAMSCALE_USERNAME, TEAMSCALE_ACCESS_TOKEN)

# Contains a mapping programming language --> included/ excluded file patterns
TEAMSCALE_LANGUAGE_SETTINGS = {
    "C/C++": "**.cpp, **.cc, **.c, **.h, **.hh, **.hpp, **.cxx, **.hxx, **.inl, **.inc, **.architecture",
    "Rust": "**.rs",
    "Java": ("**.java, **.architecture", "**/package-info.java, **/module-info.java"),
    "Kotlin": "**.kt, **.kts, **.ktm, **.architecture",
    "Python": "**.py, **.architecture",
    "Go": "**.go"
}


def get_project(project_id: str = None):
    """
    Gets all projects or if a project_id is specified just a single project

    Args:
        project_id: a project id, default None

    Returns:
        list of projects as dictionaries or a single project as dictionary depending on argument

    """
    if project_id is None:
        response = requests.get(TEAMSCALE_REST_URL + f"projects", auth=TEAMSCALE_AUTHENTICATION)
        return json.loads(response.text)
    else:
        response = requests.get(TEAMSCALE_REST_URL + f"projects/{project_id}",
                                auth=TEAMSCALE_AUTHENTICATION)
        return json.loads(response.text)


def get_project_configuration(project_id: str):
    """
    Gets the full project configuration for a certain project given a project_id.

    Args:
        project_id: a project id

    Returns:
        the project's configuration as dictionary

    """
    response = requests.get(TEAMSCALE_REST_URL + f"projects/{project_id}/configuration",
                            auth=TEAMSCALE_AUTHENTICATION)
    return json.loads(response.text)


def post_project_git(project_id: str, repo_full_name: str, default_branch: str, last_revision: str):
    """
    Creates a new project in Teamscale with the given id, git-repo path and default_branch name. The git-account is
    hardcoded to "schuhmaj" and should have been previously created in Teamscale!

    Args:
        project_id: the project id for referencing the project via the API (also the project name)
        repo_full_name: the full name of the repo on GitHub, e.g. schuhmaj/nasa-breakup-model-cpp
        default_branch: the default branch name, e.g. main
        last_revision: the last revision (sha1 of the last commit of the default branch)

    Returns:
        True if the project was successfully created

    """
    response = requests.post(TEAMSCALE_REST_URL + f"projects",
                             auth=TEAMSCALE_AUTHENTICATION,
                             json={
                                 "name": f"{project_id}",
                                 "publicIds": [
                                     f"{project_id}"
                                 ],
                                 "profile": "C/C++ (default)",
                                 "connectors": [
                                     {
                                         "type": "Git",
                                         "connectorIdentifierOptionName": "Repository identifier",
                                         "options": {
                                             "Account": "schuhmaj",
                                             "Path suffix": f"{repo_full_name}",
                                             "Repository identifier": f"{project_id}-repo",
                                             "Included file names": "**.cpp, **.cc, **.c, **.h, **.hh, **.hpp, **.cxx, **.hxx, **.inl, **.inc, **.architecture",
                                             "Excluded file names": "",
                                             "Important Branches": "",
                                             "Include Submodules": "false",
                                             "Submodule recursion depth": "10",
                                             "SSH Private Key ID": "",
                                             "Default branch name": f"{default_branch}",
                                             "Enable branch analysis": "false",
                                             "Included branches": ".*",
                                             "Excluded branches": "_anon.*",
                                             "Start revision": f"{last_revision}",
                                         }
                                     }
                                 ]
                             })
    return response.status_code == 201


def delete_project(project_id: str):
    """
    Deletes a project from teamscale
    Args:
        project_id: the project's id

    Returns:
        True if the deletion was successfully

    """
    response = requests.delete(TEAMSCALE_REST_URL + f"projects/{project_id}",
                               auth=TEAMSCALE_AUTHENTICATION)
    return response.status_code == 204


def get_findings(project_id: str, path: str = '', filter_findings: [str] = None, invert: bool = True,
                 truncate: bool = True):
    """
    Get the findings of a specific project given a project id.

    Args:
        project_id: The project id
        path: The general path were the findings shall be located inside the project
        filter_findings: Applies a filter and removes the elements listed in the filter (Notice the invert param!)
        invert: Inverts the filter, default true
        truncate: no truncation to the result

    Returns:
        List of findings as dictionaries

    Examples:
        If one only wants the code clones, then use the function in the following way:

            get_findings("project_name", filter_findings="Redundancy")

    """
    if filter_findings is None:
        filter_findings = []
    response = requests.get(TEAMSCALE_REST_URL + f"projects/{project_id}/findings/list",
                            auth=TEAMSCALE_AUTHENTICATION,
                            params={
                                "uniform-path": f"{path}",
                                "filter": f"{filter_findings}",
                                "invert": f"{invert}",
                                "all": f"{truncate}"
                            })
    return json.loads(response.text)


def get_metrics(project_id: str, path: str = ''):
    """
    Gets metrics of a specific project with a given project_id an optional sub folder.

    Args:
        project_id: the project id
        path: the optional path for which to collect the metrics inside the project structure

    Returns:
        list of metrics as dictionaries

    """
    response = requests.get(TEAMSCALE_REST_URL + f"projects/{project_id}/metric-assessments",
                            auth=TEAMSCALE_AUTHENTICATION,
                            params={
                                "uniform-path": f"{path}"
                            })
    return json.loads(response.text)[0]["metrics"]

