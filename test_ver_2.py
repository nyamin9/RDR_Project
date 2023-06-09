import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

import warnings
warnings.filterwarnings(action = 'ignore')

ID_RNN_list = []

user = st.text_input('ID를 입력하세요 : ')
password = st.text_input('패스워드를 입력하세요 : ')

st.write('')
st.write('')

#####################################################################################################################################################

# 환자 개인 정보 테이블 불러오기

def main1():
    try:
        connection = mysql.connector.connect(
            host = '115.137.160.190',
            database = 'drugdb',
            user = user,
            password = password,
            port = 3306
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary = True)
            query = """ select patientID, pRNN, age from patient_info; """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            for row in results:
                #st.write(row)
                ID_RNN_list.append(row)
            
            
            #ID_RNN = pd.DataFrame(cursor.fetchall())
            #ID_RNN = ID_RNN.rename(columns = {0 : 'patientID', 1 : 'pRNN', 2 : 'age'})
            #ID_RNN['patientID'] = ID_RNN['patientID'].astype('str')
            
    except Error as e:
        st.write("ERROR!!", e)
        
        
    finally:
        cursor.close()
        connection.close()
        #print("CONNECTION ENDED")
        

if __name__ == '__main1__':
  main1()
    
ID_RNN = pd.DataFrame(ID_RNN_list)
    
#patientID의 type 변경
ID_RNN['patientID'] = ID_RNN['patientID'].astype('str')

#####################################################################################################################################################

# 환자 처방 정보 입력

def main2():
    try:
        connection = mysql.connector.connect(
            host = '115.137.160.190',
            database = 'drugdb',
            user = user,
            password = password,
            port = 3306
        )
        
        if connection.is_connected():
            
            patientID = st.text_input('환자 ID를 입력하세요 : ')
            hosID = st.text_input('병원 ID를 입력하세요 : ')
            drugID = st.text_input('약물 ID를 입력하세요 : ')
            doctorID = st.text_input('의사 ID를 입력하세요 : ')
            prescription_amount = st.text_input('처방량을 입력하세요 : ')
            
            cursor = connection.cursor(dictionary = True)
            query = """ insert into prescription_record(patientID, hosID, drugID, doctorID, prescription_amount) values (%s, %s, %s, %s, %s); """
            record = (patientID, hosID, drugID, doctorID, prescription_amount)
            
            cursor.execute(query, record)
            connection.commit()
            
            
            #ID_RNN = pd.DataFrame(cursor.fetchall())
            #ID_RNN = ID_RNN.rename(columns = {0 : 'patientID', 1 : 'pRNN', 2 : 'age'})
            #ID_RNN['patientID'] = ID_RNN['patientID'].astype('str')
            
    except Error as e:
        st.write("ERROR!!", e)
        
        
    finally:
        cursor.close()
        #connection.commit()
        connection.close()
        #print("CONNECTION ENDED")
        

if __name__ == '__main2__':
  main2()
    
    
#####################################################################################################################################################

# 환자 처방 데이터 가져오기

prescription_list = []

def main3():
    try:
        connection = mysql.connector.connect(
            host = '115.137.160.190',
            database = 'drugdb',
            user = user,
            password = password,
            port = 3306
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary = True)
            query = """ select * from prescription_record; """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            for row in results:
                #st.write(row)
                prescription_list.append(row)
            
           
            
    except Error as e:
        st.write("ERROR!!", e)
        
        
    finally:
        cursor.close()
        connection.close()
        #print("CONNECTION ENDED")
        


if __name__ == '__main3__':
  main3()
    
prescription = pd.DataFrame(prescription_list)
prescription.patientID = prescription.patientID.astype('str')
prescription.hosID = prescription.hosID.astype('str')
prescription.drugID = prescription.drugID.astype('str')
prescription.doctorID = prescription.doctorID.astype('str')
prescription.visit_date = pd.to_datetime(prescription.visit_date)
prescription = prescription.sort_values(by = 'visit_date')

################################################################################################################

# 데이터 전처리

import math

prescription = pd.merge(prescription, ID_RNN, on = 'patientID', how = 'inner')
prescription['gender'] = prescription['pRNN']

def gender_func(row):
    if row['gender'][7] == '1':
        row['gender'] = '남'
    elif row['gender'][7] == '2':
        row['gender'] = '여'
    elif row['gender'][7] == '3':
        row['gender'] = '남'
    elif row['gender'][7] == '4':
        row['gender'] = '여'
    
    return row

# 함수 적용
prescription = prescription.apply(gender_func, axis = 1)

def age_func(row):
    row['age'] = math.floor(row['age'] / 10) * 10
    return row

prescription = prescription.apply(age_func, axis = 1)

