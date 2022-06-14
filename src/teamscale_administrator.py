from tqdm import tqdm
from model.project import Project, load
import teamscale.api_interface as teamscale


def create_projects(projects: [Project]):
    print("Creating projects in teamscale...")
    for project in tqdm(projects):
        if not teamscale.post_project_git(project):
            print(f"Project {project.repo_full_name} was not created!")


def delete_projects(projects: [Project]):
    print("Deleting projects in teamscale...")
    for project in tqdm(projects):
        if not teamscale.delete_project(project):
            print(f"Project {project.repo_full_name} was not deleted!")


if __name__ == "__main__":
    cpp_projects = load("../model_output/cpp_projects.pickle")
    create_projects(cpp_projects[0:2])
