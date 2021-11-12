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
- 입금 POST API
- 출금 POST API
- 거래내여 조회 GET API

## 🟡 구현 기능/구현 방법
🔵  회사 등록 POST API
 
- 회사명, 언어종류, tag를 입력하여 POST API를 구현합니다. 
- x_wanted_language를 조회해온 후 company_name과 tags를 request 받아옵니다.
- Company_connection을 입력, 저장합니다. for문을 이용해 company의 값을 입력합니다.
- 회사의 이름과 언어 타입, tag_list를 통해 tag가 존재한다면 append 해줍니다.
- 결과값으로 company_name과 tags를 반환합니다. <br>


🔵 회사 검색 get API

- company_name을 None으로 지정한 후, url path로 받은 회사 이름이 존재하면 초기화 합니다.
- Return 언어의 타입을 지정할 수 있습니다. 입력된 회사가 존재하지 않는다면 404에러를 반환합니다.
- 회사가 존재한다면 결과값으로 회사의 이름과 tag를 반환해줍니다.

🔵 검색어 자동완성 API

- search_value와 decode search_value를 get합니다. 
- 입력된 x_wanted_language 값을 get으로 조회합니다.
- filter의 icontains 로 입력된 값을 해당 값이 포함된 문자열을 검색한다. 값이 없다면 404 에러를 반환합니다.
- company_connection을 통해 company_id의 pk값을 얻어오고 이 과정을 통해 얻은 값을 suggestions에 넣어주고 결과값으로 반환합니다.



## 🟡 배포 서버
- 아래 OPEN API 링크를 통해 엔드포인트 및 API TEST를 진행할 수 있습니다.
- [OPEN_API](http://18.224.165.47:8000)


## 🟡 엔드포인트 설명
|METHOD| ENDPOINT| body | 수행목적 |
|------|---|---|----|
| POST	| /crud/enrollment	| company_name, tags	| 회사 추가 |
| GET | /crud/search?query=링크 | query | 검색어 자동완성 |
| GET | /crud/search/<str:company_name | query| 검색 기능 구현 |



## 🟡 프로젝트 회고

- 이정우: [블로그](https://mytech123.tistory.com/)
- 성우진: [블로그](https://velog.io/@jinatra)
- 김도담: [블로그](http://velog.io/@damdreammm)
