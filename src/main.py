import project_extractor
import teamscale_api_interface as teamscale


def main():
    print("Hello Quality!")
    urls = dict(project_extractor.parse_git_urls(project_extractor.AWESOME_CPP))
    if teamscale.post_project_git("spdlog", urls["spdlog"], "v1.x"):
        print("Success!")
    else:
        print("Failed!")


if __name__ == "__main__":
    main()
