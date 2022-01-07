from bs4 import BeautifulSoup
import requests
import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
from user_settings import URL, list_key, email

url_get = requests.get(URL)
soup = BeautifulSoup(url_get.content, 'html.parser')

h3 = soup.find('h3')
for sibling in h3.find_next_siblings():
    if sibling.name == "h3":
        break
    else:
        title_element = sibling.find_all("div", class_="list-title mathjax")
        abstract_element = sibling.find_all("p", class_="mathjax")
        link_element = sibling.find_all("a",  {"title":"Abstract"})

list_index = []

email_check = False
email_body = ""
for key in list_key:
    print(key)
    email_body = email_body + "-----------------------------\n" + key + "\n"
    aux = 0
    for index, title in enumerate(title_element):
        if set(list_key[key]) & set(title.text.strip().lower().split(' ')) or set(list_key[key]) & set(abstract_element[index]):            
            print(title.text.strip(), '\n')
            print(abstract_element[index].text.strip(), '\n')
            print("www.arxiv.org/abs/"+link_element[index].text.strip().split(':')[-1], '\n')
            print("-----------------------------")

            email_body = email_body + str(title.text.strip())+'\n' + "Abstract:"+ str(abstract_element[index].text.strip())+'\n'+\
                            "www.arxiv.org/abs/"+str(link_element[index].text.strip().split(':')[-1])+'\n\n'
            list_index.append(index)
            aux = aux + 1
            email_check = True
    if aux == 0:
        print("No articles found today. \n")
        email_body = email_body + "No articles published today. \n\n"


SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API quickstart'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def SendMessage(sender, to, subject, msgHtml, msgPlain):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message1 = CreateMessageHtml(sender, to, subject, msgHtml, msgPlain)
    result = SendMessageInternal(service, "me", message1)
    return result

def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"
    return "OK"

def CreateMessageHtml(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    return {'raw': raw}

def send_mail():
    to = email
    sender = email
    subject = "Your ArXiv list today"
    msgHtml = email_body.replace("\n", "<br>")
    msgPlain = email_body
    SendMessage(sender, to, subject, msgHtml, msgPlain)


if __name__ == "__main__":
    send_mail()