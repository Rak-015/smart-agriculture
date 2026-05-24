from django.shortcuts import render ,redirect
from django.contrib import messages
# Create your views here.
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from keras.models import load_model
from .models import *
from django.http import HttpResponse
from sklearn.neighbors import KNeighborsClassifier
import cgi
import cgitb;cgitb.enable() 
from app.forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User 
from django.contrib import messages 
from django.contrib.auth import authenticate, login 
from app.models import Soil_History, Crop_History, Plant_History



def index(request):

    return render(request, 'index.html') 

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data.get('fullname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password') 
            confirm_password = form.cleaned_data.get('confirm_password')

            if password != confirm_password:
                messages.error(request, "Password and Confirm Password not matched")
                return redirect('register')

            if User.objects.filter(username=email).exists():
                messages.error(request, "This Email Id is already Exists, try another")
                return redirect('register')

            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name=fullname
            user.save()
            messages.success(request, "Registration Successfull")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            if email == 'admin@gmail.com' and password == 'admin':
                return redirect('admin1')

            mail = User.objects.filter(username=email).first()
            
            if mail:
                user = authenticate(request, username=email, password=password)
                if user:
                    login(request, user)
                    return redirect('index')
                else: 
                    messages.error(request, "Invalid Password, Try Again")
                    return redirect('login')
            else: 
                messages.error(request, "This Email Id does not exists, Please Register")
                return redirect('login')                 
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})


def about(request):

    return render(request, 'about.html')
import random
#soil prediction
def soilprediction(request):

    global x_train, x_test, y_train, y_test, x, y

   
    if request.method == 'POST':
        df = pd.read_csv(r'datasets\data.csv')
        le = LabelEncoder()
        df['Output'] = le.fit_transform(df['Output'])
        x = df.iloc[:, :-1]
        y = df.iloc[:, -1]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=72)

        pH = float(request.POST['pH'])
        EC = float(request.POST['EC'])
        OC = float(request.POST['OC'])
        OM = float(request.POST['OM'])
        N = float(request.POST['N'])
        P = float(request.POST['P'])
        K = float(request.POST['K'])
        Zn = float(request.POST['Zn'])
        Fe = float(request.POST['Fe'])
        Cu = float(request.POST['Cu'])
        Mn = float(request.POST['Mn'])
        Sand = float(request.POST['Sand'])
        Silt = float(request.POST['Silt'])
        Clay = float(request.POST['Clay'])
        CaCO3 = float(request.POST['CaCO3'])
        CEC = float(request.POST['CEC'])
        p = 0.5
        xgp = p>=np.random.rand()
        PRED = [[pH, EC, OC, OM, N, P, K, Zn, Fe,Cu, Mn, Sand, Silt, Clay, CaCO3, CEC]]

        knn = RandomForestClassifier()
        knn.fit(x_train, y_train)
        xgp = np.array(knn.predict(PRED))
        

        if xgp == 0:
            msg = ' This prediction result is : Non Fertile'
            fertilizers = [
                'Nitrogen-rich fertilizers: Urea, Ammonium Nitrate',
                'Phosphorus fertilizers: Superphosphate, Ammonium Phosphate',
                'Potassium fertilizers: Potash, Muriate of Potash',
                'Organic fertilizers: Compost, Manure'
            ]
             # Randomly choose one fertilizer recommendation
            recommended_fertilizer = random.choice(fertilizers)
            fertilizers = [recommended_fertilizer]  # Assign the selected fertilizer to the list
        elif xgp == 1:
            msg = ' This prediction result is : Fertile'
            fertilizers = [] 
        queryset = Soil_History(prediction=msg, fertilizer=fertilizers)
        queryset.save()
        return render(request, 'soilprediction.html', {'msg': msg, 'fertilizers': fertilizers})
    return render(request, 'soilprediction.html')


#crop predictiopn
def croppredictiopn(request):
    df=pd.read_csv("datasets/Crop_recommendation.csv")
    global x_trains,y_trains
    le=LabelEncoder()
    df['label'] = le.fit_transform(df['label'])
    x = df.drop(['label'], axis=1)
    y = df['label']

    x_trains, x_tests, y_trains, y_tests = train_test_split(x,y, stratify=y, test_size=0.3, random_state=42)
   
    if request.method == "POST":
        f1 = float(request.POST['N'])
        print(f1)
        f2 = float(request.POST['P'])
        print(f2)
        f3 = float(request.POST['K'])
        print(f3)
        f4 = float(request.POST['temperature'])
        print(f4)
        f5 = float(request.POST['humidity'])
        print(f5)
        f6 = float(request.POST['ph'])
        print(f6)
        f7 = float(request.POST['rainfall'])
        print(f7)

        li = [[f1,f2,f3,f4,f5,f6,f7]]
        print(li)
        
        logistic = RandomForestClassifier()
        logistic.fit(x_trains, y_trains)
        
        result =logistic.predict(li)
        result=result[0]
        if result == 0:
            msg = 'The Recommended Crop is predicted as Carrot'
        elif result == 1:
            msg = 'The Recommended Crop is predicted as Potato'
        elif result == 2:
            msg = 'The Recommended Crop is predicted as Tomato'
        elif result == 3:
            msg = 'The Recommended Crop is predicted as Cucumber'
        elif result == 4:
            msg = 'The Recommended Crop is predicted as Spinach'
        elif result == 5:
            msg = 'The Recommended Crop is predicted as Lettuce'
        elif result == 6:
            msg = 'The Recommended Crop is predicted as Onion'
        elif result == 7:
            msg = 'The Recommended Crop is predicted as Cauliflower'
        elif result == 8:
            msg = 'The Recommended Crop is predicted as Brinjal (Eggplant)'
        elif result == 9:
            msg = 'The Recommended Crop is predicted as Peas'
        elif result == 10:
            msg = 'The Recommended Crop is predicted as Chili'
        elif result == 11:
            msg = 'The Recommended Crop is predicted as Beans'
        elif result == 12:
            msg = 'The Recommended Crop is predicted as Bell Pepper'
        elif result == 13:
            msg = 'The Recommended Crop is predicted as Cabbage'
        elif result == 14:
            msg = 'The Recommended Crop is predicted as Sweet Potato'
        elif result == 15:
            msg = 'The Recommended Crop is predicted as Zucchini'
        elif result == 16:
            msg = 'The Recommended Crop is predicted as Radish'
        elif result == 17:
            msg = 'The Recommended Crop is predicted as Kale'
        elif result == 18:
            msg = 'The Recommended Crop is predicted as Mushroom'
        elif result == 19:
            msg = 'The Recommended Crop is predicted as Garlic'
        elif result == 20:
            msg = 'The Recommended Crop is predicted as Corn'
        elif result == 21:
            msg = 'The Recommended Crop is predicted as Lettuce' 
        
        queryset = Crop_History(crop=msg)
        queryset.save()

        
        return render(request,'croppredictiopn.html',{'msg':msg})
   
    return render(request, 'croppredictiopn.html')


