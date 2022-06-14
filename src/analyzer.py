from tqdm import tqdm
from model.project import Project, load

if __name__ == "__main__":
    cpp_projects = load("../model_output/cpp_projects.pickle")
    for project in cpp_projects:
        print(project)