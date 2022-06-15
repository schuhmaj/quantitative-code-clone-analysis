import numpy as np
import matplotlib.pyplot as plt
from model.project import Project, load


COLOR_MAP = {
    "C/C++": "blue",
    "Java": "red",
    "Python": "magenta"
}


def filter_none(projects: [Project]) -> [Project]:
    return [p for p in projects if p.metrics["metrics"] is not None]


def plot_histogram_clone_coverage(projects: [Project]):
    """
    Plots a histogram for the clone coverage
    Args:
        projects: list of projects

    Returns:
        void

    """
    clone_coverage = np.array([p.metrics["metrics"][10]["value"] * 100.0 for p in projects])
    color = COLOR_MAP[projects[0].language]
    language = projects[0].language

    fig, ax = plt.subplots(figsize=(6, 4))

    # the histogram of the data
    ax.hist(clone_coverage, bins=20, range=(0.0, 100.0), color=color, label=language)

    ax.legend()

    ax.set_xlabel("Clone Coverage [%]")
    ax.set_ylabel("Number of Projects")
    ax.set_title(f"Clone Coverage Distribution for {language} ($N = {len(projects)})$")

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.savefig("../plots/histogram", dpi=300)
    plt.close()


def plot_scatter_clone_coverage(projects: [Project]):
    """
    Plots the clone coverage in relation to project size
    Args:
        projects: list of projects

    Returns:
        void

    """
    clone_coverage = np.array([p.metrics["metrics"][10]["value"] * 100.0 for p in projects])
    source_lines_of_code = np.array([p.metrics["metrics"][2]["value"] * 100.0 for p in projects])
    colors = np.array([COLOR_MAP[p.language] for p in projects])
    language = projects[0].language

    fig, ax = plt.subplots(figsize=(6, 4))

    # the histogram of the data
    ax.scatter(source_lines_of_code, clone_coverage, color=colors, alpha=0.33, label=language)

    ax.legend()

    ax.set_xscale("log")
    ax.set_ylim(0, 100)

    ax.set_xlabel("Source Lines of Code")
    ax.set_ylabel("Clone Coverage [%]")
    ax.set_title(f"Clone Coverage/ Source Lines of Code for {language} ($N = {len(projects)})$")

    fit = np.polyfit(source_lines_of_code, clone_coverage, 1)
    poly = np.poly1d(fit)
    x = np.sort(source_lines_of_code)
    ax.plot(x, poly(x), "--", color=colors[0])

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.savefig("../plots/scatter_clone_coverage_loc", dpi=300)
    plt.close()


if __name__ == "__main__":
    cpp_projects = load("../model_output/cpp_projects_data.pickle")
    cpp_projects = filter_none(cpp_projects)
    plot_histogram_clone_coverage(cpp_projects)
    plot_scatter_clone_coverage(cpp_projects)

    java_projects = load("../model_output/java_projects_data.pickle")
    java_projects = filter_none(java_projects)
    plot_histogram_clone_coverage(java_projects)
    plot_scatter_clone_coverage(java_projects)
