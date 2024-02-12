from bs4 import BeautifulSoup
import json
import requests
import os

# Get the URL of the quiz from user input
url = input('Enter the URL of the quiz (example: https://app.leb2.org/class/xxxxxx/quiz/xxxxxxx): \n')

# Remove any spaces from the URL
url = url.replace(" ", "")

# Parse the URL in https and remove the trailing slash
if not url.startswith("https://"):
    url = "https://" + url if len(url.split("://")) == 1 else "https://" + url.split("://")[1]
if url.endswith("/"):
    url = url[:-1]

# Get the name of the output file from user input
outname = input('Enter the name of the output file (default: answer): \n') or 'answer'

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

# Define the URL
req_url = url +"/get-response"
cookies = {"leb2_session": cookies}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36", 
            "X-Requested-With": "XMLHttpRequest"}
print("Sending requests...")
# Send the GET request with the headers
response = requests.get(req_url, headers=headers, cookies=cookies, timeout=25)
parse = json.loads(response.text)

css = '''
@import url('https://fonts.googleapis.com/css2?family=Sarabun&display=swap');
* {
    font-family: 'Sarabun', sans-serif;
}

.question {
    margin-bottom: 50px;
}
.question > p {
    font-size: 1.2rem;
}
.question ul {
    list-style-type: circle;
}
.question li {
    margin-bottom: 5px;
    font-size: 1.1rem;
}
.question li b {
    color: red;
    font-weight: bold;
}
'''

#rendering the question and choices in HTML
try:
    response = list((parse['quiz_response']['questions'].values()))
    answer=[]
    for i in range(len(response)):
        try:
            answer.append(list(response[i]['choices'].values()))
        except:
            answer.append(list(response[i]['choices']))
    with open(outname+'.html', 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html lang="en">\n')
            f.write('<head>\n')
            f.write('<meta charset="UTF-8">\n')
            f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
            f.write('<title>' + outname + '</title>\n')
            f.write('<style>' + css + '</style>\n')
            f.write('</head>\n')
            f.write('<body>\n')
            f.write('<h1>' + str(outname) + '</h1>\n')
            f.write('<ol>\n')
            for i in range(len(response)):
                f.write('<li class="question">\n')
                f.write(response[i]['raw_question']+'\n')
                f.write('<ul>\n')
                for j in range(len(answer[i])):
                    if answer[i][j]['file'] != None:
                        f.write('<li><b>' + answer[i][j]['choice_desc'] + '<img style="max-width:30%;border: 3px solid red;" src="' + answer[i][j]['file_expire_url'] + '" alt="image"></b></li>\n')
                    else:
                        f.write('<li><b>' + answer[i][j]['choice_desc'] + '</b></li>\n')
                f.write('</ul>\n')
                f.write('</li>\n')
            f.write('</ol>\n')
            f.write('</body>\n')
            f.write('</html>\n')
except Exception as e:
    print('Error: ' + str(e))
    exit(1)

print('Done!')