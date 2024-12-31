# 23.Django's Secret Sauce: Third-Party Packages

전문적인 장고와 파이썬 개발의 대부분은 타사 패키지를 장고 프로젝트에 통합하는 것에 관한 것이다. 필요한 도구를 처음부터 모두 작성하려고 하면 작업을 완료하는 데 어려움을 겪을 것입니다.
이는 특히 고객 프로젝트가 동일하거나 유사한 구성 요소로 구성되어 있는 컨설팅 분야의 우리에게 해당됩니다.


## 23.1 Examples of Third-Party Packages

Django 뿐만 아니라 다른 파이썬 프로젝트에서도 이용가능한 패키지들도 있습니다.
- 'django-', 'dj-'를 제거하면 원래 패키지를 찾아볼 수 있고, 해당 패키지는 다른 파이썬 프로젝트에서도 활용 가능하다라는 의미로 해석함.
- Django에만 적용되는 패키지는 보통 'django-' or 'dj-'  라는 접두어로 시작
- 

## 23.2 Know About the Python Package Index

- PyPI(Python Package Index) 
- pip는 PyPI에서 파일을 다운로드합니다.

## 23.3 Know About [DjangoPackages.org](http://djangopackages.org/)

- [https://djangopackages.org/](https://djangopackages.org/)
    - Django app을 위한 재사용 가능합 앱, 사이트, 도구 등을 모아 놓은 디렉터리
    - PyPI와 달리 각 패키지를 자체적으로 저장하지 않고, 파이썬 패키지 인덱스, 깃헙, 비트버킷, ReadTheDocs, 사용자가 입력한 데이터들을 잘 정리하여 제공
    - 각 패키지의 기능을 비교하기 좋음

## 23.4 Know Your Resources

- Django Packages, PyPI을 반드시 익혀두자.
- 바퀴를 재발명하지 말자. 이 라이브러리들은 유능한 개발자들에 의해 작성, 문서화, 테스트까지 되었습니다.
- 다양한 패키지를 사용함으로 패키지의 코드를 공부하고, 더 나은 개발자로 만들어 줄 패턴과 기술들을 배울 수 있습니다.
- 좋은 패키지와 나쁜 패키지를 식별할 능력을 얻게 됩니다.

## 23.5 Tools for Installing and Managing Packages

- 모든 패키지의 장점을 누리기 위해서는 **virtualenv, pip**(Conda or Poetry)는 필수적입니다. # 가상환경 

## 23.6 Package Requirements

- 프로젝트의 `requirements/` 디렉터리내에 requirements 파일로 관리 # 의존성 관리 방식

## 23.7 Wiring Up Django Packages: The Basics (장고 패키지 사용하기)

### 23.7.1 Step1: Read to Documentation for the Package

- 특정 패키지를 설치하기 전에 패키지에서 어떤 기능을 얻게 될지 문서를 읽자.

### 23.7.2 Step2: Add Package and Version Number to Your Requirements

- requirements에 각 패키지의 특정 버전을 지정해야 합니다.
cf) 도경님 블로그에서 그대로 인용 -> 책에 인용된 스토리가 이해가 되지 않음.
1. 하지 않는다면? Django 프로젝트를 다시 설치하거나 변경할때 반드시 문제가 발생
    - 새로 릴리즈된 패키지는 하위 호환을 장담하지 않음
2. 작업 내용을 릴리스하는 데 약간의 형식과 프로세스를 갖추는 것입니다.
    - 깃헙을 포함한 저장소들을 최종 안정 버전이 아닌 개발 중인 작업 버전입니다.
3. 배포 및 테스트 환경에서 훨씬 더 예측할 수 있게 됩니다.

### 23.7.3 Step3: Install the Requirements Into Your Virtualenv

- `pip install` 으로 환경에 맞는 requirement 파일을 실행

### 23.7.4 Step4: Follow the Package's Installation Instructions Exactly

- 해당 패키지에 익숙하지 않다면 패키지 문서대로 읽고 진행하세요.

## 23.8 Troubleshooting Third-Party Packages

