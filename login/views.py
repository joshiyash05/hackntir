from django.shortcuts import render
import pyrebase
# Create your views here.

import firebase_admin
from firebase_admin import credentials,firestore,auth

cred = credentials.Certificate("serviceAccountKey.json")
config={
  "apiKey": "AIzaSyCnqJQ8krxzMk4qcxt-Sg3hsIzTSpQW3ME",
  "authDomain": "fir-9ca93.firebaseapp.com",
  "databaseURL": "https://fir-9ca93-default-rtdb.firebaseio.com",
  "projectId": "fir-9ca93",
  "storageBucket": "fir-9ca93.appspot.com",
  "messagingSenderId": "977749723231",
  "appId": "1:977749723231:web:e04659b86a921f56f673ea",
}
try:
    firebase_admin.get_app()
except ValueError as e:
    firebase_admin.initialize_app(cred)

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database = firestore.client()

def signIn(request):
    return render(request,"Login.html")
def home(request):
    return render(request,"Home.html")
 
def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    
    
    try:
        # if there is no error then signin the user with given email and password
        user = authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"Login.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    
    
    
    return render(request,"Home.html",{"email":email})
 
def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"Login.html")
 
def signUp(request):
    return render(request,"Registration.html")
 
def postsignUp(request):
     email = request.POST.get('email')
     passs = request.POST.get('pass')
     name = request.POST.get('name')
     phone= request.POST.get('Phone')
     div= request.POST.get('Div')
     year= request.POST.get('Currentyear')
     sapid= request.POST.get('Sapid')
     database.collection('Registration').document(name).set({'name':name,'phone':phone,'Sapid':sapid,'Div':div,'year':year,'email':email})
     try:
        # creating a user with the given email and password
        user=auth.create_user(email=email,password=passs,display_name=name)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
     except:
        return render(request, "Registration.html")
     
     
     return render(request,"Login.html")
