import numpy as np
import matplotlib.pyplot as plt
from model.project import Project, load

COLOR_MAP = {
    "C/C++": "blue",
    "Java": "red",
    "Python": "green",
    "Go": "cyan",
    "Rust": "orange",
    "Kotlin": "magenta"
}


def filter_none(projects: [Project]) -> [Project]:
    return [p for p in projects if p.has_metrics()]


def plot_histogram_clone_coverage(projects: [Project], minimum_sloc: int = 0):
    """
    Plots a histogram for the clone coverage
    Args:
        projects: list of projects
        minimum_loc: minimum number of source lines of code

    Returns:
        void

    """
    clone_coverage = np.array([p.get_clone_coverage() for p in projects if p.get_sloc() >= minimum_sloc])
    color = COLOR_MAP[projects[0].language]
    language = projects[0].language
    mean_clone_coverage = np.mean(clone_coverage)
    std_clone_coverage = np.std(clone_coverage)

    fig, ax = plt.subplots(figsize=(6, 4))

    num_bins = 20

    # the histogram of the data
    n, bins, patches = ax.hist(clone_coverage, bins=num_bins, range=(0.0, 100.0), color=color, label=language)
    ax.axvline(mean_clone_coverage, ymin=-1, color='k', linestyle='dashed', linewidth=1.5,
               label=f"mean: {mean_clone_coverage:.2f}%")

    ax.hlines(y=1, xmin=mean_clone_coverage - std_clone_coverage, xmax=mean_clone_coverage + std_clone_coverage,
              color='k', linestyles='dashed', linewidth=1.5, label=f"std: {std_clone_coverage:.2f}%")

    # x = bins[:num_bins] + (100 / (num_bins * 2))
    # y = n
    # fit = np.polyfit(x, y, 10)
    # poly = np.poly1d(fit)
    # ax.plot(x, poly(x), "--", color='red', linewidth=1.5)

    ax.legend()
    ax.set_xlim(0, 100)
    ax.set_ylim(0)

    ax.set_xlabel("Clone Coverage [%]")
    ax.set_ylabel("Number of Projects")
    ax.set_title(
        f"Clone Coverage Distribution for {language} ($N = {len(clone_coverage)}$ and $SLOC \geq {minimum_sloc}$)",
        fontsize=10)

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.savefig("../plots/histogram", dpi=300)
    plt.close()


def plot_scatter_clone_coverage_loc(projects: [Project]):
    """
    Plots the clone coverage in relation to project size
    Args:
        projects: list of projects

    Returns:
        void

    """
    clone_coverage = np.array([p.get_clone_coverage() for p in projects])
    source_lines_of_code = np.array([p.get_sloc() for p in projects])
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


def plot_scatter_clone_coverage_loc_m(projects_lists: [[Project]]):
    """
    Plots the clone coverage in relation to project size
    Args:
        projects: list of projects

    Returns:
        void

    """
    fig, ax = plt.subplots(figsize=(6, 4))
    for projects in projects_lists:
        clone_coverage = np.array([p.get_clone_coverage() for p in projects])
        source_lines_of_code = np.array([p.get_sloc() for p in projects])
        colors = np.array([COLOR_MAP[p.language] for p in projects])
        language = projects[0].language

        # the histogram of the data
        ax.scatter(source_lines_of_code, clone_coverage, color=colors, alpha=0.33, label=language)

        ax.legend()

        ax.set_xscale("log")
        ax.set_ylim(0, 100)

        ax.set_xlabel("Source Lines of Code")
        ax.set_ylabel("Clone Coverage [%]")

        fit = np.polyfit(source_lines_of_code, clone_coverage, 1)
        poly = np.poly1d(fit)
        x = np.sort(source_lines_of_code)
        ax.plot(x, poly(x), "--", color=colors[0])

    ax.set_title(f"Clone Coverage/ Source Lines of Code ($N = {sum([len(p) for p in projects_lists])})$")

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.savefig("../plots/scatter_clone_coverage_loc_m", dpi=300)
    plt.close()


