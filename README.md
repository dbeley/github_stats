# github_stats

Extract statistics from github repos to a csv file

## Pre-requisites

- working github config.ini (see config_sample.ini)

## Installation

```
pipenv install '-e .'
```

## Help

```
pipenv run github_stats -h
```

## Usage

Given a simple txt file repos_list.txt

```
facebook/react
tensorflow/tensorflow
```

You can then call

```
pipenv run github_stats -f repos_list.txt
```

## Autostarting

A systemd service and its timer are provided in the systemd-service/ folder. You can tweak the service file to launch the script in another directory or to launch the script with other options.

The timer is set to launch the script every hour.

Then copy the service and the timer files in ~/.config/systemd/user/

You can launch the timer with

```
systemctl --user daemon-reload
systemctl --user enable --now github_stats.timer
```
