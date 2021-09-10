# Git extractor
Extracts list of Git commits into CSV

Output commits for a single month:
```shell
$ python extractor.py --month 2021-01 /path/to/repo1 /path/to/repo2 ... output_file.csv
```

Output commits for time period:
```shell
$ python extractor.py --since 2021-01-12 --until 2021-09-10 /path/to/repo1 /path/to/repo2 ... output_file.csv
```

By default, the script outputs commits to the `master` branch. To override the default branch name use `DEFAULT_BRANCH` env variable. To specify a different branch for a specific repo, put it after the repo path separated with colon, e.g.
```shell
$ python extractor.py --month 2021-01 /path/to/repo1:my_branch_in_repo1 /path/to/repo2:my_branch_in_repo2 ... output_file.csv
```
