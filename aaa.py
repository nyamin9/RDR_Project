import streamlit as st
import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')



## 한글폰트 사용 시 그래프에서 마이너스 부호가 깨지지 않도록 해줌

plt.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['axes.unicode_minus'] = False


prescription = pd.read_csv('real_prescription.csv')

prescription.patientID = prescription.patientID.astype('str')
prescription.hosID = prescription.hosID.astype('str')
prescription.drugID = prescription.drugID.astype('str')
prescription.doctorID = prescription.doctorID.astype('str')

num = st.text_input('환자 ID를 입력하세요 : ')

pat = prescription.loc[prescription['patientID'] == num]
drug_prescription = prescription.loc[prescription.drugID == pat.iloc[-1].drugID]

#st.dataframe(pat)

all_mean = np.mean(drug_prescription.prescription_amount)
your_mean = np.mean(pat.prescription_amount)

st.write("----------------------------------------------------------------")
st.write()

st.write("환자의 평균 복용량은", all_mean, "(mg) 입니다.")
st.write("귀하의 평균 복용량은", your_mean, "(mg) 입니다.")

if your_mean > all_mean:
    st.write("귀하는 평균 복용량보다", round(your_mean / all_mean * 100 - 100, 2), "(%) 많이 복용하고 있습니다.")
elif your_mean < all_mean:
    st.write("귀하는 평균 복용량보다", round(-(your_mean / all_mean * 100 - 100), 2), "(%) 적게 복용하고 있습니다.")
else:
    st.write("귀하는 적정 수준 복용하고 있습니다.")
    
    
st.write()    
st.write('-------------------------------------------------------------------')
st.write()

# 라인차트
## prescription record 업데이트 후
## 인덱스 date로 바꿔서 plot할 것
# plt.subplot(1,1,2)

plt.rc('font', size=16)        # 기본 폰트 크기
plt.rc('axes', labelsize=14)   # x,y축 label 폰트 크기
plt.rc('xtick', labelsize=13)  # x축 눈금 폰트 크기 
plt.rc('ytick', labelsize=13)  # y축 눈금 폰트 크기
plt.rc('legend', fontsize=20)  # 범례 폰트 크기
plt.rc('figure', titlesize=2) # figure title 폰트 크기

fig = plt.figure(figsize = (15, 5))

fig.add_subplot(1,2,1)
#plt.title('귀하의 처방량 추세')
plt.title("Your prescription volume trend")
#plt.ylabel('처방량(mg)')
plt.ylabel("prescription volume (mg)")
#plt.xlabel('처방 날짜')
plt.xlabel('date')
plt.plot(pat.prescription_amount, marker = 'o', mec = 'tomato', mfc = 'tomato', color = 'cornflowerblue')
plt.gca().spines['right'].set_visible(False) #오른쪽 테두리 제거
plt.gca().spines['top'].set_visible(False) #위 테두리 제거
#plt.gca().spines['left'].set_visible(False) #왼쪽 테두리 제거

# 히스토그램
fig.add_subplot(1,2,2)
a = prescription.copy()
a.prescription_amount = a.prescription_amount.astype('str')

res = a.groupby('prescription_amount').agg({'patientID' : 'count'})
res = res.reset_index()
res.prescription_amount = res.prescription_amount.astype('int64')
res = res.sort_values('prescription_amount')


## 해당 환자의 가장 마지막 처방량 -> 인사이트가 별로 없음
## 삭제할지 말지 결정하기!!
last = pat.iloc[-1]['prescription_amount']
your_last = res[res.prescription_amount==last]
plt.title('처방량 별 인원 분포')
plt.xlabel('처방량')
plt.ylabel('인원')

plt.bar(res.prescription_amount, res.patientID, color = 'cornflowerblue')
plt.bar(your_last['prescription_amount'], your_last['patientID'], color = 'tomato')
#plt.bar(last, res['prescription_amount'] == last, color = 'r')
plt.ylim([res.patientID.min()-res.patientID.std(), res.patientID.max()+res.patientID.std()])
#plt.annotate("annotate - xycoords('figure points')", xy=(2, 100), xycoords='figure points' )
plt.gca().spines['right'].set_visible(False) #오른쪽 테두리 제거
plt.gca().spines['top'].set_visible(False) #위 테두리 제거
#plt.gca().spines['left'].set_visible(False) #왼쪽 테두리 제거
#plt.legend()

plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.25, hspace=0.2)
plt.show()

## prescription_record에 state 추가 시 차트 추가할 것
## state 별 평균 약물 복용량 & 현재 당신의 state와 복용량
## 귀하의 증상 추세


st.pyplot(fig)


