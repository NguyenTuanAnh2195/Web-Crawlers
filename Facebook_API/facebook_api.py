'''
A Python script that crawls facebook API and return certain fields,
including name, location and website of facebook sites that are
located within a 1 km radius of a certain coordinate (The center of Hanoi)
as well as are associated with certain keywords such as "caphe", "tra_da"
"cafe".
'''


import requests
import json
from credentials import APP_ID, APP_SECRET


def get_token():
    '''
    Receives token using the provided app ID and app Secret, both of which are stored within a
    local file credentials.py. Returns the access token
    '''
    token_resp = requests.get("https://graph.facebook.com/v2.12/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials" % (APP_ID, APP_SECRET)).text
    token_json = json.loads(token_resp)
    print(token_json)
    return token_json["access_token"]


def scraper():
    '''
    Using the access token, gets the result from facebook graph API
    and returns them as a list
    '''
    result = []
    access_token = get_token()
    keyword_list = ["coffee", "tea", "cafe", "ca_phe", "tra_da"]
    for keyword in keyword_list:
        resp = requests.get('https://graph.facebook.com/v2.12/search?q=%s&type=place&center=21.027875,105.853654&distance=1000&categories=["FOOD_BEVERAGE"]&fields=name,id,location,website&access_token=%s' % (keyword, access_token)).text
        json_format = json.loads(resp)
        print(json_format)
        for elem in json_format["data"]:
            result.append(elem)
    return result


def main():
    '''
    Calls the scraper() function and binds the returned result
    to a variable. Uses json to write the content of that file into
    hanoicoffee.json
    '''
    page_result = scraper()
    print(page_result)
    json.dumps(page_result, 'hanoicoffee.json', indent=4)


if __name__ == '__main__':
    main()
