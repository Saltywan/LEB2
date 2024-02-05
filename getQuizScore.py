import json
import requests
import os

# Get the URL of the quiz from user input
url = input('Enter the URL of the quiz (example: https://app.leb2.org/class/375199/quiz/5608306): \n')

# Remove any spaces from the URL
url = url.replace(" ", "")

# Parse the URL in https and remove the trailing slash
if not url.startswith("https://"):
    url = "https://" + url if len(url.split("://")) == 1 else "https://" + url.split("://")[1]
if url.endswith("/"):
    url = url[:-1]

# Get the name of the output file from user input
outname = input('Enter the name of the output file (default: scores): \n') or 'scores'

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
req_url = url +"/get-student-response"
cookies = {"leb2_session": cookies}
headers = {
    "X-Requested-With": "XMLHttpRequest",
}
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

try:
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
            f.write('<h1>Score: ' + str(parse['student_info']['student_score']) + '</h1>\n')
            f.write('<ol>\n')
            for i in range(len(parse['student_info']['student_answer'])):
                f.write('<li class="question">\n')
                f.write('<p>' + parse['student_info']['student_answer'][i]['question'] + '</p>\n')
                f.write('<ul>\n')
                for j in range(len(parse['student_info']['student_answer'][i]['choices'])):
                    if (i==0):
                        (parse['student_info']['student_answer'][0]['teacher_choices']) = {-99: parse['student_info']['student_answer'][0]['teacher_choices'][0]}
                    if dict(list(parse['student_info']['student_answer'][i]['teacher_choices'].values())[0])['file'] != None:
                        f.write('<li> Correct Ans:' + dict(list(parse['student_info']['student_answer'][i]['teacher_choices'].values())[0])['choice_desc'] + '<img src="' + dict(list(parse['student_info']['student_answer'][i]['teacher_choices'].values())[0])['file']['expireUrl'] + '" alt="image"></li>\n')
                    else:
                        f.write('<li> Correct Ans:' + dict(list(parse['student_info']['student_answer'][i]['teacher_choices'].values())[0])['choice_desc'] + '</li>\n')
                    if parse['student_info']['student_answer'][i]['choices'][j]['is_correct'] == 1:
                        if parse['student_info']['student_answer'][i]['choices'][j]['file'] != None:
                            f.write('<li> You Picked: <b>' + parse['student_info']['student_answer'][i]['choices'][j]['choice_desc'] + '<img style="border: 3px solid red;" src="' + parse['student_info']['student_answer'][i]['choices'][j]['file']['expireUrl'] + '" alt="image"></b></li>\n')
                        else:
                            f.write('<li> You Picked: <b>' + parse['student_info']['student_answer'][i]['choices'][j]['choice_desc'] + '</b></li>\n')
                    else:
                        if parse['student_info']['student_answer'][i]['choices'][j]['file'] != None:
                            f.write('<li> You Picked:' + parse['student_info']['student_answer'][i]['choices'][j]['choice_desc'] + '<img src="' + parse['student_info']['student_answer'][i]['choices'][j]['file']['expireUrl'] + '" alt="image"></li>\n')
                        else:
                            f.write('<li> You Picked:' + parse['student_info']['student_answer'][i]['choices'][j]['choice_desc'] + '</li>\n')
                f.write('</ul>\n')
                f.write('</li>\n')
            f.write('</ol>\n')
            f.write('</body>\n')
            f.write('</html>\n')
except Exception as e:
    print('Error: ' + str(e))
    # print("Delete the session.txt file and try again")
    os.remove('session.txt')
    exit(1)

print('Done!')