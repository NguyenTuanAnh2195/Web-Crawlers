#!/usr/bin/env python3
'''
A very simple python script that takes the name of a
github user as script argument and prints out all
github repositories of that particular user
'''


import requests
import sys
import json


def scraper(user_name):
    ''' retrieves the user information from
    https://https://api.github.com/users/username/repos
    and adds them to a list, then prints out each
    list elements
    '''
    source = 'https://api.github.com/users/{}/repos'.format(user_name)
    try:
        resp = requests.get(source)
    except TypeError:
        print('Invalid username or username does not exist')
        pass
    json_format = json.loads(resp.text)
    repo_list = []
    for elem in json_format:
        repo_list.append(elem['url'])
    for repo in repo_list:
        print(repo)


def main():
    try:
        user = sys.argv[1]
    except IndexError:
        print("You have not entered an username")
    try:
        scraper(user)
    except UnboundLocalError:
        pass


if __name__ == '__main__':
    main()
