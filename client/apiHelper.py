import requests, json
import variables, pymongo
from pymongo import MongoClient
from bson.json_util import dumps
from requests.auth import HTTPBasicAuth

client = MongoClient()
db = client['gochat']
user = db['user']
user.ensure_index('username',unique=True)

def checkUser(username):
    url = variables.AWSEndPoint + "/checkUser"
    data = {"username": username}
    json_data = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    return response.text

def registerUser(username, password):
    url = variables.AWSEndPoint + "/registerUser"
    data = {"username": username, "password": password}
    json_data = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    try:
        db.user.insert_one({'username':username, 'password': (password)})
    except:
        print "nononono"

    return response.text

def deleteUser(username,password):
	storedHashPassword = db.user.find_one({'username':username})

	if storedHashPassword['password'] == (password):
		requests.get(variables.AWSEndPoint + '/removeUser', auth=(username, password))
		db.user.drop()
		return True
	else:
		return False

def sendMessage(recipient, message):
	selfUser = db.user.find_one()
	selfUserName = selfUser['username']
	selfPassword = selfUser['password']

	url = variables.AWSEndPoint + "/newMessage"
	data = {"to": recipient, "message": message}
	json_data = json.dumps(data)
	headers = {'Content-type': 'application/json'}
	response = requests.post(url, auth=(selfUserName, selfPassword), data=json_data, headers=headers)

	return response.text



def hash_pass(password):
    # used to hash the password similar to how MySQL hashes passwords with the password() function.
    import hashlib
    hash_password = hashlib.sha1(password.encode('utf-8')).digest()
    hash_password = hashlib.sha1(hash_password).hexdigest()
    hash_password = '*' + hash_password.upper()
    return hash_password