#plant prediction
def plantprediction(request):

    return render(request, 'plantprediction.html')

Plants = ['Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___healthy', 'Corn_(maize)___Northern_Leaf_Blight', 'Potato___Early_blight',
            'Potato___healthy', 'Potato___Late_blight', 'Tomato___Bacterial_spot', 'Tomato___healthy', 'Tomato___Late_blight', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus']

def result(request):
    if request.method == 'POST':
        print("hdgkj")
        m = int(request.POST["alg"])
        acc = pd.read_csv("app\Accuracy.csv")
        file = request.FILES['file']
        full_path = os.path.join('app\static\img', file.name)
        # Ensure the directories leading up to the file exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Save the file
        with open(full_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        path = f'app/static/img/{file.name}'
        print(path)
        print('hjhdfakjhdaf-=-=-=-=-')

    

        if m == 2:
            print("bv2")
            new_model = load_model('app/models/ANN.h5')
            test_image = image.load_img(path, target_size=(128, 128))
            test_image = image.img_to_array(test_image)
            test_image /=255
            a = acc.iloc[m - 1, 1]

        elif m == 3:
            print("bv2")
            new_model = load_model('app/models/CNN.h5')
            test_image = image.load_img(path, target_size=(128, 128))
            test_image = image.img_to_array(test_image)
            test_image /=255
            a = acc.iloc[m - 1, 1]

        else:
            print("bv3")
            new_model = load_model('app/mobilenet.h5')
            test_image = image.load_img(path, target_size=(128, 128))
            test_image = image.img_to_array(test_image)
            test_image /=255
            a = acc.iloc[m - 1, 1]

        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)
        preds = Plants[np.argmax(result)]

        if preds == "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot":
            msg = "Foliar fungicides can be used to manage gray leaf spot outbreaks"

        elif preds == "Corn_(maize)___Common_rust_":
            msg = "Use resistant varieties like DHM 103, Ganga Safed - 2 and avoid sowing of suceptable varieties like DHM 105"

        elif preds == "Corn_(maize)___healthy":
            msg = "Plant is Good no treatment required"

        elif preds == "Corn_(maize)___Northern_Leaf_Blight":
            msg = "Integration of early sowing, seed treatment and foliar spray with Tilt 25 EC (propiconazole) was the best combination in controlling maydis leaf blight and increasing maize yield"

        elif preds == "Potato___Early_blight":
            msg = "Mancozeb and chlorothalonil are perhaps the most frequently used protectant fungicides for early blight management"

        elif preds == "Potato___healthy":
            msg = "Plant is Good no treatment required"

        elif preds == "Potato___Late_blight":
            msg = "Effectively managed with prophylactic spray of mancozeb at 0.25% followed by cymoxanil+mancozeb or dimethomorph+mancozeb at 0.3% at the onset of disease and one more spray of mancozeb at 0.25% seven days"

        elif preds == "Tomato___Bacterial_spot":
            msg = "When possible, is the best way to avoid bacterial spot on tomato. Avoiding sprinkler irrigation and cull piles near greenhouse or field operations, and rotating with a nonhost crop also helps control the disease"

        elif preds == "Tomato___healthy":
            msg = "Plant is Good no treatment required"

        elif preds == "Tomato___Late_blight":
            msg = "Ungicides that contain maneb, mancozeb, chlorothanolil, or fixed copper can help protect plants from late tomato blight"

        else:
            msg = "Homemade Epsom salt mixture. Combine two tablespoons of Epsom salt with a gallon of water and spray the mixture on the plant"
        
    

        path1 = f'/static/img/{file.name}' 
        queryset = Plant_History(upload_image=path1, prediction=msg)
        queryset.save()
        print(path1)
        return render(request, "result.html", {'text': preds, 'a': round(a*100, 3), 'path': path1 ,'msg': msg})

    return render(request, 'result.html') 

def admin_panel(request):
    return render(request, 'admin.html')

def view_user(request): 
    user = User.objects.all()
    return render(request, 'view_user.html', {'user': user})

def soil_history(request):
    soil = Soil_History.objects.all()
    return render(request, 'soil_history.html', {'soil':soil})

def crop_history(request):
    crop = Crop_History.objects.all()
    return render(request, 'crop_history.html', {'crop':crop})

def plant_history(request):
    plants = Plant_History.objects.all()
    return render(request, 'plant_history.html', {'plants':plants})
