# Ch 05. Settings and Requirements Files

- 모든 settings 파일은 git으로 관리해라
- 복사, 붙여넣기 하지 말고 base settings를 상속도록 해라
- secret-key는 git에 포함되지 않도록 안전하게 관리해라

### 5.1 버전 관리되지 않는 로컬 세팅은 피하도록 하자.

- 일반적인 해결 방법으로 local_settings.py 모듈을 생성하고 해당 파일을 각 서버나 개발 머신에 위치시켜, 이 파일을 git에서 빼버리는 방법
- 이 방법의 단점
    - 모든 머신에 git에 포함되지 않는 코드가 존재하게 됨
    - 운영환경에서만 발생하는 문제점에 대한 파악이 어려움
    - 개발환경에 커스터마이징된 local_settings.py 모듈에 기인한 문제 발생
    - local_settings.py를 팀원들이 복사해서 사용함으로써 같은 일을 반복하지 말라는 규칙을 위반
- 다른 방안
    - 개발 환경, 스테이징 환경, 테스트 환경, 운영 환경 설정을 공통되는 객체로부터 상속받아 구성된 서로 다른 세팅 파일로 난누어 버전 컨트롤 시스템에서 관리하는 것, 그런 다음 이러한 상태에서 서버의 암호 정보 등을 버전 컨트롤에서 빼서 비밀스럽게 유지하는 것.

### 5.2 여러 개의 settings 파일 이용하기

