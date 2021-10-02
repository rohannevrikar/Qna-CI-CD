import sys
import requests
import json
import time

host = str(sys.argv[1])
subscriptionKey = str(sys.argv[2])
kbName = str(sys.argv[3])
host = host + "qnamaker/v4.0/"

def monitorOperation(host, operationId):
    state = ""
    count = 0
    print(subscriptionKey)
    print(operationId)
    while(state != "Succeeded" and count < 10):
        response = requests.get(host + "operations/" + operationId, headers={'Ocp-Apim-Subscription-Key': subscriptionKey, 'Content-Type': 'application/json'})
        state = response.json()['operationState']
        count = count + 1
        time.sleep(1)
    if(count == 10 and state != "Succeeded"):
        raise Exception("Something went wrong while creating KB")
    return response.json()['resourceLocation'].split('/')[-1]

from openpyxl import load_workbook #pip install openpyxl
wb = load_workbook('Demo-KB.xlsx') #replace file path here
sheet = wb.active
questions = sheet['A'][1:]
answers = sheet['B'][1:]
distinct_answers = list(set([x.value for x in answers]))
reqBody = {}
qnaList = []

for answer in distinct_answers:
    result = [x for x in sheet['B'][1:] if x.value == answer] #find rows having the same answer
    rows = [x.row for x in result] #extract row numbers
    questions = [sheet['A'][x-1].value for x in rows] # get questions in that row
    qna = {}
    qna['id'] = 0
    qna['answer'] = answer
    qna['questions'] = questions
    qnaList.append(qna)

reqBody['qnaList'] = qnaList
reqBody['name'] = kbName
reqBody = json.dumps(reqBody, indent = 4) 

response = requests.get(host + "knowledgebases", headers={'Ocp-Apim-Subscription-Key': subscriptionKey, 'Content-Type': 'application/json'})
responseJson = response.json()
kbs = responseJson['knowledgebases']
matchingKb = [x for x in kbs if x['name'] == kbName]

if(not len(matchingKb)):
    response = requests.post(host + "knowledgebases/create", headers={'Ocp-Apim-Subscription-Key': subscriptionKey}, data=reqBody)
    operationId = response.json()['operationId']
    kbId = monitorOperation(host, operationId)
    if(response.status_code == 202):
        print("Creating KB")
    else:
        print("Something went wrong while creating KB")

else:
    kbId = matchingKb[0]["id"]
    response = requests.put(host + "knowledgebases/" + kbId, headers={'Ocp-Apim-Subscription-Key': subscriptionKey}, data=reqBody)
    if(response.status_code == 204):
        print("Updated KB")
    else:
        print("Something went wrong while updating KB")

print("Publishing KB " + kbId)

response = requests.post(host + "knowledgebases/" + kbId, headers={'Ocp-Apim-Subscription-Key': subscriptionKey}, data=reqBody)

if(response.status_code == 204):
    print("Published KB")
else:
    print("Something went wrong while publishing KB")
