import pickle
import re


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

    def get_method_length_assessment(self) -> (float, float, float):
        """
        Returns the method length assessment (order Red, Yellow, Green) percentages.

        Returns:
            tuple of red, yellow, green assessed methods

        """
        text = self.metrics["overview"][5]["formattedTextValue"]
        return tuple([float(x) for x in re.findall(r"\w: \d+ \((\d+.\d+)%\)", text)])

    def has_metrics(self) -> bool:
        """
        Returns False if some metrics are None
        Returns:
            True if all metrics are defined values

        """
        for value in self.metrics.values():
            if value is None:
                return False
        return True

    def get_clone_coverage(self) -> float:
        """
        Returns the clone coverage as percentage value
        Returns:
            clone coverage

        """
        return self.metrics["overview"][10]["value"] * 100.0

    def get_source_lines_of_code(self) -> int:
        """
        Returns the source lines of code
        Returns:
            source lines of code

        """
        return self.metrics["overview"][2]["value"] * 100.0


def save(filepath: str, projects: [Project]):
    with open(filepath, 'wb') as file:
        pickle.dump(projects, file, protocol=pickle.HIGHEST_PROTOCOL)


def load(filepath: str) -> [Project]:
    with open(filepath, 'rb') as file:
        projects = pickle.load(file)
        return projects

