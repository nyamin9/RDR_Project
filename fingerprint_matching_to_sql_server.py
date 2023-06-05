import serial
import pandas as pd
import random
import mysql.connector
from mysql.connector import Error
import sys
import streamlit as st

# 시리얼 포트 설정
ser = serial.Serial('COM3', 9600, timeout=1)


result = []
empty_count = 0  # 빈 배열 카운트 변수



# 데이터 수신

while ser.readable:
    res = ser.readline().decode().strip()  # 줄을 읽고 디코딩한 뒤 앞뒤 공백 제거
    if res:  # 줄이 비어 있지 않은 경우에만 처리
        result.append(res.split('\n'))  # 줄을 ' \n ' 구분자를 사용하여 리스트로 분할
        empty_count = 0  # 빈 배열 카운트 초기화
    else:
        empty_count += 1  # 빈 배열 카운트 증가
        
    if empty_count >= 5:  # 빈 배열이 연속해서 3회 이상 나오면 루프 종료
        break


if ' ' in result[-1][0]:
    st.write('지문을 다시 대주세요')
    sys.exit()  # 코드 실행 중단
    
else: patientID = int(result[-1][0])


def main():
    try:
        connection = mysql.connector.connect(
            host = '115.137.160.190',
            database = 'drugdb',
            user = 'MinguKang',
            password = 'ASdfseol779$',
            port = 3306
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary = True)
            
            query = """ select * from finger_info where patientID = %s """
            record = (patientID,)
            
            cursor.execute(query, record)
            
            results = cursor.fetchall()
            
            for x in results: st.write(x)
            
    except Error as e:
        st.write("ERROR!!", e)
        #print('ERROR', e)
        
    finally:
        cursor.close()
        connection.close()
        #print("CONNECTION ENDED")
        

if __name__ == '__main__':
  main()