- settings/ 디렉터리 아래에 여러 개의 셋업 파일을 구성하여 이용

    ex)

    settings/

    __inti__.py

    base.py

    local.py

    staging.py

    test.py

    production.py

    - [base.py](http://base.py) : 프로젝트의 모든 인스턴스에 적용되는 공용 세팅 파일
    - [local.py](http://local.py) : 로컬 환경에서 작업할 때 쓰이는 파일. 디버그 모드, 로그 레벨, django-debug-toolbar 같은 도구 등이 설정되어 있는 개발 전용 로컬 파일.
    - [staging.py](http://staging.py) : 운영 환경으로 코드를 이전하기 전에 고객 및 관리자들의 확인을 위한 세미-프라이빗 버전의 스테이징 서버를 위한 파일
    - [test.py](http://test.py) : 테스트 러너, 인메모리 데이터베이스 정의, 로그 세팅 등을 포함한 테스트를 위한 세팅
    - [production.py](http://production.py) : 운영 서버에서 실제로 운영되는 세팅 파일, 운영 서버에서만 필요한 설정이 들어있다.

### 5.2.1 개발 환경의 [settings.py](http://settings.py) 예제

- from .base import * 을 통해서 사용
- 디버스 모드, 콘솔 환경에서의 메일 설정, 여러 개발 환경에서만 적용이 필요한 설정들을 포함
- $ python manage.py runserver --settings=config.settings.local

### 5.2.2 다중 개발 환경 세팅

- 사이즈가 큰 프로젝트에서 각 개발자 별로 다른 환경이 필요한 경우, [local.py](http://local.py) 를 같이 사용하는 것이 불가능 할 수 있다.
- git에서 관리되는 파일들로 구성하여 이용해라

    ex) local_audrey.py & local_pydanny.py

    - 개발환경을 git 포함하는 것이 좋으며
    - 팀원 간 서로의 개발 세팅 파일을 참고하는 것이 가능하다.

### 5.3 코드에서 설정 분리하기

- 설정을 분리하는 이유는 SECRET_KEY, AWS 키, API 키 또는 서버에 따라 특별하게 설정된 값들이 세팅 파일에 포함되기 때문이다.
    - 설정은 배포 환경에 따라 다르지만 코드는 그렇지 않다.
    - 비밀 키들은 설정값들이지 코드가 아니다.
    - 비밀 키들은 git에 포함되지 않도록 관리하여 비밀을 유지해야 한다.
    - PasS 환경에서는 각각의 서버에서 코드를 수정하는 것을 허용하지 않는다. 이것은 매우 위험한 일이다.
- 이를 해결하기 위해서 환경변수를 사용할 것을 추천한다.
- 장고는 운영체제의 환경 변수를 손쉽게 설정할 수 있는 기능을 제공하고 있음
- 환경변수를 통해 비밀키를 관리함으로써 장점
    - 환경 변수를 이용하면 걱정없이 세팅 파일을 git에 포함할 수 있다. 모든 파이썬 파일은 git으로 관리되어야 한다.
    - git으로 관리되는 모두가 동일한 settings/local.py를 나눠 쓸 수 있다.(복사/붙여넣기 X)
    - 파이썬 코드의 수정 없이 시스템 관리자들이 프로젝트 코드를 쉽게 배포할 수 있다.
    - 대부분의 PasS에서 환경변수를 통한 설정을 권장하며, 이러한 기능을 제공

### 5.3.1 환경 변수에 비밀 키를 넣기 전에 주의할 점

- 고려해야 할 점
    - 저장하는 비밀 정보를 관리할 방법 ?????????????????
    - 서버에서의 bash가 환경변수를 이용하는 작동 원리에 대한 이해 or PasS 이용 여부

### 5.3.2 로컬 환경에서 환경 변수 세팅하기

- 아래 문장을 bashrc, .bash_profile, .profile의 뒷부분에 추가하면 된다.
- 각기 다른 API 키를 동일한 API를 사용하는 여러 프로젝트의 경우, virtualenv의 /bin/acticate 스트팁트의 맨 마지막 부분에 추가하면 된다.
- $ export SOME_SECRET_KEY=1c3-cr3am-15-yummy
$ export AUDREY_FREEZER_KEY=y34h-r1ght-d0nt-t0uch-my-1c3-cr34m

### 5.3.3 로컬 환경에서 환경변수 해제하기

### 5.3.4 운영 환경에서 환경변수 세팅하기

- 파이썬에서 환경 변수로 접근하기 ⇒ 이러한 패턴을 이용하여 모든 코드가 git에 포함되면서 비밀 값들을 안전하게 유지할 수 있다.

    ```python
    import os
    os.environ['SOME_SECRET_KEY']

    #Top of settings/production.py
    import os
    SOME_SECRET_KEY = os.environ['SOME_SECRET_KEY']
    ```

### 5.3.5 비밀키가 존재하지 않을 때 예외 처리하기

```python
# settings/base.py
import os
# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
	"""Get the environment variable or return exception."""
	try:
		return os.environ[var_name]
	except KeyError:
		error_msg = 'Set the {} environment
		→ variable'.format(var_name)
		raise ImproperlyConfigured(error_msg)
```

### 5.4 환경 변수를 이용할 수 없을 때

- Apache나 Nginx기반 환경에서 환경 변수를 사용하지 못할 수 있다.
⇒ 이때 시크릿 파일 패턴을 사용하라
    1. JSON, .env, Config, YAML, XML 중 포멧을 선택하여 파일 생성
    2. 비밀관리를 위한 시크릿 로더 추가
    3. 해당 파일을 .gitignore 에 추가

### 5.4.1 JSON 파일 사용하기

```json
{
	"FILENAME": "secrets.json",
	"SECRET_KEY": "I've got a secret!",
	"DATABASES_HOST": "127.0.0.1",
	"PORT": "5432"
}
```

```python
# settings/base.py
import json

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

# JSON-based secrets module
with open('secrets.json') as f:
	secrets = json.load(f)

def get_secret(setting, secrets=secrets):
	'''Get the secret variable or return explicit exception.'''
	try:
		return secrets[setting]
	except KeyError:
		error_msg = 'Set the {0} environment
		→ variable'.format(setting)
		raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret('SECRET_KEY')
```

### 5.5 여러 개의 requirements 파일 사용하기

- 각 서버 마다 각각에 맞게 requirements 파일이 필요하다.
- repository_root에 아래와 같이 만들어라

    requirements/

    base.txt

    local.txt

    staging.txt

    production.txt

    - base.txt : 모든 환경에서 공통적으로 사용하는 디펜던시를 작성

### 5.5.1 여러 개의 requirements 파일로부터 설치하기

- $ pip install -r requirements/local.txt
$ pip install -r requirements/production.txt

### 5.6 settings에서 파일 결로 처리하기

- 절대 하드 코딩된(고정 경로) 파일 경로를 장고 세팅 파일에 넣지 말라

    ex) MEDIA_ROOT = '/Users/pydanny/twoscoops_project/media'

- 추천하는 경로

    ex) MEDIA_ROOT = BASE_DIR / 'media'

- 파이썬 기본 라이브러리인 os.path 이용하는 방법

    ```python
    def root(*dirs):
    	base_dir = join(dirname(__file__), '..', '..')
    	return abspath(join(base_dir, *dirs))

    BASE_DIR = root()
    MEDIA_ROOT = root('media')
    STATIC_ROOT = root('static_root')
    ```

### 5.7 요약

- 비밀번호나 API 키값을 제외하고는 모두 git을 통해 관리되어야 한다는 것을 명심하라.
