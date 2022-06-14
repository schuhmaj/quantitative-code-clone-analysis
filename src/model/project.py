import pickle


class Project:
    """
    Represents a Project. Used to save the extracted state.
    """

    def __init__(self, project_id: str, repo_full_name: str, language: str, branch: str, revision: str):
        self.project_id = project_id
        self.repo_full_name = repo_full_name
        self.language = language
        self.branch = branch
        self.revision = revision
        self.metrics = {}

    def __str__(self) -> str:
        return f"Project ID: {self.project_id}, Repo Full Name: {self.repo_full_name}, Language: {self.language}," \
               f"Default Branch: {self.branch}, Revision: {self.revision}, Metrics: {str(self.metrics)}"


def save(filepath: str, projects: [Project]):
    with open(filepath, 'wb') as file:
        pickle.dump(projects, file, protocol=pickle.HIGHEST_PROTOCOL)


def load(filepath: str):
    with open(filepath, 'rb') as file:
        projects = pickle.load(file)
        return projects

