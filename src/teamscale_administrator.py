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
    go_projects = load("../model_output/go_projects.pickle")
    print("Total projects: {}".format(len(go_projects)))
    start_index = 0
    end_index = start_index + 100
    print(f"Creating projects from id {start_index} to {end_index}")
    create_projects(go_projects[start_index:end_index])
