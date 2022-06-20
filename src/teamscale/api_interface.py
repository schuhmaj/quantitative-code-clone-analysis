import requests
from requests.auth import HTTPBasicAuth
import json
from model.project import Project

# The Base URL of the Teamscale client
TEAMSCALE_BASE_URL = "http://192.168.2.104:8080/"
# The API Suffix which is appended to the client BASE URL
TEAMSCALE_API_URL = "api/v8.0.3/"
# The full base URL
TEAMSCALE_REST_URL = TEAMSCALE_BASE_URL + TEAMSCALE_API_URL

# The Teamscale username
TEAMSCALE_USERNAME = "admin"
# The access token for the Teamscale user
TEAMSCALE_ACCESS_TOKEN = "R1ywCay9duOFLBZo6f4LVA5AacLPoH5H"
# The concrete authentication payload for REST requests
TEAMSCALE_AUTHENTICATION = HTTPBasicAuth(TEAMSCALE_USERNAME, TEAMSCALE_ACCESS_TOKEN)

# Contains a mapping programming language --> included/ excluded file patterns
TEAMSCALE_LANGUAGE_SETTINGS = {
    "C/C++":
        ("**.cpp, **.cc, **.c, **.h, **.hh, **.hpp, **.cxx, **.hxx, **.inl, **.inc, **.architecture",
         ""),
    "Rust":
        ("**.rs",
         ""),
    "Java":
        ("**.java, **.architecture",
         "**/package-info.java, **/module-info.java"),
    "Kotlin":
        ("**.kt, **.kts, **.ktm, **.architecture",
         ""),
    "Python":
        ("**.py, **.architecture",
         ""),
    "Go":
        ("**.go",
         "")
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


def post_project_git(project: Project):
    """
    Creates a new project in Teamscale with the given id, git-repo path and default_branch name. The git-account is
    hardcoded to "schuhmaj" and should have been previously created in Teamscale!

    Args:
        project: the project which should be created

    Returns:
        True if the project was successfully created

    """
    included_files, excluded_files = TEAMSCALE_LANGUAGE_SETTINGS[project.language]
    response = requests.post(TEAMSCALE_REST_URL + f"projects",
                             auth=TEAMSCALE_AUTHENTICATION,
                             json={
                                 "name": project.project_id,
                                 "publicIds": [
                                     project.project_id
                                 ],
                                 "profile": f"{project.language} (default)",
                                 "connectors": [
                                     {
                                         "type": "Git",
                                         "connectorIdentifierOptionName": "Repository identifier",
                                         "options": {
                                             "Account": "schuhmaj",
                                             "Path suffix": project.repo_full_name,
                                             "Repository identifier": f"{project.project_id}-repo",
                                             "Included file names": included_files,
                                             "Excluded file names": excluded_files,
                                             "Include Submodules": "false",
                                             "Submodule recursion depth": "10",
                                             "Default branch name": project.branch,
                                             "Enable branch analysis": "false",
                                             "Start revision": project.revision,
                                             "End revision": project.revision
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
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None


def get_metrics(project_id: str, path: str = ''):
    """
    Gets metrics of a specific project with a given project_id an optional sub folder.

    Args:
        project_id: the project id
        path: the optional path for which to collect the metrics inside the project structure

    Returns:
        list of metrics as dictionaries or None if none where available

    """
    response = requests.get(TEAMSCALE_REST_URL + f"projects/{project_id}/metric-assessments",
                            auth=TEAMSCALE_AUTHENTICATION,
                            params={
                                "uniform-path": f"{path}"
                            })
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if len(json_data) >= 1:
            return json_data[0]["metrics"]
        else:
            return None
    else:
        return None