def plot_scatter_clone_coverage_method_length(projects: [Project]):
    """
    Plots the clone coverage in relation to method length assessment
    Args:
        projects: list of projects

    Returns:
        void

    """
    clone_coverage = np.array([p.get_clone_coverage() for p in projects])
    red_assessed_methods = np.array([p.get_method_length_assessment()[0] for p in projects])
    colors = np.array([COLOR_MAP[p.language] for p in projects])
    language = projects[0].language

    fig, ax = plt.subplots(figsize=(6, 4))

    # the histogram of the data
    ax.scatter(clone_coverage, red_assessed_methods, color=colors, alpha=0.33, label=language)

    ax.legend()

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    ax.set_xlabel("Clone Coverage [%]")
    ax.set_ylabel("Too-Long-Methods [%]")
    ax.set_title(f"Clone Coverage/ Too-Long-Methods for {language} ($N = {len(projects)})$")

    fit = np.polyfit(clone_coverage, red_assessed_methods, 1)
    poly = np.poly1d(fit)
    x = np.sort(clone_coverage)
    ax.plot(x, poly(x), "--", color=colors[0])

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.savefig("../plots/scatter_clone_coverage_method_length", dpi=300)
    plt.close()


def plot_scatter_clone_coverage_doc(projects: [Project]):
    """
    Plots the clone coverage in relation to the number of documentation issues divided by LoC
    Args:
        projects: list of projects

    Returns:
        void

    """
    clone_coverage = np.array([p.get_clone_coverage() for p in projects])
    documentation_findings = np.array([p.metrics["documentation"] / (p.get_sloc() + 1) for p in projects])
    colors = np.array([COLOR_MAP[p.language] for p in projects])
    language = projects[0].language

    fig, ax = plt.subplots(figsize=(6, 4))

    # the histogram of the data
    ax.scatter(clone_coverage, documentation_findings, color=colors, alpha=0.33, label=language)

    ax.legend()

    ax.set_xlim(0, 100)
    ax.set_yscale('log')

    ax.set_xlabel("Clone Coverage [%]")
    ax.set_ylabel("#Documentation/ #SLOC")
    ax.set_title(f"Clone Coverage to #Documentation Issues/#SLOC for {language} ($N = {len(projects)})$", fontsize=10)

    fit = np.polyfit(clone_coverage, documentation_findings, 1)
    poly = np.poly1d(fit)
    x = np.sort(clone_coverage)
    ax.plot(x, poly(x), "--", color=colors[0])

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.savefig("../plots/scatter_clone_coverage_documentation", dpi=300)
    plt.close()


def plot_scatter_clone_coverage_issues(projects: [Project]):
    """
    Plots the clone coverage in relation to the total number of issues
    Args:
        projects: list of projects

    Returns:
        void

    """
    clone_coverage = np.array([p.get_clone_coverage() for p in projects])
    findings = np.array(
        [(p.metrics["documentation"] + p.metrics["comprehensibility"] + p.metrics["correctness"]
          + p.metrics["error handling"] + p.metrics["structure"]) / (p.get_sloc() + 1) for p in projects])
    colors = np.array([COLOR_MAP[p.language] for p in projects])
    language = projects[0].language

    fig, ax = plt.subplots(figsize=(6, 4))

    # the histogram of the data
    ax.scatter(clone_coverage, findings, color=colors, alpha=0.33, label=language)

    ax.legend()

    ax.set_xlim(0, 100)

    ax.set_xlabel("Clone Coverage [%]")
    ax.set_ylabel("#Issues/ #SLOC")
    ax.set_title(f"Clone Coverage to #Issues/#SLOC for {language} ($N = {len(projects)})$", fontsize=10)

    fit = np.polyfit(clone_coverage, findings, 1)
    poly = np.poly1d(fit)
    x = np.sort(clone_coverage)
    ax.plot(x, poly(x), "--", color=colors[0])

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.savefig("../plots/scatter_clone_coverage_issues", dpi=300)
    plt.close()


if __name__ == "__main__":
    language_projects_dict = {
        "cpp": [],
        "java": [],
        "kotlin": [],
        "rust": [],
        "python": []
    }
    for language, projects in language_projects_dict.items():
        num = len(load(f"../model_output/{language}_projects.pickle"))
        print(f"Loading {num} {language} projects")
        for i in range(num // 100 + 1):
            print(f"Loading {language} projects from {i * 100} to {(i + 1) * 100}")
            suffix = i * 100
            try:
                projects_batch = load(f"../model_output/{language}/{language}_projects_data_{suffix}_reduced.pickle")
                projects.extend(projects_batch)
            except:
                print(f"../model_output/{language}/{language}_projects_data_{suffix}_reduced.pickle was not found!")
        language_projects_dict[language] = filter_none(projects)

    total_projects = language_projects_dict["python"]
    plot_histogram_clone_coverage(total_projects)
    plot_scatter_clone_coverage_loc(total_projects)
    plot_scatter_clone_coverage_method_length(total_projects)
    plot_scatter_clone_coverage_doc(total_projects)
    plot_scatter_clone_coverage_issues(total_projects)
    plot_scatter_clone_coverage_loc_m(language_projects_dict.values())
