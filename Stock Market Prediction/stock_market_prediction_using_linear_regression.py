#Imports as they should
import pandas as pd
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import train_test_split
from IPython.display import display
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf
import datetime
import math
import re

#PRE PRE PRE Preparing
global df
df=pd.read_csv("train_test_pgd.csv")
df.set_index('Date', inplace=True)
df["CloseForecast"] = df["Close"].shift(-1)
df=df.drop('2022-12-30')

fd=pd.DataFrame()
valdf=pd.DataFrame()
y=pd.DataFrame()
valy=pd.DataFrame()
zsave=[]

#Styling
def prin(DataFrame):
    with pd.option_context('display.max_rows', 8,
                        'display.max_columns', None,
                        'display.width', 1000,
                        'display.precision', 3,
                        'display.colheader_justify', 'center'):
                        display(DataFrame)

def highlight_cols(s):
    color = 'grey'
    return 'background-color: %s' % color


print("Process data, delete columns, create columns, copies of originals")

#1 Load Data
def loaddet():
    print("What Bank would you like to choose?")
    ui = input("Load Dataset?\n").lower()
    if(ui=='y' or ui=='yes'):
      pass
      #Hopefully run some function
    elif(ui=='n' or ui=='no'):
        print("Cool Goodbye Then")
        return False
    else:
      print("Loading",ui)


#3 Operate on Columns
def operate(list,fd):
    global dff
    dff=fd.copy()
    dff['y']=dff[list[0]]
    #print("Gonna fuck working")
    recas(list)
    #print("Still working")
    #print(dff['y'])
    #print(dff.iloc[:,-1])

#3 Operate on Columns 2
def recas(list):
    
    if len(list)==1:
        print("Did it work")
        return False      

    elif list[2] not in dff.columns.tolist():
        print("I hope humanity hasnt come to this")
        if sahil(list[2])==True:
            print("in Sahil")
            dff['z']=float(list[2])
            if list[1]=='+':
                dff['y']=dff['y']+dff['z']
            elif list[1]=='-':
                dff['y']=dff['y']-dff['z']
            elif list[1]=='*':
                dff['y']=dff['y']*dff['z']                   
            elif list[1]=='/':
                dff['y']=dff['y']/dff['z']
        else:
            print("Arey... Kuch to hua hai~ ♫")           

    elif list[1]=='+':
        print("First if l2",list[2])
        dff['y'] = dff['y'] + dff[list[2]]  
        recas(list[2:])
        return

    elif list[1]=='-':
        dff['y']=dff['y'] - dff[list[2]]
        recas(list[2:])
        return

    elif list[1]=='*':
        dff['y']=dff['y'] * dff[list[2]]
        recas(list[2:])
        return 

    elif list[1]=='/':
        dff['y']=dff['y'] / dff[list[2]]
        recas(list[2:])
        return

#Checks for string
def sahil(str):
    try:
        float(str)
        return True
    except:
        return False

#Begins Loop again or Waits for Validation Check
def again():
    print("Begin Again? or Validate? Or.... ;)")
    g=input()

    if g=='yes' or g=='y':
        dfplay(df)
        
    elif g=='v' or g=='validate':
        validatemaster()
    
    else:
        print("GG")

#6 Goes with Recommended settings
def recc():
    global fd,y,zsave
    fd=df.copy()

    #Make Changes as Necessary
    fd['High-Low']=fd['High']-fd['Low']
    fd['Diffv']=fd['Volume'].diff()

    #Drop after diff
    fd=fd.dropna()

    #Assign Y after
    y=fd["CloseForecast"]
    fd=fd.drop(["Adj Close","CloseForecast","High","Low"],axis=1)
    fd=fd.drop(["Open"],axis=1)

    print("Saving")
    zsave=fd.columns.tolist()

#The main Driver Code that allows us to run all functions in an orderly fashion
def dfplay(df):
    state=True
    global fd
    fd=df
    print(fd.head(5))
    while state==True:
        print('\n')
        print("1. View Columns          5. Restart")
        print("2. Drop Columns          6. Recommended")
        print("3. Play with Columns     7. Save")
        print("4. Exit                  8. Train and Result")


        opt = input()

        if opt=='1':
            print(fd.head())
            print('\n')
            print(fd.info())

        elif opt=='2':
            drdf=input("Drop Which?\n")
            try:
                if drdf in list(fd):
                    fd=fd.drop(drdf,axis=1)         


                elif drdf=='e' or drdf=='exit':
                    return

                else:
                    print("Try Again")
            except:
                print("Huh? Something went wrong")

        elif opt=='3':
            try:
                pldf=input("Enter Column and operation")
                pldfl=re.split('(\W)', pldf)
                print("I am pldfl : ",pldfl)

                
                if pldf=='e' or pldf=='exit':
                    return

                elif len(pldfl)==1:
                    print("Kya karu mai")

                else:
                    for _ in range(0,len(pldfl),2):
                        if pldfl[_] not in list(fd) and not sahil(pldfl[_]):
                            print("Spelling Mistake Much?")
                            break
                        else:
                            operate(pldfl,fd)
                            #print("Hola Mola")
                            fd[pldf]=dff['y']
                            fd.head(5)

            except:
                print("You gotta write it like this 'Open/High+Close etc...'")
                pass

        elif opt=='4':
            state=False

        elif opt=='5':
            fd=df
            print('\n'*3)
            print(fd.head(5))


        elif opt=='6':
            print("Going with recommended")
            recc()

        elif opt=='7':
            global zsave
            zsave=fd.columns.tolist()
            print("Save Complete")
        
        elif opt=='8':
            #Begin Training
            print("before func",fd)
            learnmachine()
            state=False
        
        else:
            print("Cmon Man")