################################################################################################################

## 시각화

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math



## 한글폰트 사용 시 그래프에서 마이너스 부호가 깨지지 않도록 해줌
## plt.rcParams['font.family'] = 'Malgun Gothic'
## mpl.rcParams['axes.unicode_minus'] = False

plt.rc('font', size=20)        # 기본 폰트 크기
plt.rc('axes', labelsize=16)   # x,y축 label 폰트 크기
plt.rc('xtick', labelsize=14)  # x축 눈금 폰트 크기 
plt.rc('ytick', labelsize=14)  # y축 눈금 폰트 크기
plt.rc('legend', fontsize=20)  # 범례 폰트 크기
plt.rc('figure', titlesize=20) # figure title 폰트 크기

st.write('')
st.write('')
st.write('')

num = st.text_input('환자의 ID를 입력하세요 : ')

pat = prescription.loc[prescription['patientID'] == num]
drug_prescription = prescription.loc[prescription.drugID == pat.iloc[-1].drugID]

same_age = drug_prescription.loc[drug_prescription.age == pat.iloc[-1].age]
same_gender = drug_prescription.loc[drug_prescription.gender == pat.iloc[-1].gender]

if pat.iloc[-1].drugID == '1': 
    drug = "케타민"
elif pat.iloc[-1].drugID == '2': 
    drug = "프로포폴"
elif pat.iloc[-1].drugID == '3': 
    drug = "프로포폴"
elif pat.iloc[-1].drugID == '4': 
    drug = "암페타민"
elif pat.iloc[-1].drugID == '5': 
    drug = "펜타민"    
elif pat.iloc[-1].drugID == '6': 
    drug = "GHB"
elif pat.iloc[-1].drugID == '7': 
    drug = "메틸페니데이트"    
elif pat.iloc[-1].drugID == '8': 
    drug = "조피클론"    
elif pat.iloc[-1].drugID == '9': 
    drug = "졸피뎀"
elif pat.iloc[-1].drugID == '10': 
    drug = "졸피뎀"    
elif pat.iloc[-1].drugID == '11': 
    drug = "벤조디아제핀"     

    
if pat.iloc[-1].drugID == '1': 
    disease = "케타민"
elif pat.iloc[-1].drugID == '2': 
    disease = ""
elif pat.iloc[-1].drugID == '3': 
    disease = ""
elif pat.iloc[-1].drugID == '4': 
    disease = "우울증"
elif pat.iloc[-1].drugID == '5': 
    disease = "비만"    
elif pat.iloc[-1].drugID == '6': 
    disease = "기면증"
elif pat.iloc[-1].drugID == '7': 
    disease = "주의력결핍 과잉행동장애(ADHD)"    
elif pat.iloc[-1].drugID == '8': 
    disease = "불면증"    
elif pat.iloc[-1].drugID == '9': 
    disease = "불면증"
elif pat.iloc[-1].drugID == '10': 
    disease = "불면증"    
elif pat.iloc[-1].drugID == '11': 
    disease = "불안장애"     
        
all_mean = round(np.mean(drug_prescription.prescription_amount), 2)
ss = round(np.std(pat.prescription_amount), 2)
your_mean = round(np.mean(pat.prescription_amount), 2)

age_mean = round(np.mean(same_age.prescription_amount), 2)
gender_mean = round(np.mean(same_gender.prescription_amount), 2)


st.write('')
st.write('')

st.write("환자 전체의", drug, "평균 복용량은", all_mean, "(mg) 입니다.")
st.write('')

st.write("귀하의", drug, "평균 복용량은", your_mean, "(mg) 입니다.")
st.write('')

if your_mean > all_mean:
    st.write("귀하는 평균 복용량보다", round(your_mean / all_mean * 100 - 100, 2), "(%) 많이 복용하고 있습니다.")
elif your_mean < all_mean:
    st.write("귀하는 평균 복용량보다", round(-(your_mean / all_mean * 100 - 100), 2), "(%) 적게 복용하고 있습니다.")
else:
    st.write("귀하는 적정 수준 복용하고 있습니다.")
    
    
st.write('')    
st.write('')
st.write('')

#####################################################################################################################################################

import matplotlib.font_manager as fm
import matplotlib.dates as mdates

@st.cache_data
def fontRegistered():
  fm.fontManager.addfont('NANUMGOTHIC-BOLD.TTF')
  fm._load_fontmanager(try_read_cache=False)
    

# font_name = font_manager.FontProperties(fname='NANUMGOTHIC-BOLD.TTF').get_name()
# plt.rc('font', family=font_name)

  
# 라인차트
## prescription record 업데이트 후
## 인덱스 date로 바꿔서 plot할 것
# plt.subplot(1,1,2)

