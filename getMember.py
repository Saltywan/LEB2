import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import json

# Get the URL of the class from user input
url = input('Enter the URL of the member page (example: https://app.leb2.org/class/501585/member): \n')

# Remove any spaces from the URL
url = url.replace(" ", "")

# Parse the URL in https and remove the trailing slash
if not url.startswith("https://"):
    url = "https://" + url if len(url.split("://")) == 1 else "https://" + url.split("://")[1]
if url.endswith("/"):
    url = url[:-1]

# Get the name of the output file from user input
outname = input('Enter the name of the output file (default: members): \n') or 'members'

def getCookies():
    # Get the cookies of leb2 from user input (first time setup only)
    if not(os.path.isfile('session.txt')):
        cookies = input('Enter the cookies of leb2 (leb2_session): \n')

    #check if session file exists
    if os.path.isfile('session.txt'):
        with open('session.txt', 'r') as f:
            cookies = f.read()
    else:
        with open('session.txt', 'w') as f:
            f.write(cookies)
    return cookies

def getMember(url, numPage=1, lastPage=0, cookies=getCookies()):
    # url = "https://app.leb2.org/class/389968/member?q=&page="
    query = "?q=&page="
    get_url = url + query + str(numPage)
    print(get_url)
    cookies = {"leb2_session": cookies}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36", 
            "X-Requested-With": "XMLHttpRequest"}

    r = requests.get(get_url, cookies=cookies, headers=headers)
    data = json.loads(r.text)
    page = BeautifulSoup(data['content'], 'lxml')
    if lastPage == 0:
        lastPage = page.find_all('a', class_='page-link')[-1].get('href').split('=')[-1]
    # print(lastPage)
    univid = page.find_all('a', class_='user-univid')
    uni_id = [univid[i].text for i in range(len(univid))]
    leb2_id = [univid[i].get('data-userid') for i in range(len(univid))]
    name = [univid[i].get('data-name')[1:] for i in range(len(univid))]
    email = re.findall(r'[\w\.-]+@[\w\.-]+', str(page))

    df = pd.DataFrame({'uni_id': uni_id, 'leb2_id': leb2_id, 'name': name, 'email': email})

    if str(numPage) == str(lastPage):
        # sort by uni_id
        df = df.sort_values(by=['uni_id'], ascending=True)
        return df
    else:
        # return df.append(getMember(url, numPage+1, lastPage))
        return pd.concat([df, getMember(url, numPage+1, lastPage)], ignore_index=True)

if __name__ == "__main__":
    try:
        df = getMember(url)
        df.to_csv(outname+'.csv', index=False)
        print(f"File {outname}.csv has been saved")
    except Exception as e:
        print(e)
        print("Please check the URL and try again")
        os.remove('session.txt')