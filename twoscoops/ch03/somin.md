
# 3. 장고 프로젝트를 어떻게 설계할 것인가


## 3.1 Django3의 기본 레이아웃, 구조

- project 시작 명령어
    django-admin startproject mysite
    cd mysite (mysite 안으로 이동)
- application 시작 명령어
    django-amdin startapp my_app

[ 기본구조 ]

mysite/
├── manage.py
├── my_app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
└── mysite
├── __init__.py
├── asgi.py
├── settings.py
├── urls.py
└── wsgi.p

## 3.2 선호해야 할 프로젝트 구조

<repository_root>/
├── <configuration_root>/
├── <django_project_root>/

## 3.3 프로젝트 구조 예시

- 만약 아이스크림 평가 프로젝트를 만든다고 가정하면,
프로젝트는 이런식으로 구성될 수 있다.

icecreamratings_project
├── config/
│   ├── settings/
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── docs/
├── icecreamratings/
│   ├── media/ # Development only!
│   ├── products/
│   ├── profiles/
│   ├── ratings/
│   ├── static/
│   └── templates/
├── .gitignore
├── Makefile
├── README.md
├── manage.py
└── requirements.tx

- 가장 상위 디렉토리에는 README.md, .gitignore, requirements.txt파일 및 프로젝트 배포 및 실행에 필요한 파일들을 포함한다.

- 두번째 <django-project-root>인 icecreamratings 디렉토리는 실제 Django 프로젝트의 루트

- 세번째 <configuration_root>인 config디렉토리는
URLConf와 설정관련 파일들이 포함되는 곳
__init__.py를 꼭 포함해야 한다.

## 3.4 Virtualenv

- 위에 설명에 보면, 프로젝트 디렉토리나 하위 디렉토리 어디에도 virtualenv 디렉토리가 없다는걸 알 수 있다.
- virtualenv는 별도의 디렉토리로 관리하는 것이 좋다.

* for Mac or Linux:
~/projects/icecreamratings_project/
~/.envs/icecreamratings/

* for Windows:
c:\projects\icecreamratings_project\
c:\envs\icecreamratings\

* 만약 virtualenvwrapper를 사용한다면
~/.virtualenvs/icecreamratings/

- 이미 requirements.txt파일에서 버전을 관리하고 있기 때문에 virtualenv 소스코드를 직접적으로 편집하지 않아도 된다.

## 3.5 프로젝트 시작을 넘어서
- Cookiecutter로 프로젝트 시작하기

[ Cookiecutter란? ]
장고의 초기설정을 간편하게 도와주는 라이브러리
관련링크
https://kwaakdo.github.io/2019/10/03/django-cookiecutter.html
Django에서 제공하는 기본 startproject 템플릿보다 훨씬 유용하고 자신의 프로젝트에 맞게 사용자가 지정할 수 있다.
