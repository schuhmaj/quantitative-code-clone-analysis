from tqdm import tqdm
from model.project import Project, load
import teamscale.api_interface as teamscale


def create_projects(projects: [Project]):
    """
    Create a list of projects in teamscale.
    Args:
        projects: list of projects

    Returns:
        void

    """
    print(f"Creating {len(projects)} projects in teamscale...")
    for project in tqdm(projects):
        if not teamscale.post_project_git(project):
            print(f"Project {project.repo_full_name} was not created!")


def delete_projects(projects: [Project]):
    """
    Deletes all projects in teamscale in the given list.
    Args:
        projects: list of projects

    Returns:
        void

    """
    print(f"Deleting {len(projects)} projects in teamscale...")
    for project in tqdm(projects):
        if not teamscale.delete_project(project.project_id):
            print(f"Project {project.repo_full_name} was not deleted!")


if __name__ == "__main__":
    cpp_projects = load("../model_output/cpp_projects.pickle")
    print("Total projects: {}".format(len(cpp_projects)))
    # create_projects(cpp_projects[0:100])
    # create_projects(cpp_projects[100:200])
    # create_projects(cpp_projects[200:300])
    # create_projects(cpp_projects[300:400])
    # create_projects(cpp_projects[400:500])
    # create_projects(cpp_projects[500:])  # TODO Next
