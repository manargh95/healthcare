import codecs
import re
import webbrowser

import os

from firebase_admin import credentials, initialize_app, firestore
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'



DATA_REQUEST_REGISTER="healthcareRequestregister"
DATA_REQUEST_LOGIN="healthcareRequestlogin"
DATA_REQUEST_EDIT="healthcareRequestedit"

#Flask App Initialization
app = Flask(__name__)
api=Api(app)


@app.route("/")
def index():
    return "Welcome"

webbrowser.open('file://' + os.path.realpath("sample.html"))
#Firestore DB Initialization
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
# question is the targeted Collection
todo_ref = db.collection('User')

#Data coming from Application post request
class registerAPI(Resource):
    def post(self):
        name=request.json["name"]
        email=request.json["email"]
        password=request.json["password"]
        return create(name,email,password)

class loginAPI(Resource):
    def post(self):
        email= request.json['email']
        password= request.json['password']
        return read(email,password)

class updateAPI(Resource):
    def post(self):
        email = request.json['email']
        password = request.json['password']
        new_email = request.json['new_email']
        new_password = request.json['new_password']
        new_name = request.json['new_name']
        return edit(email,password,new_name,new_email,new_password)


#Register ModelRequest as a resource
api.add_resource(registerAPI,"/"+DATA_REQUEST_REGISTER)
api.add_resource(loginAPI,"/"+DATA_REQUEST_LOGIN)
api.add_resource(updateAPI,"/"+DATA_REQUEST_EDIT)



@app.route('/register', methods=['GET','POST'])
def create(name,email,password):
    try:
        if (re.search(regex,email)):
            if(len(password)>5):
                todo_ref.add({'name': name,
                             'email': email, 'password': password})
                return {"status":"Register done successfully"}
            else:
                return {"status":"Password must be more than 5 digits"}
        else:
             return {"status":"Invalid Email!"}

    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/login', methods=['GET','POST'])
def read(email,password):
    docs = todo_ref.get()
    for doc in docs:
        if(u'{}'.format(doc.to_dict()['email'])==email and
                   u'{}'.format(doc.to_dict()['password']) == password):
            return {"email:":email,"password:":password}

    return {"status:":"Your email or password is wrong"}

@app.route('/edit')
def edit(email,password,new_name,new_email,new_password):
    if re.search(regex, new_email):
        if len(new_password) >5:
            result= todo_ref.where ('email','==',email)\
                            .where('password','==',password).get()
            field_update =\
                {"email": new_email,"password":new_password,"name":new_name}
            for item in result:
                doc = todo_ref.document(item.id)
                doc.update(field_update)
            return {"status":"You personal data updated successfully"}
        else:
            return {"status":"Password must be more then 5 digits"}
    else:
        return {"status":"Invalid email"}


if __name__=="__main__":
    app.run(debug=True)


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello this is the new version!"