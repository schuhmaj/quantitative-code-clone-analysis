from tqdm import tqdm
from model.project import Project, load, save
import teamscale.api_interface as teamscale


def extract_interesting_data(projects: [Project]):
    """
    Extracts the interesting data from a list of projects
    Args:
        projects: list of projects

    Returns:
        void

    """
    print("Extracting interesting data of projects...")
    for project in tqdm(projects):
        redundancy_findings = teamscale.get_findings(project.project_id, filter_findings="Redundancy")
        metrics = teamscale.get_metrics(project.project_id)
        project_metrics = {
            "redundancy": redundancy_findings,
            "metrics": metrics
        }
        project.metrics = project_metrics


if __name__ == "__main__":
    # cpp_projects = load("../model_output/cpp_projects.pickle")
    #
    # cpp_projects = cpp_projects[0:100]
    # extract_interesting_data(cpp_projects)
    #
    # save("../model_output/cpp_projects_data.pickle", cpp_projects)

    java_projects = load("../model_output/java_projects.pickle")

    java_projects = java_projects[0:100]
    extract_interesting_data(java_projects)

    save("../model_output/java_projects_data.pickle", java_projects)
