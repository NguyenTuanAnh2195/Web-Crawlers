'''
A simple python script that takes in any number of integer number from
the terminal and checks if these numbers matches the current two last
numbers of each of the number of today's lotto result
'''
import requests
import json
from bs4 import BeautifulSoup
import argparse


def scraper():
    '''
    Send a request to http://ketqua.net to gather data
    Returns a list of integers of today's lotto result
    '''
    resp = requests.get('http://ketqua.net').text
    soup = BeautifulSoup(resp, 'lxml')
    lotto_list = [soup.find('td', id='rs_0_0').get_text(),
              soup.find('td', id='rs_1_0').get_text(),
              soup.find('td',
                        id=('rs_2_%i' % i for i in range(2))).get_text(),
              soup.find('td',
                        id=('rs_3_%i' % i for i in range(6))).get_text(),
              soup.find('td',
                        id=('rs_4_%i' % i for i in range(4))).get_text(),
              soup.find('td',
                        id=('rs_5_%i' % i for i in range(6))).get_text(),
              soup.find('td',
                        id=('rs_6_%i' % i for i in range(3))).get_text(),
              soup.find('td',
                        id=('rs_7_%i' % i for i in range(4))).get_text()]
    lotto_list = [int(i) % 100 for i in lotto_list]
    return lotto_list

def main():
    '''
    Takes in any number of integer arguments from the terminal
    Compares them with the lotto result returned by "scraper" function.
    Prints out if the user has entered a winning number
    '''
    result = scraper()
    parser = argparse.ArgumentParser()
    parser.add_argument('user_list', nargs='*', type=int)
    args = parser.parse_args()
    winning_numbers = []
    for i in args.user_list:
        for number in scraper():
            if i == number:
                winning_numbers.append(i)
            else:
                pass
    if len(winning_numbers) > 0:
        for i in winning_numbers:
            print("Congratulations! your winning number is {}".format(i))
    else:
        print("Sorry, better luck next time!")


if __name__ == '__main__':
    main()