#To Load and apply the same settings that was tried to validation to check its performance
def validatemaster():


    def valloaddet():
        global valy,valdf
        print("At lest in valloaddet")

        yf.pdr_override()
        try:
            valdf= pdr.get_data_yahoo('ICICIBANK.NS', '2023-01-01', '2023-02-01')
            print("It didnt Try")
        except:
            print("It didnt Fucking Try")
            valdf=pd.read_csv("icval.csv")
        finally:
            print("It Tried right")
            valdf=pd.read_csv("icval.csv")
            valdf.set_index('Date', inplace=True)

        
        valdf = valdf.dropna()
        valdf["CloseForecast"] = valdf["Close"].shift(-1)

        valy["CloseForecast"]=valdf["CloseForecast"]
        #CHECK WHY THE FUCK ITS NOT REGISTERING VALY nan value
        try:
            valdf.index = valdf.index.strftime('%Y-%m-%d')
        except:
            print("That... Failed, You can continue though")

    def valdat():
            global valdf,zsave,xdfl,valy
            xdfl=[]
            valdfl=valdf.columns.tolist()
            if len(zsave)<=1:
                print("Zsave is 1???")
                recc()

                #Dumbass
            for x in zsave:
                xd=re.split('(\W)', x)
                if len(xd)>1:
                        if xd[1]==' ':
                            valdf=valdf.drop(x,axis=1)

                if x=='Diffv':
                    valdf['Diffv']=valdf['Volume'].diff()
                    valdf["CloseForecast"]=valy["CloseForecast"]
                    valy=valy.drop("CloseForecast",axis=1)
                    valdf=valdf.dropna()
                    valy["CloseForecast"]=valdf["CloseForecast"]
                    print(valy)
                    continue
                else:
                    xdfl.append(xd)

            for k in xdfl:
                if type(k) is list and len(k)!=1:
                    operate(k,valdf)
                    print("Good here as well operate xdfl,valdfl")
                    valdf[''.join(k)]=dff['y']


            for l in valdfl:
                if l in zsave:
                    #print("In Zsave hence continue")
                    continue
                
                elif l not in zsave:
                    valdf=valdf.drop(l,axis=1)

            #Sorting
            valdf = valdf[zsave]

            print("valdf\n",valdf)

    def valrun(valdf):
        global valy
        valdf=valdf.dropna()
        valy=valy.dropna()
        tp=pd.DataFrame()
        print("Valy cf",valy)
        print("Valy cf",valy.info())

        print("Valdf",valdf)

        tp["ActualForecast"]=valy['CloseForecast']
        #valdf.drop("CloseForecast",axis=1)

        print("valdf\n",valdf)
        print("tp\n",tp)
        try:
            valypred=reg.predict(valdf)
        except:
            print('-'*40)
            print("No reg")
            print('-'*40)

        else:
            tp.index = valdf.index
            tp["Predicted"]=valypred

            valdf["CloseForecast"]=tp["ActualForecast"]
            valdf["Predicted"]=tp["Predicted"]


            display(valdf.style.set_properties(subset=['CloseForecast',"Predicted"], **{'background-color': 'green'},axis=0))
            valdf.to_csv("Repval.csv")




            #print

            print('-'*40)
            print("ROOT MEAN SQUARE :",mse(tp["ActualForecast"],tp["Predicted"],squared=True))
            print('-'*40)


            tp['ActualForecast'].plot(figsize=(10,7))
            tp['Predicted'].plot(figsize=(10,7))
            plt.show()


    valloaddet()
    print("In Valdat")
    valdat()
    print("Loaded, Running Reg")
    valrun(valdf)
    print("Done?")

#Prepares Data to be sent so that a model can be trained upon it
def learnmachine():
    #First Assign Y
    global fd,zsave,y
    
    print(fd)

    if len(zsave)<=1:
        recc()

    try:
        y=fd["CloseForecast"]
        fd=fd.drop("CloseForecast",axis=1)
    except:
        print("Exists")

    
    #Assign X then split
    try:
        x=fd
        print("X AND Y",x,y)
        x_train, x_test,y_train,y_test=train_test_split(x,y,test_size=0.1,shuffle=False)

    except:
        print("Error has occured in split... Stopping now")

    else:
        whynot(x_train,y_train,x_test,y_test)
        again()
        
#Function That consists of the Regression models
def whynot(x_train,y_train,x_test,y_test):

    #linear Regeression
    #Just linear Regression No tricks

    global reg
    reg = linear_model.LinearRegression()
    reg.fit(x_train, y_train)

    print("Linear test",reg.score(x_test,y_test))
    print("Linear train",reg.score(x_train,y_train))

    ypred=reg.predict(x_test)
    tp=pd.DataFrame()

    tp.index = y_test.index
    tp["lypred"]=ypred
    tp["yact"]=y_test


    #print
    xyz=pd.DataFrame({'coef':reg.coef_, 'category':x_test.columns}).sort_values(by = 'coef', ascending = False).set_index('category')
    display(xyz)
    print('-'*40)
    print("ROOT MEAN SQUARE :",mse(y_test,ypred,squared=True))
    print('-'*40)
    prin(tp)



    tp['lypred'].plot(figsize=(10,7))
    tp['yact'].plot(figsize=(10,7))
    plt.show()




try:
    aj=loaddet()
except:
    display("Could not load Data")
else:
    if aj==False:
      pass
    else:
      dfplay(df)






# print("What models to Apply? Just Linear, Ridge and Lasso")

# print("Linear, Then Get accuracy, not by Precision but by RMSE, Then plot")

# print("Shift check")

# print("Elastinets")







