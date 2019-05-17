import argparse
import logging
import time
import datetime
import configparser
import pkg_resources
import locale
from pathlib import Path
from github import Github

logger = logging.getLogger()
temps_debut = time.time()


def main():
    args = parse_args()
    locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")
    auj = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config['github']['username']
    password = config['github']['password']

    g = Github(username, password)

    if args.file is None:
        file = pkg_resources.resource_string(__name__, "repos_list.txt")
        repos = file.decode("utf-8").split('\n')
        repos = repos[:-1]
    else:
        with open(args.file, 'r') as f:
            repos = f.readlines()
        repos = [x.strip() for x in repos]
    logger.debug(repos)

    logger.debug("Check Exports Folder")
    directory = "Exports"
    Path(directory).mkdir(parents=True, exist_ok=True)

    for repo_name in repos:
        try:
            repo = g.get_repo(repo_name)
            logger.debug("Repo : %s", repo)
            stargazers = repo.stargazers_count
            logger.debug("Stars : %s", stargazers)
            forks = repo.forks_count
            logger.debug("Forks : %s", forks)
            subscribers = repo.subscribers_count
            logger.debug("Subscribers : %s", subscribers)
            try:
                contributors = repo.get_contributors().totalCount
                logger.debug("Contributors : %s", contributors)
            except Exception as e:
                logger.error(e)
                contributors = "NA"

            if not Path(f"{directory}/repos_stats.csv").is_file():
                with open(f"{directory}/repos_stats.csv", 'a+') as f:
                    f.write(f"Repo,Date,Stars,Forks,Subscribers,Contributors\n")
            if not Path(f"{directory}/{repo_name.replace('/', '_')}_repo_stats.csv").is_file():
                with open(f"{directory}/{repo_name.replace('/', '_')}_repo_stats.csv", 'a+') as f:
                    f.write(f"Repo,Date,Stars,Forks,Subscribers,Contributors\n")

            with open(f"{directory}/repos_stats.csv", 'a+') as f:
                f.write(f"{repo_name},{auj},{stargazers},{forks},{subscribers},{contributors}\n")
            with open(f"{directory}/{repo_name.replace('/', '_')}_repo_stats.csv", 'a+') as f:
                f.write(f"{repo_name},{auj},{stargazers},{forks},{subscribers},{contributors}\n")
        except Exception as e:
            logger.error("%s : %s", repo_name, e)

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
