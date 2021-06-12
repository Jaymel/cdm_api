# 이용 방법
먼저 config.py 파일에 DB의 접속 정보를 작성합니다.
이후 cmd나 터미널에서 pip install -r requirements.txt 명령을 통해 실행 환경을 설정합니다.
코드를 작성한 파이썬 버전은 3.8 입니다.

설정이 완료되었으면 터미널에서 flask run 명령어를 통해 서버를 실행할 수 있습니다.

#API 설명
API는 크게 네개로
환자의 통계를 확인할 수 있는 person
방문자 통계를 확인할 수 있는 visit
테이블 별 concept_id 정보를 확인할 수 있는 concept
테이블 별 row 검색이 가능한 search 입니다.

person api 정보-
|method|url|response
|---|---|---|
|GET|/person/all|전체 환자 수|
|GET|/person/ethnicity|민족 별 환자 수|
|GET|/person/death|사망한 환자 수|
|GET|/person/gender|성별 환자 수|
|GET|/person/race|인종 별 환자 수|

visit api 정보-
|method|url|response
|---|---|---|
|GET|/visit/all|방문 유형(입원/외래/응급)별 방문 수|
|GET|/visit/gender|성 별 방문 수|
|GET|/visit/race|인종 별 방문 수|
|GET|/visit/ethnicity|민족 별 방문 수|
|GET|/visit/age|방문시 연령대 별 방문 수|

concept api 정보-
|method|url|response
|---|---|---|
|GET|/concept?table=&concept=&page=|사용하는 전체 테이블에서 각 concept_id 정보, table과 concept로 검색 가능하며 page로 페이지네이션|

search api 정보-
|method|url|response
|---|---|---|
|GET|/search/<table>?<keyword>=&page=|table로 테이블을 쿼리, <keyword>로 필터링할 수 있으며 keyword의 수는 제한 없음, page로 페이지네이션|