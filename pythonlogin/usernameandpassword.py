import os
import base64
from argon2 import PasswordHasher
import datetime
import json

dt = datetime.datetime.now()
with open("pythonlogin/users/users.json", "r") as f:
    global a
    a: dict = json.loads(f.read())
users = a
with open("pythonlogin/admins/admins.json", "r") as f:
    global b
    b: dict = json.loads(f.read())
admins = b
cookies = {}
forumsposts = {}
forumsreplys = {}
with open("pythonlogin/forums/forumposts.json", "r") as f:
    global posts
    posts: dict = json.load(f)
    forumsposts = posts
with open("pythonlogin/forums/forumreplys.json", "r") as f:
    global replys
    replys: dict = json.load(f)
    forumsreplys = replys
currentcookie = ""
currentuser = "Anonymous"
things = ["signup", "login", "post", "forums"]
forumsactions = ["delete", "view"]
loginorlogout = True
hasher = PasswordHasher()
nextpostid = len(forumsposts) + 1
nextreplyid = len(forumsreplys) + 1
currentid = nextpostid + nextreplyid - 1
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
            z = {"hash": password, "id": len(users) + 2}
            with open("pythonlogin/users/users.json", "r") as f:
                global lol
                lol: dict = json.load(f)
            with open("pythonlogin/users/users.json", "w") as f:
                lol[username] = z
                f.write(json.dumps(lol, indent=2))
            print("thank you for signing up")
        case "login":
            if loginorlogout == True:
                username = input("what username?\n>")
                password = input("what password?\n>")
                with open("pythonlogin/users/users.json", "r") as f:
                    a: dict = json.loads(f.read())
                    users = a
                with open("pythonlogin/admins/admins.json") as f:
                    b: dict = json.loads(f.read())
                    admins = b
                if username in users:
                    try:
                        if hasher.verify(users[username].get("hash", ""), password):
                            byte = os.urandom(32)
                            code = base64.urlsafe_b64encode(byte).rstrip(b"=")
                            currentcookie = code.decode("utf-8")
                            cookies[currentcookie] = username
                            currentuser = username
                            print("successful login!")
                            things.remove("login")
                            loginorlogout = False
                            things.append("logout")
                    except:
                        print("invalid login")
                elif username in admins:
                    try:
                        if hasher.verify(admins[username].get("hash", ""), password):
                            byte = os.urandom(32)
                            code = base64.urlsafe_b64encode(byte).rstrip(b"=")
                            currentcookie = code.decode("utf-8")
                            cookies[currentcookie] = username
                            currentuser = username
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
                user = "Anonymous"
            post = input("what do you wanna post?\n>")
            text = input("what do you wanna have as the text?\n>")
            with open("pythonlogin/forums/forumposts.json", "r") as f:
                global what
                what: dict = json.load(f)
            with open("pythonlogin/forums/forumposts.json", "w") as f:
                what[nextpostid - 1] = {
                    "title": post,
                    "text": text,
                    "author": user,
                    "id": nextpostid,
                    "currentid": currentid,
                    "timestamp": dt.astimezone().now().strftime("%d/%m/%y(%a)%H:%M:%S"),
                }
                f.write(json.dumps(what, indent=2))
                forumsposts = what
            nextpostid += 1
            currentid += 1
        case "forums":
            if not cookies.get(currentcookie) in admins:
                for _, text in enumerate(forumsposts.items()):
                    print(
                        f"'{text[1].get("title")}' by {text[1].get("author")} [{text[1].get("timestamp","no timestamp")},Post No.{text[1].get("id")}, No.{text[1].get("currentid")}]"
                    )
                    print(f"    {text[1].get("text")}")
                    commentsection = 1
                    for _, idk in enumerate(forumsreplys.items()):
                        if int(idk[1].get("replyid")) == int(text[1].get("id")):
                            if commentsection == 1:
                                print("----COMMENT-SECTION----")
                            commentsection = 0
                            print(
                                f"    {idk[1].get("author")}: {idk[1].get("text")} [{idk[1].get("timestamp")},Reply No.{idk[1].get("id")}, No.{idk[1].get("currentpostandreplyid")}]"
                            )
                    print(f"    (Reply)")
                if len(forumsposts) != 0:
                    replyornot = input()
                    match replyornot:
                        case "reply":
                            postid = input("Enter the id of the post: ")
                            if forumsposts.get(str(int(postid) - 1)) == None:
                                print(forumsposts)
                                print("there isnt a post with that id")
                                continue
                            replytext = input("Enter the reply: ")
                            with open("pythonlogin/forums/forumreplys.json", "w") as f:
                                forumsreplys[nextreplyid] = {
                                    "text": replytext,
                                    "author": currentuser,
                                    "replyid": postid,
                                    "id": nextreplyid,
                                    "currentpostandreplyid": currentid,
                                    "timestamp": datetime.datetime.now().strftime(
                                        "%d/%m/%y(%a)%H:%M:%S"
                                    ),
                                }
                                f.write(json.dumps(forumsreplys, indent=2))

                            nextreplyid += 1
                            currentid += 1
            else:
                for action in forumsactions:
                    print(action)
                whataction = input(">")
                match whataction:
                    case "delete":
                        for index, text in enumerate(forumsposts.items()):
                            print(
                                f"{text[1].get("id")}: '{text[1].get("title")}' by {text[1].get("author")}"
                            )
                        whichone = int(input(">"))
                        with open("pythonlogin/forums/forumposts.json", "w") as f:
                            forumsposts.pop(whichone - 1)
                            f.write(json.dumps(forumsposts, indent=2))
                        print("successfully removed post")
                    case "view":
                        for _, text in enumerate(forumsposts.items()):
                            print(
                                f"'{text[1].get("title")}' by {text[1].get("author")} [{text[1].get("timestamp","no timestamp")},Post No.{text[1].get("id")}, No.{text[1].get("currentid")}]"
                            )
                            print(f"    {text[1].get("text")}")
                            commentsection = 1
                            for _, idk in enumerate(forumsreplys.items()):
                                if int(idk[1].get("replyid")) == int(text[1].get("id")):
                                    if commentsection == 1:
                                        print("----COMMENT-SECTION----")
                                    commentsection = 0
                                    print(
                                        f"    {idk[1].get("author")}: {idk[1].get("text")} [{idk[1].get("timestamp")},Reply No.{idk[1].get("id")}, No.{idk[1].get("currentpostandreplyid")}]"
                                    )
                            print(f"    (Reply)")
                        if len(forumsposts) != 0:
                            replyornot = input()
                            match replyornot:
                                case "reply":
                                    postid = input("Enter the id of the post: ")
                                    if forumsposts.get(str(int(postid) - 1)) == None:
                                        print(forumsposts)
                                        print("there isnt a post with that id")
                                        continue
                                    replytext = input("Enter the reply: ")
                                    with open(
                                        "pythonlogin/forums/forumreplys.json", "w"
                                    ) as f:
                                        forumsreplys[nextreplyid] = {
                                            "text": replytext,
                                            "author": currentuser,
                                            "replyid": postid,
                                            "id": nextreplyid,
                                            "currentpostandreplyid": currentid,
                                            "timestamp": datetime.datetime.now().strftime(
                                                "%d/%m/%y(%a)%H:%M:%S"
                                            ),
                                        }
                                        f.write(json.dumps(forumsreplys, indent=2))

                                    nextreplyid += 1
                                    currentid += 1
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
