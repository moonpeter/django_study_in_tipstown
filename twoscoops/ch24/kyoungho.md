# Testing Stinks and Is a Waste of Money!

## 24.1 Testing Saves Money, Jobs, and Lives

- 테스트의 중요성 및 필요성에 대해서 설명
  - 테스트 하지 않는 코드로 인하여 손실을 입을 수 있고 그로 인해 직장도 잃고 의료보험도 잃어 생명까지도 위협받는 다는 이야기
- 필자는 coverage.py 사용을 선호한다고 함

## 24.2 How to Structure Tests

- 장고 앱을 생성할 때 기본으로 만들어지는 tests.py를 삭제하도록 하자

  - 각각의 기능에 맞는 테스트 파일을("test_" 접두어를 붙여서) 따로 만들도록 하자

    - test_forms.py, test_models.py, test_views.py 와 같이
    - ```di
      tests/
      	__init__.py
      	test_forms.py
      	test_models.py
      	test_views.py
      ```

## 24.4 How to write Unit Tests

- 단위테스트에 대한 필자의 방법론

### 24.3.1 Each Test Method Tests One Thing

- 테스트 메서드는 그 테스트 범위가 좁아야 한다.
  - 하나의 단위테스트는 여러 개의 뷰나 모델 폼, 한 클래스의 여러 메서드를 담당해서는 안된다.
  - 그러나 뷰 하나만으로도 모델, 폼, 메서드, 함수가 연관지어 호출되기 때문에 여려움이 있다.
  - 환경을 최소한으로 구성하여 해당 문제를 피할 수 있다.
    - 테스트 실행을 위한 최소한의 레코드를 setUp() 메서드를 사용하여 생성

      ```python
      # flavors/tests/test_api.py
      import json
      from django.test import TestCase
      from django.urls import reverse

      from flavors.models import Flavor

      class FlavorAPITests(TestCase):

          def setUp(self):
      	Flavor.objects.get_or_create(title='A Title', slug='a-slug')

          def test_list(self):
      	url = reverse('flavors:flavor_object_api')
      	response = self.client.get(url)
      	self.assertEquals(response.stasus_code, 200)
      	data = json.loads(response.content)
      	self.assertEquals(len(data), 1)
      ```
    - ```python
      # flavors/tests/test_api.py

      import json

      from django.test import TestCase
      from django.urls import reverse

      from flavors.models import Flavor

      class DjangoRestFrameworkTests(TestCase):

          def setUp(self):
      	Flavor.objects.get_or_create(title='title1', slug='slug1')
      	Flavor.objects.get_or_create(title='title2', slug='slug2')

      	self.create_read_url = reverse('flavors:flavor_rest_api')
      	self.read_update_delete_url = reverse('flavors:flavor_rest_api', kwargs={'slug': 'slug1'})

          def test_list(self):
      	response = self.client.get(self.create_read_url)

      	# 생성된 두 타이틀 확인
      	self.assertContains(response, 'title1')
      	self.assertContains(response, 'title2')

          def test_detail(self):
      	response = self.client.get(self.read_update_delete_url)
      	data = json.loads(response.content)
      	content = {'id': 1, 'title': 'title1', 'slug': 'slug1', 'scoops_remaining': 0}
      	self.assertEquals(data, content)

          def test_create(self):
      	post = {'title': 'title3', 'slug': 'slug3'}
      	response = self.client.post(self.create_read_url, post)
      	data = json.loads(response.content)
      	self.assertEquals(response.status_code, 201)
      	content = {'id': 3, 'title': 'title3', 'slug': 'slug3', 'scoops_remaining': 0}
      	self.assertEquals(data, content)
      	self.assertEquals(Flavor.objects.count(), 3)

          def test_delete(self):
      	response = self.client.delete(self.read_update_delete_url)
      	self.assertEquals(response.status_code, 204)
      	self.assertEquals(Flavor.objects.count(), 1)

      ```

### 24.3.2 For Views, When Possible Use the Request Factory

- django.test.client.RequestFactory는 모든 뷰에 대해 첫 번째 인자로 이용할 수 있는 인스턴스를 제공
  - 기본 장고 테스트 클라이언트보다 독립된 환경을 제공
  - 단, 세션과 인증을 포함한 미들웨어를 지원하지 않기 때문에 추가적인 작업이 요구된다.
  - 세션을 필요로 하는 뷰를 테스트 하고자 하면 아래와 같이 작성 할 수 있다.
  - ```python
    from django.contrib.auth.models import AnonymousUser
    from django.contrib.sessions.middleware import SessionMiddleware
    from django.test import TestCase, RequestFactory

    form .views import cheese_flavors

    def add_middleware_to_request(request, middleware_class):
        middleware = middleware_class()
        middleware.process_request(request)
        return request

    def add_middleware_to_response(request, middleware_class):
        middleware = middleware_class()
        middleware.process_response(request)
        return request

    class SavoryIceCreamTest(TestCase):
        def setUp(self):
            self.factory = RequestFactory()

        def test_cheese_flavors(self):
    	request = self.factory.get('/cheesy/broccoli/')
    	request.user = AnonymousUser()

    	request = add_middleware_to_request(request, SessionMiddleware)
    	request.session.save()

    	response = cheese_flavors(request)
    	self.assertContains(response, 'bleah!')
    ```

