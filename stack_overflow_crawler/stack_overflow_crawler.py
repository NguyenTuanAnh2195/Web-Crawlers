'''
A python script that takes in ***N*** number(s) of questions
with the tag ***Label*** and prints out the title of the
each question as well as the top rated answer
'''


import requests
import json
import argparse


def scraper(N, label):
    '''
    Takes N and label and use them to scrape data from Stack Api
    Stack Api allows users to retrieve data with the
    corresponding label and/or ID.
    '''
    source = 'https://api.stackexchange.com/2.2/tags/{}/faq?site=stackoverflow'.format(label)
    resp = requests.get(source).text
    json_format = json.loads(resp)
    json_format['item'] = sorted(json_format['items'],   # sort for the questions with most vote
                                 key=lambda dct: dct['score'],
                                 reverse=True)
    result = []
    for elem in json_format['items']:
        answer_resp = 'https://api.stackexchange.com/2.2/questions/{}/answers?order=desc&sort=activity&site=stackoverflow'.format(elem['question_id'])
        answer = requests.get(answer_resp).text
        answer_json = json.loads(answer)
        answer_json['items'] = sorted(answer_json['items'],   # sort for the answer with most vote
                                      key=lambda dct: dct['score'],
                                      reverse=True)
        answer_link = elem['link'] + "/{}#{}".format(
            answer_json['items'][0]['answer_id'],
            answer_json['items'][0]['answer_id'])
        result.append((elem['title'], answer_link))
        if len(result) == N:
            break
    return result


def main():
    parser = argparse.ArgumentParser(description='Receive user input.')
    parser.add_argument('integers', type=int)  # stores N questions
    parser.add_argument('tag', type=str)    # store Label tag
    args = parser.parse_args()
    try:
        result = scraper(args.integers, args.tag)
    except Exception:
        print("Invalid parameters!")
    for i in result:
        print('\n'.join(i))


if __name__ == '__main__':
    main()
