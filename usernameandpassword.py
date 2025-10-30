import os
import base64
from argon2 import PasswordHasher
users = {"user": {"hash":"$argon2id$v=19$m=65536,t=3,p=4$EwTY9dDONdgIgDGk0KcYOA$qjMYKohx1zdnLzDBydVoEM/oKWb2hftzlJTC0FTQP74","id":2}}
admins = {"admin": {"hash":"$argon2id$v=19$m=65536,t=3,p=4$EwTY9dDONdgIgDGk0KcYOA$qjMYKohx1zdnLzDBydVoEM/oKWb2hftzlJTC0FTQP74","id":1}}
cookies = {}
forumsposts = {0: {"title":"stop doing donuts","text": "stop", "author": "admin","id":0}}
currentcookie = ""
things = ["signup", "login", "post", "forums"]
forumsactions = ["delete", "view", "edit"]
loginorlogout = True
hasher = PasswordHasher()
global nextpostid
nextpostid=len(forumsposts)
while True:
    for thing in things:
        print(thing)
    decision = input(">")
    match decision:
        case "signup":
            username = input("what username?\n")
            if username in users or username in admins:
                print("this username is already taken.")
                continue
            unhashedpass = input("what password?\n")
            password = hasher.hash(unhashedpass)
            users[username] = {"hash":password,"id":len(users)+1}
            print("thank you for signing up")
        case "login":
            if loginorlogout == True:
                username = input("what username?\n>")
                password = input("what password?\n>")
                if username in users:
                    try:
                        if hasher.verify(users[username].get("hash",""), password):
                            byte = os.urandom(32)
                            code = base64.urlsafe_b64encode(byte).rstrip(b"=")
                            currentcookie = code.decode("utf-8")
                            cookies[currentcookie] = username
                            print("successful login!")
                            things.remove("login")
                            loginorlogout = False
                            things.append("logout")
                    except:
                        print("invalid login")
                elif username in admins:
                    try:
                        if hasher.verify(admins[username].get("hash",""), password):
                            byte = os.urandom(32)
                            code = base64.urlsafe_b64encode(byte).rstrip(b"=")
                            currentcookie = code.decode("utf-8")
                            cookies[currentcookie] = username
                            print("successful login!")
                            things.remove("login")
                            loginorlogout = False
                            things.append("logout")
                    except:
                        print("invalid login")
                elif username not in users or username not in admins:
                    print("invalid login")
                else:
                    continue
        case "post":
            if not currentcookie == "" or currentcookie in cookies:
                user = cookies.get(currentcookie, "")
            else:
                print("you aren't signed in")
                continue
            post = input("what do you wanna post?\n>")
            text = input("what do you wanna have as the text?\n>")
            forumsposts[nextpostid] = {"title":post,"text": text, "author": user, "id":nextpostid}
            nextpostid+=1
        case "forums":
            if not cookies.get(currentcookie) in admins:
                for _, text in enumerate(forumsposts.items()):
                    print(f"{text[1].get("id")}: '{text[1].get("title")}' by {text[1].get("author")}")
                    print(f"    {text[1].get("text")}")
            else:
                for action in forumsactions:
                    print(action)
                whataction = input(">")
                match whataction:
                    case "delete":
                        for index, text in enumerate(forumsposts.items()):
                            print(f"{text[1].get("id")}: '{text[1].get("title")}' by {text[1].get("author")}")
                        whichone = int(input(">"))
                        forumsposts.pop(whichone)
                        print("successfully removed post")
                    case "view":
                        for index, text in enumerate(forumsposts.items()):
                            print(f"{index}: '{text[1].get("title")}' by {text[1].get("author")}")
                            print(f"    {text[1].get("text")}")
        case "logout":

            if not currentcookie == "":
                del cookies[currentcookie]
                currentcookie = ""
                print("successfully logged out.")
                things.remove("logout")
                things.insert(1, "login")
                loginorlogout = True
            else:
                continue