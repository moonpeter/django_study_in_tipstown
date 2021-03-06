# Ch02. 최적화된 장고 환경 설정하기
- These are good to have in your tool chest, since they are commonly used not just in Django, but in the majority of Python software development. 



### 2.1 같은 데이터베이스를 이용하라.


2.1.1 운영 데이터를 완전히 똑같이 로컬에서 구동할 수는 없다.

2.1.2 다른 종류의 데이터베이스 사이에는 다른 성격의 필드 타입과 제약 조건이 존재한다.

Keep in mind that different databases handle type casting of field data differently. 
cf) 
- type casting vs type hinting
- https://stackoverflow.com/questions/41046640/type-hinting-vs-type-casting-in-setters-php (php의 경우지만, python에서도 큰 맥락은 같은 듯)
- type hinting
- mypy, dataclass, pydantic
- python 3.10(type annotations)
- https://dev.to/iamdeb25/python-type-annotations-141n
- https://stackoverflow.com/questions/42397502/how-to-use-python-type-hints-with-django-queryset


2.1.3 Fixtures 는 만능 해결책이 아니다.

- Fixtures는 단순히 하드 코딩된 간단한 데이터 세트를 생성하는데 좋은 도구

- 큰 크기의 데이터 세트를 이전하는 데는 그다지 신뢰할 만한 도구가 아니다.

  

### 2.2 pip와 virtualenv 이용하기

- pip(Python Package Index)
  - 파이썬 패키지를 설치하고 관리하는 데 이용한다.
  - virtualenv를 지원함
  - 파이썬 3.1.4 이후 버전부터는 기본적으로 내장
- virtualenv
  - 파이썬 패키지 의존성을 유지할 수 있게 독립된 파이썬 환경을 제공하는 도구

2.2.1 virtualenvwrapper

- 사용하는 것을 강력히 추천함

- $ source ~/.virtualenvs/twocoops/bin/activate ⇒ $ workon twoscoops

  

### 2.3 pip를 이용하여 장고와 의존 패키지 설치하기

- 저자는 pip와 requirrements file을 이용하여 장고를 설치하는 것을 추천함

  

### 2.4 버전 컨트롤 시스템 이용하기

- 코드의 변경 내용을 기록하려면 반드시 버전 컨트롤 시스템을 이용해야 한다.
- 깃(Git)과 리포지토리 호스팅 서비스는 GitHub와 GitLab을 추천한다.



### 2.5 선택 사항 : 동일한 환경 구성

- 제거 가능한 환경 구성의 차이
  - O/S system 차이( ex ⇒ Mac or Windows)
  - Python 설정 차이
  - 개발자 간의 설정 차이

2.5.1 Docker
https://www.44bits.io/ko/post/almost-perfect-development-environment-with-docker-and-docker-compose

- 장점
  - 프로젝트 내 모든 개발자가 동일한 개발환경 설정 가능
  - 스테이징, 테스트 및 프로덕션 서버와 유사한 환경의 로컬 개발 환경 구성 가능
- 단점
  - 도커 설정으로 인하여 추가적인 복잡성 증가
  - 성능 저하를 유발할 수 있음, 최신 사양에서는 크지 않지만 열악한 개발환경에서는 유의미한 성능 저하 일 수 있음

