# 🔴 [위코드 x 원티드] 8퍼센트 기업 협업 과제

## 🟡 구현 기술 스택
- Language  : Python

- Framework :  Django

- Postman

- DB  : sqlite3

- 배포 :AWS EC2 with Nginx, Gunicorn

## 🟡 Contributors
|이름 |담당 기능| GitHub 주소|
|------|---|---|
|김도담|모델링, 입,출금 API| [damdream](http://github.com/damdream)|
|성우진|모델링, 거래내역 조회 API | [jinatra](http://github.com/jinatra)|
|이정우|배포| [acdacd66](http://github.com/acdacd66)|

## 🟡 빌드 및 실행 방법
- repo 폴더안의 requirements.text 파일을 install 한다.
pip install -r requirements.txt
- python manage.py runserver를 통해 서버를 실행한다.
<br>
- [Postman API 주소](https://documenter.getpostman.com/view/16843875/UVC5F7ej) 를 통해 확인 가능합니다.
<br>

## 🟡 기본 설계
![무제](https://user-images.githubusercontent.com/81546305/140999122-f1c0640b-4c5c-4254-ba9c-969291c65e85.jpg)

- company 모델을 기본으로 이름, 언어 타입, tag 값을 각각의 row로 갖고, 
  company_connection과 연결되는 company_id를 통해 다른 언어로 입력된 같은 회사를 연결시켜 주었습니다.


## 🟡 구현 내용
- 거래내여 조회 GET API
- 입금 POST API
- 출금 POST API

## 🟡 구현 기능/구현 방법
🔵  거래내역 조회 GET API
 
- 검색 시작 날짜(`start_date`), 검색 종료 날짜(`end_date`), 입/출금 타입(`type`) 및 pagination data(`offset`, `limit`)을 쿼리 스트링으로 전달받습니다.
- 각각의 쿼리스트링이 전달되지 않으 경우, 기존에 지정해두 default value를 통해 filtering하게 됩니다.
- filtering method로는 q객체를 사용하였습니다.
- 인증되지 않은 유저(다른 유저)의 접근을 제한하기 위해 토큰을 이용하여 사용자르 식별합니다.
- Key Error, Value Error(잘못된 type 형식 등), Validation Error(잘못된 날짜 형식 등)에 대한 예외처리를 주었습니다.

🔵 입금 POST API

- 

🔵 출금 POST API

- 



## 🟡 배포 서버
- 아래 OPEN API 링크를 통해 엔드포인트 및 API TEST를 진행할 수 있습니다.
- 


## 🟡 엔드포인트 설명
|METHOD| ENDPOINT| body | 수행목적 |
|------|---|---|----|
| GET	| /accounts/history?start_date&?end_date?type	| query string	| 거래 내역 조회 |
| POST |  |  | 입금 |
| POST | | | 출금 |


## 🟡 아쉬웠더 점

- 성우진
<img width="669" alt="image" src="https://user-images.githubusercontent.com/85162752/141450304-0eff9404-3ff4-49b3-b099-81a91a4c2b0a.png">

  - 위 조회 화면에서는 특정 기간(일주일, 한달 등)을 조회할 수 있는 버튼을 주었는데, 해당 post request에 대해 즉각적으로 반환해줄 수 있는 API를 짜지 못했더 점이 못내 아쉽습니다.
  - DB join을 최소화하기 위해 하나의 쿼리문을 통해 객체르 가져올 수 있도로 하였는데, 각 객체의 user_id에 접근하여 token의 user_id와 비교할 수 있는 방법을 제출 기한 내에 생각하지 못해 첫 객체를
    기준으로 잡아 인증 검사를 하였던 것이 아쉬웠습니다.



## 🟡 프로젝트 회고

- 이정우: [블로그](https://mytech123.tistory.com/)
- 성우진: [블로그](https://velog.io/@jinatra)
- 김도담: [블로그](http://velog.io/@damdreammm)
