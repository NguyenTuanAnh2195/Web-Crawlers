'''
A Python scripts that uses the coordinates of the Notre Dame of HCM City
to find 50 coffe shops that is within its 5km radius.
API used is from Google Map.
The content of the file credentials, including the API key is
stored locally.
Selections are available on whether to create a CSV formatted file
or a SQLite Data Base.
'''
import requests
import json
import credentials
from time import sleep
import sqlite3

def scraper():
    '''
    Uses the coordinates of the location to scrape information from the
    Google Map API
    Page Tokens are stored in script variables
    '''
    result = []
    api_key = credentials.GGL_MAP_API_KEY
    resp = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=10.779614,106.699256&radius=5000&type=cafe&key={}".format(api_key)).text
    json_format = json.loads(resp)
    second_page_token = json_format['next_page_token']
    sleep(2)
    second_resp = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}".format(second_page_token, api_key)).text
    second_json_format = json.loads(second_resp)
    third_page_token = second_json_format['next_page_token']
    sleep(2)
    third_resp = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}".format(third_page_token, api_key)).text
    third_json_format = json.loads(third_resp)
    result.extend(i["name"] for i in json_format["results"])
    result.extend(i["name"] for i in second_json_format["results"])
    for i in third_json_format["results"]:
        result.append(i["name"])
        if len(result) == 50:
            break
    return result


def main():
    result = scraper()
    ''' # Delete this line and uncomment to insert data to a csv file
    with open("hcmcoffee.csv", "wt") as f:
        for i in result:
            f.write(i)
            f.write("\n")
    print(result)
    '''
    conn = sqlite3.connect('hcmcoffee.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Cafe (name TEXT);')
    for indx,i in enumerate(result):
        c.execute('INSERT INTO Cafe VALUES(\"%s\");' %i)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