### 24.3.3 Don't Write Tests That Have to be Tested

- 테스트가 필요한 테스트 코드는 작성하지 말자.
  - 가능한 단순하게 작성하라

### 24.3.4 Don't Repeat Yourself Doesn't Apply to Writing Tests

- 테스트 코드에 대해서는 반복적인 코드를 작성해도 된다.
  - setUp() 메서드가 유용하긴 하지만, 복잡한 테스트 유틸리티를 만드는 실수를 하지 말라.
  - 여러 비슷한 테스트 케이스를 작성하는 대신 하나의 메서드로 복잡하게 만드는 경우가 있는데, 차라리 반복적인 코드를 여러번 쓰는 것이 나은 선택이다.

### 24.3.5 Dont Rely on Fixtures

- 픽스처를 사용하는 것이 문제를 더 일으킬 수 있다.
- ORM에 의존하는 코드를 제작하는 편이 훨씬 쉽다.
- 테스트 데이터를 생성해 주는 도구
  - factory boy
  - faker
  - model bakery
  - mock - 목 객체를 생성, 파이썬 3.3부터는 표준 라이브러리로 채택

### 24.3.6 Things That Should Be Tested

- 테스트 해야 할 대상들 - 물론 모두 다 해야한다.
  - 뷰
  - 모델
  - 폼
  - Validators - 최대한 다양한 케이스를 고민해보라
  - 시그널
  - 필터
  - 탬플릿 테그
  - 기타: 콘텍스트 프로세서, 미들웨어, 이메일, 목록에 포함되지 않은 모든 것
- 프로젝트 안에서 테스트가 필요 없는 부분
  - 장고 코 부분
  - 서드 파티 패키지에서 이미 테스트가 된 부분
  - 모델 부분
    - 단, 새로운 필드 타입을 생성하는 경우라면 해야함.

### 24.3.7 Test for Failure

- 테스트의 성공이 문제 없을 보장하지는 않는다.

### 24.3.8 Use Mock to Keep Unit Tests From Touching The World

- 단위테스트는 그 자체가 호출하는 함수나 메서드 이외의 것을 테스트 하지 않도록 되어 있다.
- 테스트 외적인 환경에 대한 액션(외부 API에 대한 접속, 이메일 수신, 웹훅) 필요한 경우 아래와 같은 선택을 고려하라
  1. 통합테스트로 변경
  2. Mock 라이브러리를 통해 외부 API에 대한 가짜 리스펀스 생성
- Mock 라이브러리는 테스트를 위해 특정한 값의 반환을 필요할 때 이용 할 수 있는 monkey patch 라이브러리를 제공
  - 이를 통해 외부 API에 대한 유효성 검사가 아닌 우리 코드에 대한 로직을 검사하게 됨
  - monkey patch : 프로그램이 시스템 소프트웨어를 개별적으로 확장 또는 수정하는 방법을 의미

### 24.3.9 Use Fancier Assertion Methods

- 유용한 assertion methods
  - assertRaises
  - assertRaisesMessage()
  - assertCountEqual()
  - assertDictEqual()
  - assertFormError()
  - assertContains()
  - assertHTMLEqual()
  - assertInHTML()
  - assertJSONEqual()
  - assertURLEqual()

### 24.3.10 Document the Purpose of Each Test

- 문서화 되지 않은 테스트 코드는 테스트를 불가능하게 할 수 도 있다.

## 24.4 What About Integration Test?

- 통합 테스트
  - 개별적인 소트프웨어 모듈이 하나의 그룹으로 테스트되는 것
  - 단위테스트가 끝난 후에 하는 것이 이상적
  - ex
    - 셀레니움 테스트
    - 실제 테스트(Mock 리스펀스 말고)
    - 아웃바운드 리퀘스트 테스트 - httpbin.io
    - API 작동 테스트 - runscope.com or postman.com
  - 문제점
    - 세팅에 많은 시간이 필요
    - 단위 테스트에 속도가 느리다.
    - 에러 발생에 대한 원인 파악이 어렵다.
    - 작은 변경에도 전체 테스트에 문제를 일으킬 수 있다.
    - 그럼에도 통합테스트는 꼭 진행해야 한다.

## 24.5 Continuous Integration

- 커밋될 때마다 테스트가 실행되도록 CI를 세팅해라(어떠한 크기의 프로젝트라도)
- 34장에서 자세히 다룸

## 24.6 Who Cares? We Dont Have Time for Tests!

- 테스트 코드를 짜고 실행하는게 시간과 비용이 더 걸리는 것처럼 느껴질 수 있겠지만, 넓게 보면 두가지 모두 단축 시켜줄 것이며 꼭 필요하다는 내용

## 24.7 The Game of Test Coverage & 24.8 Setting Up the Test Coverage Game & 24.9 Playing the Game of Test Coverage

- 최대한 테스트 커버리지를 증가시키는 게임
- 단계
  - 1. 테스트 작성하기
    2. 테스트 실행 및 커버리지 리포트 작성

       ```
       $ coverage run manage.py test -settings-twoscoops.settings.test
       ```
    3. 리포트 생성

       ```
       $ coverage html --omit="admin.py"
       ```
- 규칙
  - 커버리지를 낮추는 커밋은 절대 하지 않기!


## 24.10 Alternatives to unittest

- Unittest의 대안
  - pytest
  - nose
