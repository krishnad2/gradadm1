import streamlit as st 
import numpy as np 
import pandas as pd
import time
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import random
random.seed(1234)
st.title('Streamlit App for Graduate Admissions')

menu_option = st.sidebar.radio(
    'Select Option',
    ('About', 'Explore Data',"R F Model","Top Students","Imp Variables","Probabilities")
)

df = pd.read_csv("./binary.csv")
X= df.drop('admit',axis=1)
y=df['admit']
rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
rf=rf.fit(X, y)

def about():
  f=open("./About.txt","r")
  t=f.read()
  return t

def data_explore():
  return df

def get_data():
  return X,y

def compute_rfresults():
  return rf 

def top_students_prob():
  pred=rf.predict_proba(X)
  preddf=pd.DataFrame(pred,columns=['prob0','Probability'])
  preddf['Stno']=preddf.index+1
  preddf1=preddf[preddf['Probability']>0.5]
  return(preddf1) 
 
if(menu_option == "About") :
    t=about()
    st.text(t)
elif(menu_option == "Explore Data") :   
    df=data_explore()
    st.text("Explore Data")
    st.dataframe(df)
elif(menu_option == "R F Model") :
    st.write("Random Forest Model results ")
    rf=compute_rfresults() 
    st.text(rf)
    X,y = get_data() 
    predicted = rf.predict(X)
    accuracy = accuracy_score(y, predicted)
    st.write('Out-of-bag score estimate:', rf.oob_score_)
    st.write('Mean accuracy score:', accuracy)
    st.text("Confusion Matrix")
    m=metrics.confusion_matrix(y,predicted)
    st.write(m)
elif(menu_option == "Top Students") :  
    st.write("Students with High Probability")
    preddf2 = top_students_prob()
    preddf2=preddf2[['Stno','Probability']]
    preddf3=preddf2.sort_values(by=['Probability'],ascending=False)
    st.dataframe(preddf3)
elif(menu_option == "Imp Variables") :  
    st.write("Important Varialbes")  
    rf=compute_rfresults()
    # Get Importance
    importance=rf.feature_importances_
    X,y=get_data()
    var=pd.Series(X.columns)
    Score=pd.Series(importance)
    varimpdf=pd.concat([var,Score],axis=1)
    varimpdf.columns=['var','Score']
    varimpdf.sort_values(by=['Score'],inplace=True, ascending=False)
    varimpdf=varimpdf.iloc[:,:10]
    df1=varimpdf.head(10)
    fig, ax = plt.subplots()
    ax.barh(df1['var'],df1['Score'])
    ax.set_xlabel("Score")
    ax.set_ylabel('Variable')
    ax.set_title('Variables Importnce')
    col1, col2 = st.beta_columns(2)
    col1.header("Important Variables")
    col1.dataframe(varimpdf)
    col2.header("Important Variables Plot")
    col2.pyplot(fig)
elif(menu_option == "Probabilities") :  
    st.write("Admission Probabilities") 
    rf=compute_rfresults()
    X, y=get_data()
    pred=rf.predict_proba(X)
    preddf=pd.DataFrame(pred,columns=['prob0','Probability'])
    sno=pd.Series(range(1,400))
    preddf['stno']=sno
    preddf['gre']=X['gre']
    preddf['gpa']=X['gpa']
    preddf['rank']=X['rank']
    preddf1=preddf[['stno','gre','gpa','rank','Probability']]
    st.dataframe(preddf1)
else:
    st.text(menu_option)
    st.text("Over")    
     
    
     
 