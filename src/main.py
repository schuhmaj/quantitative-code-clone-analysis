import util.git as git
import teamscale.api_interface as teamscale


def main():
    print("Hello Quality!")
    repo_full_name = "schuhmaj/polyhedral-gravity-model-cpp"
    branch, revision = git.get_github_info(repo_full_name)
    print(teamscale.post_project_git("polyhedral-gravity-model-cpp", repo_full_name, branch, revision,
                                     "Rust (default)"))


def main2():
    print(teamscale.delete_project("polyhedral-gravity-model-cpp"))


if __name__ == "__main__":
    main2()
