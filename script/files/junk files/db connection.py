import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('apka-gieldowa-firebase-adminsdk-vohou-f865fa2fae.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://apka-gieldowa.firebaseio.com'
})



root = db.reference('Main')
root_days = db.reference('Main/Dates')

#print(default_app.name)
# Add a new user under /users.
#new_user = root.push({
#    'name' : 'Mary Anning',
#    'since' : 1700
#})

company_name = 'KREZUS'
company_name_2 = 'KREZUS_2'

day_1 = '23'
day_2 = '24'

post_ref = root_days

record_1 = post_ref.push({company_name: {
         'date_of_birth': 'June 23, 1912',
         'full_name': 'Alan Turing'}})

record_2 = post_ref.push({company_name: {
         'date_of_birth': 'June 24, 1913',
         'full_name': 'Alana Turing'}})

record_3 = post_ref.push({company_name: {
         'date_of_birth': 'June 25, 1914',
         'full_name': 'Alan Turing'}})

print(str(record_1.key) + " " + str(record_2.key) + " " + str(record_3.key))
print (root.get(0))

for key in root_days.get():
    print ('Key {0}'.format(key))

