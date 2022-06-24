from tqdm import tqdm
from model.project import Project, load, save
import teamscale.api_interface as teamscale


def extract_interesting_data(projects: [Project]):
    """
    Extracts the interesting data from a list of projects
    Args:
        projects: list of projects (elements will be modified!)

    Returns:
        void

    """
    print("Extracting interesting data of projects...")
    for project in tqdm(projects):
        redundancy_findings = teamscale.get_findings(project.project_id, filter_findings="Redundancy")
        comprehensibility_findings = teamscale.get_findings(project.project_id, filter_findings="Comprehensibility")
        correctness_findings = teamscale.get_findings(project.project_id, filter_findings="Correctness")
        documentation_findings = teamscale.get_findings(project.project_id, filter_findings="Documentation")
        error_handling_findings = teamscale.get_findings(project.project_id, filter_findings="Error Handling")
        structure_findings = teamscale.get_findings(project.project_id, filter_findings="Structure")
        overview = teamscale.get_metrics(project.project_id)
        project_metrics = {
            "overview": overview,
            "redundancy": redundancy_findings,
            "comprehensibility": comprehensibility_findings,
            "correctness": correctness_findings,
            "documentation": documentation_findings,
            "error handling": error_handling_findings,
            "structure": structure_findings
        }
        project.metrics = project_metrics


def reduce_interesting_data(projects: [Project]):
    """
    Reduces the metrics (with exception to 'overview') to just the lengths, i.e. the number of findings in the category
    Args:
        projects: list of projects (elements will be modified!)

    Returns:
        void

    """
    for project in tqdm(projects):
        redundancy_findings = \
            len(project.metrics["redundancy"]) if project.metrics["redundancy"] is not None else None
        comprehensibility_findings = \
            len(project.metrics["comprehensibility"]) if project.metrics["comprehensibility"] is not None else None
        correctness_findings = \
            len(project.metrics["correctness"]) if project.metrics["correctness"] is not None else None
        documentation_findings = \
            len(project.metrics["documentation"]) if project.metrics["documentation"] is not None else None
        error_handling_findings =\
            len(project.metrics["error handling"]) if project.metrics["error handling"] is not None else None
        structure_findings = \
            len(project.metrics["structure"]) if project.metrics["structure"] is not None else None
        project_metrics = {
            "overview": project.metrics["overview"],
            "redundancy": redundancy_findings,
            "comprehensibility": comprehensibility_findings,
            "correctness": correctness_findings,
            "documentation": documentation_findings,
            "error handling": error_handling_findings,
            "structure": structure_findings
        }
        project.metrics = project_metrics


if __name__ == "__main__":
    # Programming Language
    language = "go"

    total_projects = load(f"../model_output/{language}_projects.pickle")
    last_start = (len(total_projects) // 100) * 100
    for i in range(len(total_projects) // 100):
        start = i * 100
        end = (i + 1) * 100
        print(f"Extracting data for {language} projects from {start} to {end}")
        projects = total_projects[start:end]
        extract_interesting_data(projects)
        save(f"../model_output/{language}/{language}_projects_data_{start}.pickle", projects)
        reduce_interesting_data(projects)
        save(f"../model_output/{language}/{language}_projects_data_{start}_reduced.pickle", projects)
    print(f"Extracting data for {language} projects from {last_start} to end")
    projects = total_projects[last_start:]
    extract_interesting_data(projects)
    save(f"../model_output/{language}/{language}_projects_data_{last_start}.pickle", projects)
    reduce_interesting_data(projects)
    save(f"../model_output/{language}/{language}_projects_data_{last_start}_reduced.pickle", projects)

