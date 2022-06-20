from tqdm import tqdm
from model.project import Project, save
import util.parser as parser
import util.git as git

# Collection of C/C++ projects
AWESOME_CPP = "https://raw.githubusercontent.com/fffaraz/awesome-cpp/master/README.md"
# Collection of Java projects
AWESOME_JAVA = "https://raw.githubusercontent.com/akullpp/awesome-java/master/README.md"
# Collection of Go projects
AWESOME_GO = "https://raw.githubusercontent.com/avelino/awesome-go/main/README.md"
# Collection of Rust projects
AWESOME_RUST = "https://raw.githubusercontent.com/rust-unofficial/awesome-rust/main/README.md"
# Collection of Python projects
AWESOME_PYTHON = "https://raw.githubusercontent.com/vinta/awesome-python/master/README.md"
# Collection of Kotlin projects
AWESOME_KOTLIN = "https://raw.githubusercontent.com/KotlinBy/awesome-kotlin/readme/README.md"

# Mapping from programming language to (list of) sources
PROJECT_SOURCES = {
    "C/C++": [AWESOME_CPP],
    "Java": [AWESOME_JAVA],
    "Go": [AWESOME_GO],
    "Rust": [AWESOME_RUST],
    "Python": [AWESOME_PYTHON],
    "Kotlin": [AWESOME_KOTLIN]
}


def extract_projects(programming_language: str) -> [Project]:
    """
    Extracts GitHub projects for a given programming language
    Args:
        programming_language: the programming language of the projects

    Returns:
        list of projects

    """
    git_repos = []
    sources = PROJECT_SOURCES[programming_language]
    print("Parsing sources for git repos...")
    for source in tqdm(sources):
        git_repos.extend(parser.parse_git_repos(source))
    print(f"Number of possible GitHub Repositories for {programming_language}: {len(git_repos)}")

    projects = []
    print("Creating projects and collection repo meta data...")
    for project_id, repo_full_name in tqdm(git_repos):
        try:
            default_branch, revision = git.get_github_info(repo_full_name)
            project = Project(project_id, repo_full_name, programming_language, default_branch, revision)
            projects.append(project)
        except Exception as e:
            print(e)

    print(f"Final number of collected projects in {programming_language}: {len(projects)}")
    return projects


if __name__ == "__main__":
    # cpp_projects = extract_projects("C/C++")
    # save("../model_output/cpp_projects.pickle", cpp_projects)
    # java_projects = extract_projects("Java")
    # save("../model_output/java_projects.pickle", java_projects)
    # go_projects = extract_projects("Go")
    # save("../model_output/go_projects.pickle", go_projects)
    # rust_projects = extract_projects("Rust")
    # save("../model_output/rust_projects.pickle", rust_projects)
    python_projects = extract_projects("Python")
    save("../model_output/python_projects.pickle", python_projects)
    # kotlin_projects = extract_projects("Kotlin")
    # save("../model_output/kotlin_projects.pickle", kotlin_projects)

