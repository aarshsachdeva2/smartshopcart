####################   1   #####################################

import numpy as np 
import pandas as pd 

from sklearn import linear_model

from random import randrange
import requests
import warnings
warnings.filterwarnings("ignore")
count=0



def senddata(userData):
  print(userData)
  url = 'http://192.168.43.44:7000/insert'
  x = requests.post(url, data=userData)
  print(x.text)


import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
cap = cv2.VideoCapture(0)



X_train = np.genfromtxt("C:/Users/jituc/OneDrive/Desktop/major project/resourcefiles/xtrain2.csv" , delimiter = ",")
Y_train=np.genfromtxt("C:/Users/jituc/OneDrive/Desktop/major project/resourcefiles/ytrain2.csv" , delimiter = ",")
codes=pd.read_csv("C:/Users/jituc/OneDrive/Desktop/major project/resourcefiles/codes.csv")





logreg=linear_model.LogisticRegression()
logreg.fit(X_train,Y_train);


code=codes[['code']]
name=codes[['name']]
code=np.array(code)
name=np.array(name)


prev=""
cur=""





def product():
  global cur
  global prev
  # Read image
  while(1):
    cv2.waitKey(10)
    ret,im = cap.read()
    if ret == True:
      cv2.imshow('Frame',im)
      decodedObjects = pyzbar.decode(im)
      if len(decodedObjects)>0:
        cur=str(decodedObjects[0].data)
        if cur!=prev:
          #print(cur)
          prev=cur
          cv2.destroyAllWindows()
          return cur[2:len(cur)-1]




def input_function(length,input_string):
    input_test=[]
    name_of_item=input_string
    flag=0
    
    for  i in range(len(code)):
        if name_of_item==name[i]:
            flag+=1
            number=i
            if flag==0:
                print('not found')
    if flag!=0:   
        code_of_item=int(code[number])
        code_digits=[int(i) for i in str(code_of_item)]
        
        for i in range(length):
            x=code_digits[i]
            input_test.append(x)

        input_test_array=np.array(input_test)
        input_test_array_1 = np.c_[input_test_array , np.ones(len(input_test_array))]
        input_test_array_transpose=np.ndarray.transpose(input_test_array_1)

        input_test_array_transpose = input_test_array_transpose.astype(float)
        Y_pred=logreg.predict(input_test_array_transpose)
        Y_pred=np.array(Y_pred)
        Y_pred=Y_pred[0]
        return Y_pred;
    else:
        return "n"






def recommended_items(Y_pred,input_string):
    path="C:/Users/jituc/OneDrive/Desktop/major project/resourcefiles/recommended_items/" + str(Y_pred)+ ".csv"
    
    recommended_item_list=pd.read_csv(path)
    recommended_item_list=np.array(recommended_item_list)
    name_of_item=input_string
    
    for i in range(len(recommended_item_list)):
        if name_of_item== recommended_item_list[i]:
            index=i
            recommended_item_list = np.delete(recommended_item_list, index)
            break



    return recommended_item_list

def mains():
    ans='n'
    length=3;
    flag=True;
    global count
    input_string=product()
    datas=input_string.split(':')
    print(datas)
    userData = {};
    if len(datas)>1:
      price=int(datas[1])
      input_string=datas[0]
    else:
      flag=False;
      print("use proper text format for generation of qrcode")
    #input_string="paneer"
    Y_pred=input_function(length,input_string);
    if Y_pred=="n":
        print(input_string+": Item not in store/found")
    else:
        Y_pred=int(Y_pred)
        count=count+1
        recommended_items_list=recommended_items(Y_pred,input_string)
        if flag:
          userData["code"]=1
          userData["product"]=input_string
          userData["price"]=price
          userData["info"]=str(recommended_items_list)
          senddata(userData)
          
while(1):
    mains()
    
    