1. 스스로 해결해보자.
2. 해당 문서를 숙지하고 빠뜨린 단계가 없는지 확인
3. 다른 사람도 같은 문제를 겪었는지 검색
4. 버그같다면 패키지 저장소의 이슈 트래커를 검색
5. 그래도 해결이 되지 않는다면 도움을 청하자.
    - StackOverflow, IRC #django 채널, etc # IRC가 뭔지 모르겠음, django forum, django google group 개인적으로 추천

## 23.9 Releasing Your Own Django Packages

유용한 Django 앱을 제작했다면 다른 프로젝트에서 재사용 할 수 있도록 패키징 할 수 있습니다.

[Advanced tutorial: How to write reusable apps](http:/docs.djangoproject.com/en/3.2/intro/reusable-apps/)
으로 패키징을 시작할 수 있습니다. # 가장 좋은 방법

이 외의 방법

- 코드를 포함하는 공개 저장소를 생성(GitHub, Gitlab, ..)하자.
- 파이썬 패키지 인덱스에 패키지를 릴리스하자.
    - [Packaging Python Projects]([packaging.python.org/distributing/](http://packaging.python.org/distributing/))
- 패키지를 [Django Packages]([djangopackages.org](http://djangopackages.org/))에 추가하자.
- [Read the Docs]([readthedocs.io](http://readthedocs.io/))를 이용하여 스핑크스(Sphinx) 문서를 호스팅하자.

## 23.10 What Makes a Good Django Package?

### 23.10.1 Purpose

- 패키지는 유용한 기능이 있어야 하며, 당연히 잘 작동해야 합니다.
- 패키지의 이름은 패키지의 목적, 기능을 설명할 수 있어야 합니다.

### 23.10.2 Scope

해당 태스크에만 집중되어야 합니다.

- 논리 자체가 엄격해짐
- 추후 기능 패치하거나 다른 패키지로 교체하기 수월해짐

### 23.10.3 Documentation

1. 문서는 Markdown으로 작성되어야 함
2. MkDocs, Sphink 등의 도구를 사용하여 생성하고 공개적으로 호스팅해야 함
    - readthedocs.io과 web hook 기능을 추천(문서의 변경사항을 자동으로 생성)
3. 종속성이 있는 경우 문서화는 필수
4. 패키지 설치 지침도 문서화

### 23.10.4 Tests

반드시 테스트를 거쳐야만 합니다.

- 패키지의 신뢰도 향상
- 앞으로 나올 파이썬, Django 버전에도 도움
- 컨트리뷰터들이 효과적으로 공헌할 수 있게 됨
- 패키지의 테스트를 실행하는 방법을 문서화
- 다른 컨트리뷰터들이 해당 테스트를 쉽게 실행하게 되므로, 질 높은 기여를 받을 수 있는 혜택을 얻게 됨

### 23.10.5 Templates

Django 패키지에 기본 기능들을 구현해 둔 베어본 템플릿 셋을 제공하는 것이 표준

- CSS를 제외한 최소한의 HTML, JS를 제공
- 스타일 지정이 필요한 위젯이 포함되었다면 CSS도 포함

### 23.10.6 Activity

필요에 따라 주기적으로 업데이트 되어야 합니다.

저장소의 코드가 마이너나 메이저 릴리스일 경우 PyPI에도 자동으로 업데이트 되도록 해야 합니다.

### 23.10.7 Community

- .rst 파일 알아보기 : rst(Restructured Text)
- [rst 관련 파이콘 발표자료](https://www.slideshare.net/ianychoi/pycon-kr-2017-rst-python-openstack)
- 모든 컨트리뷰터에게 해당 작업에 대한 귀속 조건을 담은 CONTRIBUTORS.rst나 AUTHORS.rst 파일을 제공해야 함
- 패키지에 컨트리뷰터들이 생겨남에 따라 커뮤니티 리더 역할도 해야 함
- 다른 개발자들이 포크해 간다면 머지될 수 있는지 관심을 가져야 함

### 23.10.8 Modularity

- Django의 코어 컴포넌트(템플릿, ORM 등)을 다른 모듈로 교체하지 않고도 문제 없이 작동되어야 합니다.
- 설치는 기존 Django 프로젝트에 최소한의 영향을 미쳐야 합니다.

### 23.10.9 Availability on PyPI

- 패키지의 메이저나 마이너 릴리스를 PyPI에서 다운받을 수 있어야 합니다.
- 개발자들이 문제 없는 버전을 찾기 위해 패키지 저장소로 오지 않도록 해야 합니다.
- 올바른 버전 번호의 규칙을 따라야 합니다.

### 23.10.10 Uses the Broadest Requirements Specifiers Possible

`setup.py` 파일안에 `install_requires` 인자에는 제작된 서드 파티 라이브러리를 이용하기 위해 필요한 다른 패키지의 정보가 담겨져 있습니다.

호환성을 위해 가능한 넓게 기술해야 합니다.

```python
Django>=3.1,<3.0
requests>=2.13.0,<=3.0.0
```

- [https://pip.pypa.io/en/stable/cli/pip_install/](https://pip.pypa.io/en/stable/cli/pip_install/)
- [https://nvie.com/posts/pin-your-packages/](https://nvie.com/posts/pin-your-packages/)
- [module 만들기](https://github.com/navdeep-G/samplemod)

### 23.10.11 Proper Version Numbers

PEP 386의 'A.B.C 패턴'

- A: 메이저 번호
- B: 마이너 번호
- C: 버그 수정 릴리스

alpha, beta, rc(release-candidate) 접미사는 앞으로 릴리스될 버전

- ex: Django 3.2-alpha / django-crispy-forms 1.9.1-beta
- 절대로 alpha, beta, rc는 PyPI에 올리면 안됨

더 읽을 자료들

- [https://www.python.org/dev/peps/pep-0386/](https://www.python.org/dev/peps/pep-0386/)
- [https://semver.org/](https://semver.org/)

### 23.10.12 Name

- PyPI에 중복된 이름이 있는지 확인
- DjangoPackages에 중복된 이름이 있는지 확인
- 외설적이거나 문제가 될 만한 이름을 금지

### 23.10.13 License

- MIT
    - 상용 또는 비상용 환경 모두 허용되는 라이선스. 개인이라면 MIT
- Apach
    - 특허를 고민하고 있다면

### 라이선스 생성법
패키지 저장소의 루트에 LICENSE.rst 파일을 생성하고, 최상단에 라이선스 이름, 해당 라이선스의 문구들을 기입

- [https://choosealicense.com/](https://choosealicense.com/)

### 23.10.14 Clarity of Code

- 패키지의 코드는 최대한 단순하고 간결하게 구성해야 합니다.
- 일반적이지 않은 파이썬 코드나 Django의 hack을 쓴다면 정확한 의도와 설명이 있어야 합니다.

### 23.10.15 Use URL Namespaces

URL Namespace를 이용하면, 프로젝트들 사이에서 서로 충돌을 막을 수 있고, 앞으로 생길지 모르는 문제를 미리 대비할 수 있습니다.

## 23.11 Creating Your Own Packages the Easy Way

- **Cookiecutter** 추천
    - https://github.com/cookiecutter/cookiecutter
    - [https://cookiecutter.readthedocs.io/en/1.7.2/](https://cookiecutter.readthedocs.io/en/1.7.2/)


### Cookiecutter 사용하기

```bash
# cookiecutter 설치
$ pip install cookiecutter

# Django 프로젝트를 새로 생성
$ cookiecutter https://github.com/pydanny/cookiecutter-djangopackage.git

# 파이썬 패키지를 새로 생성
$ cookiecutter https://github.com//ionelmc/cookiecutter-pylibrary.git
```

프롬포트가 나오면, 해당 정보를 입력하고, 코드, 문서, 테스트, 라이선스, 기타 필요한 여러 파일을 포함한 Django, Python, 이외 패키지 템플릿의 기본 구현체가 생성됩니다.

## 23.12 Maintaining Your Open Source Package

> 오픈소스 패키지는 돈을 받고 하는 작업이 아닌 재미를 위한 자원봉사입니다. 자신의 페이스에 따라 최선을 다하는 선에서 진행하세요.
>

각각의 오픈 소스 패키지는 시간의 지남에 따라 성숙해지기도 하고, 필요에 따라 변화하기도 합니다.

다음은 오픈 소스 프로젝트 관리의 팁들입니다.

### 23.12.1 Give Credit for Pull Requests

누군가가 풀 요청이 반영되었다면 공로를 인정해야 합니다.

CONTRIBUTORS.txt 나 AUTHORS.txt 같은 프로젝트 저작자 문서에 공헌자의 이름을 반드시 추가해야합니다.

### 23.12.2 Handling Bad Pull Requests

반영될 수 없는 풀 요청들에 대해서 친절하고 긍적적인 자세로 반려시켜야 합니다.

- 반려 / 거부해야하는 요청들
    - 테스트 케이스를 통과하지 못한 풀 요청.
    - 테스트 범위를 벗어난 코드들.
    - 풀 요청은 가능한 한 최소의 범위에 대한 수정/변경이어야 합니다. 광범위한 내용이라면 세부적으로 나누고 독립적으로 처리해달라는 메시지와 함께 해당 요청을 거부해야 합니다.
    - 너무 복잡한 코드일 경우, 좀 더 단순하게 구성하거나 주석을 더 자세히 달아달라는 메시지와 함께 요청을 거부해야 합니다.
    - PEP-8 규약을 따르지 않은 코드는 수정을 요구해야 합니다.
    - 대부분이 빈 칸 정리로 이루어진 코드는 거부되어야 합니다. 이는 pull 요청의 diff는 기능적으로 읽을 수 없습니다. 공백 정리는 자체 pull 요청에 있어야 합니다.

### 23.12.3 Do Formal PyPI Releases

파이썬 세계에서는 작인 마이너 변경이나 버그 수정이 트렁크나 마스터에서 일어날 때마다 릴리스하는 것이 정통한 방법으로 알려져 있습니다.

언제 어떻게 릴리스해야 하는지 이해되지 않는다면 [python-request]([https://github.com/psf/requests/blob/master/HISTORY.md](https://github.com/psf/requests/blob/master/HISTORY.md))의 변경 이력을 살펴보세요.

배포할 준비가 되었다면 다음을 따라하면 됩니다.

```bash
$ pip install twine
$ python setup.py sdist
$ twine upload dist/*
```

> twine은 PyPI로 올리는데 선호되는 라이브러리입니다. python setup.py의 문제점은 SSH 연결을 이용하지 않는 문제점(중간자(man-in-the-middle) 공격에 쉽게 노출)이 있는 반면 twine은 인증된 TLS를 이용해 패키지를 업로드 합니다. 보안 문제를 중요시한다면 twine을 이용해야합니다.
>

### 23.12.4 Create and Deploy Wheels to PyPI

PEP 427에 따르면 Wheel은 새로운 파이썬 배포 표준입니다. egg를 대체하고 더 빠른 설치와 안전한 디지털 서명을 허용합니다. pip 1.4 이상, setuptools 0.8 이상에서 지원합니다.

```bash
$ pip install wheel
$ pip install twine
```

패키지를 PyPI로 배포 후 다음 명령을 따라해봅니다.

```bash
$ python setup.py bdist_wheel
$ twine upload dist/*
```

twine은 setup.cfg와 [setup.py](http://setup.py)이 같은 레벨에 위치하고 있고 다음 코드를 포함할 때 universal wheel을 생성합니다.

```bash
# setup.cfg
[wheel]
universal = 1
```

- [PEP 427 상세 규약]([https://www.python.org/dev/peps/pep-0427/](https://www.python.org/dev/peps/pep-0427/))
- [Wheel Package on PyPI]([https://pypi.org/project/wheel/](https://pypi.org/project/wheel/))
- [Documentation]([https://wheel.readthedocs.io/en/stable/](https://wheel.readthedocs.io/en/stable/))
- [Advocacy]([pythonwheels.com](http://pythonwheels.com/))

### 23.12.5 Add Git Tags to the Repo

repo안의 릴리스에 **git tag**를 지정해야합니다.

이건 릴리스가 PyPI에 제출되었을 때의 코드 스냅샷입니다.

뿐만 아니라 패키지를 설치하기 위한 장소를 가질 수 있습니다.

예를 들어, 개인 패키지 서버를 구축하지 않는 경우 git tag에 의존할 수 있습니다.

```bash
git tag -a v1.4 -m "my version 1.4"
git push prigin v1.4
```

- [ref]([https://git-scm.com/book/en/v2/Git-Basics-Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging))

### 23.12.6 Upgrade the Package to New Versions of Django

Django는 주기적으로 마이너 릴리스가 업데이트 되고, 약 1년 주기로 메이저 릴리스가 있습니다.

Django 업데이트가 있을 때마자 최신 Django 버전에 대한 패키지 테스트를 해야 합니다.

이때 virtualenv 환경을 이용해서 해야 합니다.

(프로젝트에 테스트 케이스를 포함해야 하는 중요한 이유들 중 하나입니다.)

### 23.12.7 Follow Good Security Practices

- [Alex Gaynor(core Django, Python, PyPy dev)]([https://alexgaynor.net/2013/oct/19/security-process-open-source-projects/](https://alexgaynor.net/2013/oct/19/security-process-open-source-projects/))

> "보안 취약성은 패키지의 사용자까지 위험에 빠뜨릴 수 있기 때문에, 사용자들을 위해서도 보안 취약성 문제로부터 안전하도록 도와야 할 의무가 있다" - Alex Gaynor
>

### 23.12.8 Provide Sample Base Templates

프로젝트를 이용한 기본적인 예제 템플릿을 제공해야 합니다.

단순한 HTML이나 Bootstrap 같은 프론트엔드 프레임워크를 이용하는 방법을 추천합니다.

또한 상호 운영성을 높이기 위해 templates/myapp/base.html 을 패키지에 포함시켜야 합니다.

- [cookiecutter-djangopackage 예제]([https://github.com/pydanny/cookiecutter-djangopackage/blob/master/{{cookiecutter.repo_name}}/{{cookiecutter.app_name}}/templates/{{cookiecutter.app_name}}/base.html](https://github.com/pydanny/cookiecutter-djangopackage/blob/master/%7B%7Bcookiecutter.repo_name%7D%7D/%7B%7Bcookiecutter.app_name%7D%7D/templates/%7B%7Bcookiecutter.app_name%7D%7D/base.html)) 참고

### 23.12.9 Give the Package Away

때때로 패키지에서 손을 때야 할 순간이 옵니다.

이땐 현재 프로젝트에서 활동적으로 참여하는 사람에게 권한을 넘겨 줌으로써 프로젝트는 다시 살아날 수 있습니다.

- 권한을 넘겨줌으로써 큰 주목과 존경을 받은 사례들
    - Ian Bicking and pip/virtualenv.
    - Daniel and Audrey Roy Greenfeld and djangopackages.org
    - Daniel Roy Greenfeld and django-crispy-forms, dj-stripe, and django-mongonaut
    - Audrey Roy Greenfeld and Cookiecutter
    - Rob Hudson and django-debug-toolbar.

## 23.13 Additional Reading

- [Django Apps Checklist]([https://devchecklists.com/django-apps-checklist/en/](https://devchecklists.com/django-apps-checklist/en/))
- [Effective Code Review]([https://alexgaynor.net/2013/sep/26/effective-code-review/](https://alexgaynor.net/2013/sep/26/effective-code-review/))
- [Sharing Your Labor of Love: PyPI Quick and Dirty]([https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/](https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/))

## 23.14 Summary

Django의 진짜 힘은 방대한 양의 서드 파티 패키지입니다.

pip와 virtualenv의 사용법을 꼭 익혀두세요.

현존하는 패키지들에 친숙해지세요. PyPI와 Django Packages들에서 정보를 얻으세요.

좋은 패키지는 패키지 성숙도, 문서화, 테스트, 코드 품질로 판단할 수 있습니다.

프로젝트 규모와 상관없이 안정적인 패키지 설치는 가장 기본적인 조건입니다.

이는 프로젝트의 트렁크나 마스터를 이용하는 것이 아니라 특정 릴리스를 정해 이용할 수 있어야한다는 의미입니다.

특정 릴리스가 없다면 최소한 특별한 커밋을 이용할 수 있어야 합니다.

프로젝트에서 문제를 만난다면 도움을 청할 수 있다는 것을 기억하세요.