def main4():
  fontRegistered()
  font_name = fm.FontProperties(fname='NANUMGOTHIC-BOLD.TTF').get_name()
  plt.rc('font', family=font_name)
  
  fig = plt.figure(figsize = (30, 7))
  fig.add_subplot(1,3,1)

  x = ['전체 환자 평균', '귀하 평균']
  y = [all_mean, your_mean]
  colors = ['#caf0f8', '#FF595E']
  last = pat.iloc[-1]['prescription_amount']

  plt.title(f'귀하의 {drug} 투약 현황\n\n')
  plt.ylabel('평균 처방량(mg)\n')
  plt.bar(x, y, color = colors, edgecolor='gray')
  plt.text(0, your_mean/2, all_mean, verticalalignment ='top', horizontalalignment ='center')
  plt.text(1, your_mean/2, your_mean, verticalalignment ='top', horizontalalignment ='center')
  #plt.axhline(y=last,linewidth=1, color='k')
  plt.gca().spines['right'].set_visible(False) #오른쪽 테두리 제거
  plt.gca().spines['top'].set_visible(False) #위 테두리 제거

###########################################################################################################################################################################

  fig.add_subplot(1,3,2)

  x = ['전체 환자 평균', f'{pat.iloc[-1].age}대 환자 평균', '귀하 평균']
  y = [all_mean, age_mean, your_mean]
  colors = ['#caf0f8', '#90e0ef', '#FF595E']
  last = pat.iloc[-1]['prescription_amount']

  plt.title(f'{pat.iloc[-1].age}대 {disease} 환자 {drug} 투약 현황\n\n')
  #plt.ylabel('평균 처방량(mg)\n')
  plt.bar(x, y, color = colors, edgecolor='gray')
  plt.text(0, your_mean/2, all_mean, verticalalignment ='top', horizontalalignment ='center')
  plt.text(1, your_mean/2, age_mean, verticalalignment ='top', horizontalalignment ='center')
  plt.text(2, your_mean/2, your_mean, verticalalignment ='top', horizontalalignment ='center')
  #plt.axhline(x=,linewidth=1, color='k')
  plt.gca().spines['right'].set_visible(False) #오른쪽 테두리 제거
  plt.gca().spines['top'].set_visible(False) #위 테두리 제거

###########################################################################################################################################################################

  fig.add_subplot(1,3,3)

  x = ['전체 환자 평균', f'{pat.iloc[-1].gender}성 환자 평균', '귀하 평균']
  y = [all_mean, gender_mean, your_mean]
  colors = ['#caf0f8', '#48cae4', '#FF595E']
  last = pat.iloc[-1]['prescription_amount']

  plt.title(f'{pat.iloc[-1].gender}성 {disease} 환자 {drug} 투약 현황\n\n')
  #plt.ylabel('평균 처방량(mg)\n')
  plt.bar(x, y, color = colors, edgecolor='gray')
  plt.text(0, your_mean/2, all_mean, verticalalignment ='top', horizontalalignment ='center')
  plt.text(1, your_mean/2, gender_mean, verticalalignment ='top', horizontalalignment ='center')
  plt.text(2, your_mean/2, your_mean, verticalalignment ='top', horizontalalignment ='center')
  #plt.axhline(y=last,linewidth=1, color='k')
  plt.gca().spines['right'].set_visible(False) #오른쪽 테두리 제거
  plt.gca().spines['top'].set_visible(False) #위 테두리 제거
  st.pyplot(fig)

###########################################################################################################################################################################

  st.write('')
  st.write('')
  st.write('')

###########################################################################################################################################################################

  pat.visit_date = pat.visit_date.astype('str')
  
  fig = plt.figure(figsize = (30, 7))
  #fig.add_subplot(1,2,1)
  plt.title(f'귀하의 {drug} 처방량 추세\n\n')
  plt.ylabel('처방량(mg)\n')
  plt.xlabel('\n처방 날짜')
  plt.plot(pat.visit_date, pat.prescription_amount, marker = 'o', mec = 'tomato', mfc = 'tomato', color = 'cornflowerblue')
  plt.xticks(rotation=45)
  #dateFmt = mdates.DateFormatter('%Y-%m-%d')
  #ax.xaxis.set_major_formatter(dateFmt)
  plt.gca().spines['right'].set_visible(False) #오른쪽 테두리 제거
  plt.gca().spines['top'].set_visible(False) #위 테두리 제거
  #plt.gca().spines['left'].set_visible(False) #왼쪽 테두리 제거
  st.pyplot(fig)

  st.write('')    
  st.write('')
  st.write('')
  
  
if __name__ == "__main4__":
  main4()
