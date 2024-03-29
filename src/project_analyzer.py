import numpy as np
import matplotlib.colors
import matplotlib.pyplot as plt
from model.project import Project, load
from scipy import stats
import itertools
import collections

COLOR_MAP = {
    "C/C++": "blue",
    "C": "midnightblue",
    "Java": "red",
    "Python": "green",
    "Go": "cyan",
    "Rust": "orange",
    "Kotlin": "magenta"
}

LABEL_MAP = {
    "cpp": "C/C++",
    "c": "C",
    "java": "Java",
    "python": "Python",
    "go": "Go",
    "rust": "Rust",
    "kotlin": "Kotlin"
}


def filter_none(projects: [Project]) -> [Project]:
    return [p for p in projects if p.has_metrics()]


def plot_histogram_clone_coverage(projects: [Project], minimum_sloc: int = 0, suffix: str = ""):
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

    fig, ax = plt.subplots(figsize=(5, 4))

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
    ax.set_title(f"Clone Coverage Distribution ($N = {len(clone_coverage)}$ and $SLOC \geq {minimum_sloc}$)",
                 fontsize=11)

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.savefig(f"../plots/histogram{suffix}", dpi=300)
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


def plot_number_of_projects(projects_lists: [[Project]]):
    """
    Plots the number of projects depending on the size
    Args:
        projects_lists: list of projects

    Returns:
        void

    """
    fig, ax = plt.subplots(figsize=(6, 4))
    for projects in projects_lists:
        source_lines_of_code = np.array([p.get_sloc() for p in projects])
        color = COLOR_MAP[projects[0].language]
        language = projects[0].language

        values, base = np.histogram(source_lines_of_code, bins=np.logspace(0, 9, 100))
        cumulative = np.cumsum(values)

        # the histogram of the data
        ax.plot(base[:-1], len(source_lines_of_code)-cumulative, color=color, label=language)

    ax.axvline(10e5, ymin=-1, color='k', linestyle='dashed', linewidth=1.5)

    ax.hlines(y=100, xmin=0, xmax=10e8, color='k', linestyles='dashed', linewidth=1.5)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(10e8)
    ax.set_xticks(np.logspace(0, 9, 10))

    ax.legend(loc='lower left')

    ax.set_xlabel("Source Lines of Code")
    ax.set_ylabel("Number of projects")

    ax.set_title(f"Complementary cumulative distribution function ($N_{{total}} = {sum([len(p) for p in projects_lists])})$")

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.savefig("../plots/number", dpi=300)
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


def plot_mean_matrix(projects_dict, alpha=0.05, min_sloc=0, permutations=None):
    """
    Plots a matrix comparing the mean values
    Args:
        projects_dict: dictionary of list of projects
        alpha: for the t test
        min_sloc: minimal SLOC

    Returns:
        void

    """
    pvalues = collections.defaultdict(dict)
    for sample_1, sample_2 in itertools.product(projects_dict.keys(), repeat=2):
        if sample_1 == sample_2:
            pvalues[sample_1][sample_2] = 42
            continue
        statistic, pvalue_greater = compare_samples_statistically(sample_1, sample_2, projects_dict, alternative='greater', min_sloc=min_sloc, permutations=permutations)
        statistic, pvalue_less = compare_samples_statistically(sample_1, sample_2, projects_dict, alternative='less', min_sloc=min_sloc, permutations=permutations)
        if pvalue_greater < alpha:
            # print("Accept H_1: Greater")
            pvalues[sample_1][sample_2] = 1
        elif pvalue_less < alpha:
            # print("Accept H_1: Less")
            pvalues[sample_1][sample_2] = -1
        elif pvalue_greater > alpha and pvalue_less > alpha:
            # print("Accepting H_0: Equal")
            pvalues[sample_1][sample_2] = 0
        else:
            # print("Weird issue!!!!")
            raise Exception("Weird value calculated! Investigate!")

    matrix = np.array([[pvalues[s1][s2] for s2 in pvalues[s1]] for s1 in pvalues])

    cvals = [-1, 0, 1, 42]
    colors = ["green", "yellow", "red", "black"]

    norm = plt.Normalize(min(cvals), max(cvals))
    tuples = list(zip(map(norm, cvals), colors))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples)

    fig, ax = plt.subplots(figsize=(5, 5))

    plt.imshow(matrix, interpolation='none', cmap=cmap)
    labels = [LABEL_MAP[key] for key in projects_dict.keys()]
    plt.xticks(range(len(labels)), labels)
    plt.yticks(range(len(labels)), labels)

    # ax.legend()

    ax.set_xlabel("Language 2")
    ax.set_ylabel("Language 1")
    ax.set_title(f"Code Clone Coverage Mean Values Compared")

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.savefig(f"../plots/comparison", dpi=300)
    plt.close()


