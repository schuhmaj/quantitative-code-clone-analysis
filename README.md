# quantitative-code-clone-analysis
Quantitatively measuring code clones and related metrics in projects of
different programming languages and comparing + evaluating the results.


## Requirements

The requirements needed to run the project can be found in the
`requirements.txt` file in the repository root folder.

## Execution

In general, the project contains 4 scripts which are executed
separately.

1. `project_extractor.py` extracts GitHub Links from given source files,
    validates that these links are actually Repositories, find out the name 
    of the **default branch** & **latest revision** and saves the projects into a pickle file.
2. `teamscale_administrator.py` uses the pickled file as input and creates the
    corresponding projects within _teamscale_ via a GitConnector. This takes some time!
3. `teamscale_extractor.py` uses the pickled files as input (to retrieve the project IDs)
    and fetches the results of _teamscale_'s analysis. It then saves the appended projects
    again in pickle file.
4. `project_analyzer.py` uses the pickled files to process and present some graphics
    of the collected data

**CAUTION!** Step 2 and 3 need to be executed with some spacing since _teamscale_
needs time to analyze and process all the projects! So do not execute those scripts
directly after each other. First make sure that _teamscale_ has finished!
