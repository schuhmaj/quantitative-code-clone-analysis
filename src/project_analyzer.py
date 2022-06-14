import numpy as np
import matplotlib.pyplot as plt
from model.project import Project, load


def plot_histogram_clone_coverage(projects: [Project]):
    """
    Plots a nice histogram for the clone coverage
    Args:
        projects: list of projects

    Returns:
        void

    """
    clone_coverage = np.array([p.metrics["metrics"][10]["value"] * 100.0 for p in projects])

    fig, ax = plt.subplots(figsize=(6, 4))

    # the histogram of the data
    ax.hist(clone_coverage, bins=20, range=(0.0, 100.0))

    ax.set_xlabel("Clone Coverage [%]")
    ax.set_ylabel("Number of Projects")
    ax.set_title("Clone Coverage Distribution for C++")

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.savefig("../plots/histogram", dpi=300)
    plt.close()


if __name__ == "__main__":
    cpp_projects = load("../model_output/cpp_projects_data.pickle")
    plot_histogram_clone_coverage(cpp_projects)