def compare_samples_statistically(
        sample_1, sample_2, projects_dict, alternative='two-sided', permutations=None, min_sloc=0):
    """
    Computes the t-statistic and p value for two distributions
    Args:
        sample_1: first sample name
        sample_2: second sample name
        projects_dict: dictionary of list of projects
        alternative: the alternative hypothesis H_1
        permutations: use instead a permutation test if given and not None
        min_sloc: minimal SLOC

    Returns:
        t-statistic, p-value

    """
    sample_1_coverage = np.array([p.get_clone_coverage() for p in projects_dict[sample_1] if p.get_sloc() > min_sloc])
    sample_2_coverage = np.array([p.get_clone_coverage() for p in projects_dict[sample_2] if p.get_sloc() > min_sloc])

    statistic, pvalue = stats.ttest_ind(sample_1_coverage, sample_2_coverage, equal_var=False, alternative=alternative,
                                        permutations=permutations)
    return statistic, pvalue


def compare_statistically(projects_dict, alpha=0.05, alternative='two-sided', permutations=None, min_sloc=0):
    """
    Calculates the t statistic and p value for some distributions of interest
    Args:
        projects_dict: dict of lists of projects
        alpha: significant niveau
        alternative: H_1
        permutations: use instead a permutation test
        min_sloc: minimal SLOC

    Returns:
        void

    """
    statistic, pvalue = \
        compare_samples_statistically("c", "cpp", projects_dict, alternative, permutations, min_sloc)
    print(f"Result pure C vs. C/C++: D={statistic} p={pvalue}")
    if pvalue > alpha:
        print("Accept H_0: Equal distributions")
    else:
        print(f"Accept H_1: {alternative}")

    statistic, pvalue = \
        compare_samples_statistically("cpp", "rust", projects_dict, alternative, permutations, min_sloc)
    print(f"Result C/C++ vs. Rust: D={statistic} p={pvalue}")
    if pvalue > alpha:
        print("Accept H_0: Equal distributions")
    else:
        print(f"Accept H_1: {alternative}")

    compare_samples_statistically("java", "kotlin", projects_dict, alternative, permutations, min_sloc)
    print(f"Result Java vs. Kotlin: D={statistic} p={pvalue}")
    if pvalue > alpha:
        print("Accept H_0: Equal distributions")
    else:
        print(f"Accept H_1: {alternative}")

    statistic, pvalue = \
        compare_samples_statistically("cpp", "java", projects_dict, alternative, permutations, min_sloc)
    print(f"Result C/C++ vs. Java: D={statistic} p={pvalue}")
    if pvalue > alpha:
        print("Accept H_0: Equal distributions")
    else:
        print(f"Accept H_1: {alternative}")


if __name__ == "__main__":
    language_projects_dict = {
        "cpp": [],
        "c": [],
        "java": [],
        "kotlin": [],
        "rust": [],
        "python": [],
        "go": []
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

    total_projects = language_projects_dict["go"]
    plot_histogram_clone_coverage(total_projects)
    plot_scatter_clone_coverage_loc(total_projects)
    plot_scatter_clone_coverage_method_length(total_projects)
    plot_scatter_clone_coverage_doc(total_projects)
    plot_scatter_clone_coverage_issues(total_projects)
    plot_scatter_clone_coverage_loc_m(language_projects_dict.values())
    plot_number_of_projects(language_projects_dict.values())
    compare_statistically(language_projects_dict, min_sloc=0, alternative='greater', permutations=None)
    plot_mean_matrix(language_projects_dict, min_sloc=0, permutations=10000)
