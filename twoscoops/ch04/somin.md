
# 4. Django App 설계


Django 프로젝트는 많은 App으로 구성된다.
INSTALLED_APPS는 해당 프로젝트에서 사용 가능한 앱 목록을 나타낸다.

## 4.1 Django app 디자인
- 좋은 Django 앱을 만들고 유지하기 위해서는 각 앱은 자신의 앱 작업에 집중해야 한다.
- 만약 app이 하는 작업을 간결하게 말할 수 없거나 and로 이어지는 경우 앱이 크기 때문에 분할해야 한다.

- 만약 "Two Scoops"라고 불리는 웹 애플리케이션을 만들고 오픈준비를 한다고 상상해보자.

- 장고 프로젝트는 다음과 같이 생성할 수 있다.
1. flavoers app -> 아이스크림 맛과 리스트를 웹사이트에 표시
2. blog app -> Two Scoops의 official blog
3. event app -> 우리 가게의 이벤트를 웹사이트에 표시

- 각각의 앱은 한가지의 주요 목적을 가지고 작업을 수행한한다.
위의 기능을 하는 하나의 앱보다 세개의 앱으로 나누어 구현하는 것이 훨씬 나은 방법이다.
- 나중에 확장하기에도 훨씬 편안하다.

## 4.2 app name
1. 일반적으로 앱의 이름은 앱의 메인 모델의 복수버전 하지만 앱의 메인모델만 생각하면 안된다.
2. URL고려하여 원하는 URL로 생성해야 한다.
ex) http://www.example.com/weblog/

## 4.3 app은 작은단위로 유지
- 몇 개의 큰 앱보다 작은 앱을 많이 사용하는게 더 좋다.


## 4.4 app에 속하는 모듈
- 앱에는 common 파이썬 모듈과 uncommon 파이썬 모듈이 모두 포함된다.
* Common modules
scoops/
├── __init__.py
├── admin.py
├── forms.py
├── management/
├── migrations/
├── models.py
├── templatetags/
├── tests/
├── urls.py
├── views.py

* Uncommon modules
scoops/
├── api/
├── behaviors.py
├── constants.py
├── context_processors.py
├── decorators.py
├── db/
├── exceptions.py
├── fields.py
├── factories.py
├── helpers.py
├── managers.py
├── middleware.py
├── schema.py
├── signals.py
├── utils.py
├── viewmixins.py

## 4.5 Ruby on Rails-Style Approaches
[Ruby on Rails란?]
- Ruby로 개발된 오픈소스 웹 프레임워크
- 링크 : http://blog.wishket.com/%EB%A3%A8%EB%B9%84-%EC%98%A8-%EB%A0%88%EC%9D%BC%EC%A6%88ruby-on-rails-a%EB%B6%80%ED%84%B0-z%EA%B9%8C%EC%A7%80-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0/
