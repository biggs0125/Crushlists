from pymongo import Connection
import re

def conn():
    connection = Connection('mongo2.stuycs.org')
    db = connection.admin
    res = db.authenticate('ml7','ml7')
    db = connection['crushlists']
    return db

def clearDB():
    db = conn()
    db.students.remove()

def addUserInfo(name,username,password):
    db = conn()
    regx = re.compile("^"+name,re.IGNORECASE)
    r = [x for x in db.students.find({'name':regx})]
    if r[0].has_key('username'):
        return False
    else:
        db.students.update({"name": name}, {"$set": {"username": username,"password":password}})
        return True

def addPerson(name,crushlist,*args):
    db = conn()
    if len(args) > 0:
        d = {'name':name, 'crushlist':crushlist, 'username':args[0], 'password':args[1]}
    else:
        d = {'name':name, 'crushlist':crushlist}
    regx = re.compile("^"+name,re.IGNORECASE)
    r = [x for x in db.students.find({'name':regx})]
    if len(r) > 0:
        if d.has_key('username'):
            db.students.update({'name':name},d)
        else:
            db.students.update({'name':name},{'$set' : {'crushlist':crushlist}})
    else:
        db.students.insert(d)

def getPeopleYouLike(name):
    db = conn()
    regx = re.compile("^"+name,re.IGNORECASE)
    r = [x for x in db.students.find({'name':regx})]
    if len(r) == 0:
        return ["You have not submitted a crushlist","Or you might need to add a last name or try capitalizing/uncapitalizing the name"]
    else:
        a = r[0]
        return a['crushlist']
        
def getPeopleWhoLikeYou(name):
    db = conn()
    r = [x for x in db.students.find()]
    yours = []
    for person in r:
        for x in person['crushlist']:
            if x.lower() == name.lower():
                yours.append(person['name'])
    if len(yours) == 0:
        return ["No one has put you on their crushlist", "Or you might need to type your name differently or try capitalizing/uncapitalizing the name"]
    return yours

def getName(username,password):
    db = conn()
    r = [x for x in db.students.find()]
    for person in r:
        if person.has_key('username'):
            if person['username'] == username:
                if person['password'] == password:
                    return person['name']
    return 0

def getAllPeople():
    db = conn()
    r = [x for x in db.students.find()]
    l = [x['name'] for x in r]
    return l

def printAll():
    db = conn()
    r = [x for x in db.students.find()]
    l = [[x['name'],x['crushlist']] for x in r]
    for x in l:
        print x[0]
        print x[1]

def printUserInfo(username):
    db = conn()
    r =  db.students.find_one({'name':username})
    print r

def removeUser(name):
    db = conn()
    db.students.remove({'name':name})


#### Re-hashing the db

def addUser(name,username,password):
    db = conn()
    regx = re.compile("^"+name,re.IGNORECASE)
    d = {'name':regx,'username':username,'password':password}
    r = [x for x in db.users.find({'name':name})]
    if len(r) == 0:
        db.users.insert(d)
    else:
        return "User Already Exists"

def addPerson2(name,crush,year):
    db = conn()
    d = {'name':name,'crush':crush,'year':year}
    r = [x for x in db.people.find({'name':name})]
    print r

def getPeopleYouLike2(name):
    db = conn()
    regx = re.compile("^"+name,re.IGNORECASE)
    r = [x for x in db.people.find({'name':regx})]
    l = [[x['crush'],x['year']] for x in r]
    return l

def getPeopleWhoLikeYou2(name):
    db=conn()
    regx = re.compile("^"+name,re.IGNORECASE)
    r = [x for x in db.people.find({'crush':regx})]
    l = [x['name'] for x in r]
    return l


#printAll()



