import argparse
import logging
import time
import datetime
import configparser
import pkg_resources
import locale
import os
from github import Github

logger = logging.getLogger()
temps_debut = time.time()


def main():
    args = parse_args()
    file = args.file
    locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")
    auj = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config['github']['username']
    password = config['github']['password']

    g = Github(username, password)

    if file is None:
        file = pkg_resources.resource_string(__name__, "repos_list.txt")
        repos = file.decode("utf-8").split('\n')
        repos = repos[:-1]
    else:
        with open(file, 'r') as f:
            repos = f.readlines()
        repos = [x.strip() for x in repos]
    logger.debug(repos)

    logger.debug("Check Exports Folder")
    directory = "Exports"
    if not os.path.exists(directory):
        logger.debug("Creating Exports Folder")
        os.makedirs(directory)

    for repo_name in repos:
        repo = g.get_repo(repo_name)
        logger.debug(f"Repo : {repo}")
        stargazers = repo.stargazers_count
        logger.debug(f"Stars : {stargazers}")
        forks = repo.forks_count
        logger.debug(f"Forks : {forks}")
        subscribers = repo.subscribers_count
        logger.debug(f"Subscribers : {subscribers}")
        contributors = repo.get_contributors().totalCount
        logger.debug(f"Contributors : {contributors}")

        if not os.path.isfile(f"{directory}/repos_stats.csv"):
            with open(f"{directory}/repos_stats.csv", 'a+') as f:
                f.write(f"Repo,Date,Stars,Forks,Subscribers,Contributors\n")
        if not os.path.isfile(f"{directory}/{repo_name.replace('/', '_')}_repo_stats.csv"):
            with open(f"{directory}/{repo_name.replace('/', '_')}_repo_stats.csv", 'a+') as f:
                f.write(f"Repo,Date,Stars,Forks,Subscribers,Contributors\n")

        with open(f"{directory}/repos_stats.csv", 'a+') as f:
            f.write(f"{repo_name},{auj},{stargazers},{forks},{subscribers},{contributors}\n")
        with open(f"{directory}/{repo_name.replace('/', '_')}_repo_stats.csv", 'a+') as f:
            f.write(f"{repo_name},{auj},{stargazers},{forks},{subscribers},{contributors}\n")

    logger.debug("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description="Script extracting statistics from github repos")
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-f', '--file', help="File containing the repos (default : sample file containing popular repos)", type=str)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()
