
from Pyrebase import pyrebase


config = {  "apiKey": "AIzaSyAp_dUis7EoVCPnatbpSwbx0HYG5nDUVss",
            "authDomain": "pulpapp-1555504377247.firebaseapp.com",
            "databaseURL": "https://pulpapp-1555504377247.firebaseio.com",
            "storageBucket": "pulpapp-1555504377247.appspot.com",
            "serviceAccount": "pulpapp-1555504377247-6e7b0411fe4b.json"
            }
firebase = pyrebase.initialize_app(config)


auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
#authenticate a user
user = auth.sign_in_with_email_and_password("pythontest@gmail.com", "pythontest")
token = user['idToken']

archer = {"name": "Sterling Archer", "agency": "Figgis Agency"}
#db.child("agents").push(archer, user['idToken'])
print(user)

lana = {"name": "Lana Kane", "agency": "Figgis Agency"}
#db.child("agents").child("Lana").set(lana, user['idToken'])

all_agents = db.child("agents").get(user['idToken']).val()



lana_data = db.child("agents").child("Lana").get(user['idToken']).val()
print(lana_data)

print(storage.get_url(token=token))
bucket = storage.bucket
print(storage.__dir__())
# print(storage.download(token=token,filename='/users/infosec.PNG'))
print(storage.child('users/GioTest.jpg').put('Gio.jpg',token))
#storage.put(token=token,file='Gio.jpg')
file1 = open("prova.csv", "w")
for x in storage.list_files():
    print(x)

#storage.download('users/cuzzygio.csv',token);
#storage.download(token=token,filename="allow.PNG")


#file1.write(storage.child('users/').download('cuzzygio.csv',token))
storage.child('users/GioTest.jpg').download('GioTest1.jpg',token)
file1.close()
