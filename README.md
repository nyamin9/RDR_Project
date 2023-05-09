# RDR : Rapid Drug Report Project  

<br>  

항정신성의약품 처방 즉시, 차트와 텍스트를 통해 환자가 본인의 전반적인 복용 통계량을 즉각적으로 파악할 수 있도록 돕는 방법을 고안합니다.  

<br>  

현재 우리나라에서 마약류를 관리하는 [NIMS 통합시스템](https://data.nims.or.kr/study/intro/view.do)은, 마약류 유통과정의 전체 과정을 담고 있습니다.  

이에, 각각의 환자를 관리하기에는 너무 복잡하고 비효율적인 데이터베이스라고 판단하였습니다.  

따라서 저희 팀은 환자와 병원, 처방전에 집중한 데이터베이스를 구축해 환자별, 질병별 모니터링이 가능한 간소화된 데이터베이스를 구축하고자 합니다.  

<br>  


이를 통해, 본인이 복용하는 약물 양의 모니터링을 통한 약물 오남용 예방 효과를 기대합니다.  

<br>  

***  

<br>  

<p align = 'center'><b>🛠 Tech 🛠</b></p>  

<p align="center">
  <img src="https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=Python&logoColor=white"/></a>&nbsp 
  <img src="https://img.shields.io/badge/-pandas-150458?style=flat-square&logo=pandas&logoColor=white"/></a>&nbsp
  <img src="https://img.shields.io/badge/-MySQL-4479A1?style=flat-square&logo=MySQL&logoColor=white"/></a>&nbsp   
  <br>  
  <img src="https://img.shields.io/badge/-Plotly-3F4F75?style=flat-square&logo=Plotly&logoColor=white"/></a>&nbsp
  <img src="https://img.shields.io/badge/-Jupyter-F37626?style=flat-square&logo=Jupyter&logoColor=white"/></a>&nbsp
</p>  

<br>  

***  

<br>  

## 데이터베이스  

<br>  

데이터베이스는 아래의 구조로 구현하였습니다.  

<br>  

<p align="center"><img src="https://user-images.githubusercontent.com/65170165/236972749-e3e4a893-7f1b-455c-9938-4cf010eb1acf.png" height="500px" width="680px"></p>  


<br>  

<b>TABLE 1. doctor_info</b> : 의사 개인 정보 테이블  


| doctorID    | hosID       | dname     | dRNN              | phone            |
|--------------|--------------|-----------|-------------------|------------------|
| 의사 고유 ID | 병원 고유 ID | 의사 이름 | 의사 주민등록번호 | 의사 휴대폰 번호 |  

<br>  


<b>TABLE 2. drug_info</b> : 약물 정보 테이블  

| drugID      | drugname | min         | max         |
|--------------|----------|-------------|-------------|
| 약물 고유 ID | 약물명   | 최소 복용량 | 최대 복용량 |  

<br>  

<b>TABLE 3. patient_info</b> : 환자 정보 테이블  

| patientID   | pname  | pRNN         | phone    | age  |
|--------------|--------|--------------|----------|------|
| 환자 고유 ID | 환자명 | 주민등록번호 | 전화번호 | 나이 |  

<br>  

<b>TABLE 4. hospital</b> : 병원 정보 테이블  

| hosID        | hosnName | hosphone      |
|--------------|----------|---------------|
| 병원 고유 ID | 병원명   | 병원 전화번호 |  

<br>  

<b>TABLE 5. hospital_drug</b> : 병원 약물 보유 현황 테이블  


| hosID        | drugID       | amount         |
|--------------|--------------|----------------|
| 병원 고유 ID | 약물 고유 ID | 약물 보유 현황 |  

<br>  

<b>TABLE 6. prescription_record</b> : 처방전 테이블  

|   patientID  |     hosID    |    drugID    |   doctorID   | prescription_amount |    day   | state | visit_date |
|:------------:|:------------:|:------------:|:------------:|:-------------------:|:--------:|:-----:|:----------:|
| 환자 고유 ID | 병원 고유 ID | 약물 고유 ID | 의사 고유 ID |        처방량       | 처방 일수 |  상태 |  처방 날짜 |  


<br>  



