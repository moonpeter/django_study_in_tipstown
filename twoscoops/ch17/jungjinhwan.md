오늘날의 인터넷은 HTML 기반 웹사이트 그 이상입니다. 개발자는 웹 클라이언트, 네이티브 모바일 앱, B2B 어플리케이션을 지원하는 개발을 해야합니다. 쉽게 작성 가능한 JSON, YAML, XML, 기타 포맷 등을 지원하는 것은 중요합니다. REST API 설계를 통해서 어플리케이션의 데이터를 다른 관심사로 노출합니다(By design, a Representational State Transfer (REST) Application Programming Interface (API) exposes application data to other concerns.)

장고에서 이러한 REST API 를 만드는 패키지가 Django REST Framework(이하 DRF) 입니다.사실, Django 와 DRF 가 다른점이 무엇인지 질문하는 일은 자주 일어납니다. 약 2013년도 이후 API 를 갖춘 신규 Django 프로젝트의 90~95%는 DRF 를 사용한 것으로 추정되고 있습니다.

왜 인기가 좋을까요? DRF 가 성공한 요인은 다음과 같습니다.
- DRF 객체지향적 설계로 되어있고 확장이 쉽도록 설계되어 있습니다.
- DRF 는 장고 CBV 에서 직접적으로 구축됩니다. 때문에 당신이 CBV를 이해하고 있다면, DRF 디자인을 장고의 연장선에서 이해할 것입니다.
- API 생성을 위한 다양한 view, 일반적인 API 뷰 그리고 뷰셋에 대한 django.views.generic.View 와 유사한 API View를 제공합니다.
- 시리얼라이저는 굉장히 강력하지만 사용하지 않거나 교체될 수 있습니다.
- 인증과 인가는 강력하고 확장 가능한 방식으로 제공됩니다.
- 만약 FBV 로 API 를 작성하고 싶다면 이것 또한 지원합니다.

이러한 이유들로, DRF 매우 큽니다. 이는 REST API 를 구축하는데 많은 문제들이 해결되었음을 의미하므로 중요합니다. 
우리는 새로운 API 패러다임인 18장 GraphQL API 만들기도 볼 것이다.

만약 DRF 를 어떻게 사용하는지 아직 모른다면, 우리는 공식 튜토리얼을 추천한다.
- https://www.django-rest-framework.org/tutorial/quickstart/
- https://www.django-rest-framework.org/tutorial/1-serialization/



#### 팁 : Django REST Framework 는 당신의 지원이 필요합니다!

```
DRF 는 공동 자금을 지원하는 프로젝트 입니다. 상업적으로 사용하는 경우, 유로플랜에 가입하여 지속적인 개발에 투자할 것을 권장합니다. 이 자금들 덕분에 우리는 프로젝트가 기능면에서 도약하는 것을 보았습니다. 재정 기부는 15달러에서 시작하여 올라갑니다. 더 높은 수준에서 DRF 프로젝트는 우선 지원도 제공합니다.
```



## 17.1 기본 REST API 설계의 기초

HTTP 와 DRF가 어떻게 상호작용 하는지에 대해서 차근차근 살펴봅시다. 

HTTP 는 정의된 액션 메서드를 통해 콘테츠를 전달하는 프로토콜입니다. REST API 의 관례는 이러한 액션들을 의존하고 있습니다. 따라서 각 동작 별 적합한 HTTP 메서드를 살펴보면 다음과 같습니다.


| 요청목적                             | HTTP 메서드 | 대응되는 SQL |
| ------------------------------------ | ----------- | ------------ |
| 새로운 리소스 생성                   | POST        | INSERT       |
| 기존 리소스 읽기                     | GET         | SELECT       |
| 기존 리소스 수정                     | PUT         | UPDATE       |
| 기존 리소스 일부분 수정              | PATCH       | UPDATE       |
| 기존 리소스 제거                     | DELETE      | DELETE       |
| GET 의 HTTP 헤더만을 반환(body 없음) | HEAD        |              |
| 요청을 다시 반환                     | TRACE       |              |



위 표에 대한 몇가지 주의할 사항은 다음과 같습니다.

- 읽기전용 API 를 구현한다면, GET 메서드만 구현하면 됩니다.
- 읽기, 쓰기에 대한 API 를 구현한다면, GET, POST, PUT, DELETE 메서드를 사용해야 될 것입니다.
- GET 과 POST 만을 사용하여 모든 작업을 제공하는 것은 API 유저에게 좌절스러운 패턴일 수 있습니다.
- GET, PUT, DELETE 는 멱등성을 보장해야 합니다. POST, PATCH 는 멱등하지 않습니다.
- PATCH 종종 구현되지 않지만, API 가 PUT 요청을 지원하는 경우라면 PATCH 도 구현하는 것이 좋은 생각입니다.
- DRF 는 이러한 메서드들에 대해 이해하기 쉬우며 DRF 자체 또한 이해하기 쉽게 설계되었습니다.



여기 REST API 를 구현할 때 고려해야 할 일반적인 HTTP 상태코드가 있습니다. DRF 의 일반적인 View 와 ViewSet 은 호출되는 요청 메서드에 따라 적절한 상태코드를 반환합니다. 이것은 일부분임을 주의하십시오. 더 많은 상태코드에 대해서는 여기서 찾아볼 수 있습니다. https://en.wikipedia.org/wiki/List_of_HTTP_status_codes



| HTTP 상태코드          | 성공/실패  | 의미                                                         |
| :--------------------- | :--------- | :----------------------------------------------------------- |
| 200 OK                 | 성공       | GET - 리소스 반환 <br />PUT - 상태 메시지 제공, 리소스 반환  |
| 201 Created            | 성공       | POST - 상태 메시지 제공, 새로 생성된 리소스 반환             |
| 204 No Content         | 성공       | PUT, DELETE - 제거, 업데이트 요청에 대한 성공적인 응답       |
| 304 Not Modified       | 리다이렉트 | ALL - 지난 마지막 요청 이후 변화된 사항이 없음.<br />성능을 위해 Last Modified 와 ETag 헤더를 확인 |
| 400 Bad Request        | 실패       | ALL - 유효성 에러애 대한 에러 메시지를 반환                  |
| 401 Unauthorized       | 실패       | ALL - 인증 필요.<br />유저 인증정보가 제공되지 않았거나 제공되었으나 유효하지 않은경우 |
| 403 Forbidden          | 실패       | ALL - 유저가 접근 제한된 콘텐츠를 요청하였음                 |
| 404 Not Found          | 실패       | ALL - 리소스를 찾지 못함                                     |
| 405 Method Not Allowed | 실패       | ALL - 허용되지 않는 HTTP 메서드를 요청하였음                 |
| 410 Gone               | 실패       | ALL - 요청한 원본에 대해 더이상 사용할 수 없음.<br />API 가 새로운 버전이 생겨서 종료될 때 사용됨.<br />모바일 앱에서 이 상태를 테스트 하여<br />문제가 발생시 사용자에게 업그레이드를 안내를 할 수 있음 |
| 429 Too Many Requests  | 실패       | ALL - 유저가 주어진 시간동안 너무 많은 요청을 보냈다.<br />요청속도 제한과 함께 사용된다 |



## 17.2 간단한 API 로 디자인 개념 설명하기

HTTP 메서드들과 HTTP 상태코드, 직렬화, views 모듈에 대해 DRF 가 어떻게 동작하는지 설명하기 위해서, 간단한 JSON API 를 만들어 봅시다. 우리는 이전 챕터의 flavors app 를 사용할 것입니다. AJAX(혹은 python-requests, 다른 라이브러리 등)을 이용한 HTTP 요청을 통해 flavor 를 생성, 읽기, 갱신, 제거 할수 있도록 API 를 제공할 것입니다. 



##### example 17.1: 기본 DRF 권한 클래스 표준설정

```python
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
}

```



#### 팁 : IsAdminUser 기본 권한 클래스

```
우리의 REST API 는 제한할 것입니다. `rest_framework.permissions.IsAdminUser` 와 같이 설정하는것은 좋은 방법입니다. 이것은 뷰 마다 오버라이딩을 할 수 있게 되는 것입니다. API 뷰가 기본적으로 안전해지며 API 뷰에 추가적인 코드를 작성하는 것 보다 더 좋습니다.
```



이 과정에서 여기 Flavor 모델을 다시한번 보면, API 조회를 위해 UUID 필드 사용을 추가하는 것으로 향상되었습니다.



##### example 17.2: REST API 에서 사용될 Flavor 모델

```python
# flavors/models.py
import uuid as uuid_lib

from django.db import models
from django.urls import reverse


class Flavor(models.Model):
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)  # 웹 URL 을 찾을 때 사용됨
  uuid = models.UUIDField(  # API 조회에서 사용됨
    db_index=True,
    default=uuid.uuid4,
    editable=False,
  )
  scoops_remaining = models.IntegerField(default=0)
  
  def get_absolute_url(self):
    return reverse('flavors:detail', kwargs={'slug': self.slug})
  
```



#### 주의 : 공개적인 ID 로 순차적인 Key를 사용하지 마세요!

```tex
순차적인 키(예를들어, 장고 모델의 기본 생성되는 Primary Key)는 공개적으로 사용할 경우 보안적인 문제가 될 수 있습니다. 우리는 Section 28.28 : Nerver Display Sequential Primary Keys 에서 이 내용을 깊이 다룹니다.

여기 예제에서는, 모델 리소스 하나를 찾을 때 UUID 를 Primary Key 대신 사용할 것입니다. 우리는 항상 조회에서 순차적인 숫자를 사용하는 것을 피해야 합니다.
```



시리얼라이져(serializer) 클래스 정의합니다.



##### Example 17:3: Flavor 모델 시리얼라이저

```python
# flavors/api/serializers.py
from rest_framework import serializers

from ..models import Flavor


class FlavorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Flavor
    fields = ['title', 'slug', 'uuid', 'scoops_remaining']

```



이제 API 뷰를 추가해봅시다.

##### Example 17.4: Flavor API 뷰

```python
# flavors/api/views.py
from rest_framework.generics import (
  ListCreateAPIView,
  RetrieveUpdateDestoryAPIView,
)
from rest_framework.permissions import IsAuthenticated

from ..models import Flavor
from .serializers import FlavorSerializer


class FlavorListCreateAPIView(ListCreateAPIView):
  queryset = Flavor.objects.all()
  permission_classes = (IsAuthenticated, )
  serializer_class = FlavorSerializer
  lookup_field = 'uuid'  # Don't use Flavor.id!
  
  
 class FlavorRetrieveUpdateDestoryAPIView(RetrieveUpdateDestoryAPIView):
  queryset = Flavor.objects.all()
  permission_classes = (IsAuthenticated, )
  serializer_class = FlavorSerializer
  lookup_field = 'uuid'  # Don't use Flavor.id!
 
```



끝이다! 빠르지 않은가?



#### 팁 : Classy DRF 레퍼런스

```
DRF 의 동작에 대해서, 매우 좋은 cheat sheet 를 발견했다. https://cdrf.co 사이트다.
ccbv.co.uk 레퍼런스 사이트와 유사하게 시작된 패턴을 DRF 기준으로 제공한다.
```



 이제 `flavors/urls.py` 를 작성해볼 것이다.

##### example 17.5: urls 작성

```python
# flavors/urls.py
from django.urls import path
from flavors.api import views


urlpatterns = [
	# /flavors/api/
  path(
    route='api/',
    view=views.FlavorListCreateAPIView.as_view(),
    name='flavor_rest_api'
  ),
  path(
    route='api/<uuid:uuid>/',
    view=views.FlavorRetrieveUpdateDestoryAPIView.as_view(),
    name='flavor_rest_api'
  ),
]

```



우리가 하고 있는 것은 URLConf 이름을 재사용하는 것입니다. Javascript 프론트에서 필요할 때 쉽게 관리할 수 있습니다. 모든 Flavor 리소스는 `{% url %}` 템플릿 태그를 통해 접근하면 됩니다.



URLConf 가 무엇을 하고 있는지 명확하지 않다면, 아래 테이블을 통해 확인해봅시다.

| Url                | View                               | Url Name (same) |
| ------------------ | ---------------------------------- | --------------- |
| /flavors/api/      | FlavorListCreateAPIView            | flavor_rest_api |
| flavors/api/:uuid/ | FlavorRetrieveUpdateDestoryAPIView | flavor_rest_api |



결과적으로 전통적인 REST 스타일의 API 가 정의되었습니다.

##### example 17.6: 전통적인 REST 스타일 API 정의

```
flavors/api/
flavors/api/:uuid/
```



#### 경고: 우리의 API 는 권한처리를 하지 않았습니다.

```
우리는 기본 IsAdmin 권한을 IsAuthenticated 권한으로 오버라이딩 했습니다. 만약 이 예제를 사용해서 API 를 구현한다면, 잊지말고 적절한 유저 권한처리를 할당하세요!
- https://www.django-rest-framework.org/api-guide/authentication/
- https://www.django-rest-framework.org/api-guide/permissions/
```



#### 팁: REST API 설명에 대한 일반적인 문법

```
API 뷰 코드와 관련된것 같은 코드는 드문일이 아닙니다. /flavors/api/:uuid 경우에 :uuid 는 값입니다. 이러한 변수 표현 방식은 다른 REST API 나 프레임워크 및 언어에서도 볼수있는 적합한 방식입니다.
```



우리는 REST API 를 장고에서 만들기가 얼마나 쉬운지 보여주었다. 이제 유지보수 및 확장에 관련된 조언을 살펴보자.



## 17.3 REST API 아키텍처

DRF를 통해 간단하고, 빠르게 API를 만드는 것은 쉽습니다. 하지만, 당신의 프로젝트에 적합하게 확장하고 유지보수하는 것은 좀더 생각이 필요합니다. 이것은 일반적으로 사람들이 API 디자인에 매달리는 포인트입니다. 여기 그 디자인을 향상하는 몇가지 팁들이 있습니다.



### 17.3.1 일관된 API 모듈 이름을 사용하기

다른것과 마찬가지로, 어떤 네이밍을 하느냐는 프로젝트 전반에 일관성이 있어야 합니다. 우리의 API 디자인과 관련된 모듈 네이밍 설정은 다음을 따를 것입니다.



##### example 17.7: API 와 관련된 모듈 네이밍 설정

```
flavors/
| - api/
|  | - __init__.py
|  | - authentication.py
|  | - parsers.py
|  | - permissions.py
|  | - renderers.py
|  | - serializers.py
|  | - validators.py
|  | - views.py
|  | - viewsets.py
```



아래 사항들에 대해서 살펴보십시오.

- `api/` 라는 앱 안의 패키지 내에 모든 API 컴포넌트들을 위치시킵니다. 이를통해 API 컴포넌트를 일관된 위치에 격리할 수 있습니다. 만약 앱 폴더의 root 에 위치시켰다면, API 에 특화된 모듈들이 앱의 이반영역에서 길게 늘어졌을 것입니다.
- Viewsets 은 그 자체 모듈에 속합니다. (?)
- 앱 또는 프로젝트 수준의`urls.py` 에 라우터를 위치시킵니다. 



### 17.3.2 프로젝트의 코드를 깔끔하게 구성하기

상호 연결된 작은 앱이 많은 프로젝트의 경우 특정 API 보기가 있는 위치를 찾기가 어려울 수 있습니다. 각 관련 앱 내에 API 코드를 배치하는 것과 반대로, 때로는 API 용 앱을 별도로 빌드하는 것이 합리적입니다. 여기에 모든 serializers, renderes, views 를 배치합니다. 그리므로, 앱의 이름은 API 버전을 반영해야 합니다. ("Section 17.3.7 API 버전" 을 보세요.)

예를들어, `apiv4` 라고 작명한 앱에 API 컴포넌트들(Serializers, Views, 기타 등등)을 배치할 수 있습니다.

단점으로는, API 앱이 너무 커질 가능성이 있고 다른 앱들과의 연결이 끊어질 수도 있습니다. 따라서, 다음 섹션에서 대안을 고려해봅니다.



### 17.3.3 앱에대한 코드는 앱에 남겨두기



### 17.3.3 앱 관련 코드는 앱 안에 두기

결론적으로, REST API들은 views 일 뿐입니다. 더 간단하고 작은 프로젝트를 위해 REST API 의 views 는 `views.py` 혹은 `viewsets.py` 모듈로 이동해야 하며, 다른 views 들과 마찬가지로 동일한 우리의 지침을 따르면 됩니다. 앱 또는 모델 별 serializer 와 renderer 도 마찬가지 입니다.

REST API 의 view 클래스 많은 단일 `api/views.py` 또는 `api/viewsets.py` 모듈이 탐색이 어려운 경우, 이를 분할할 수 있습니다. 일반적으로 특정 모델 이름을 딴 Python 모듈이 포함된 `api/views/` 또는 `api/viewsets`/ 패키지로 이동합니다.



```tex
flavors/
  |-- api/
  |   |-- __init__.py
  |   |-- ... other modules here
  |   |-- views
  |   |--   |-- __init__.py
  |   |--   |-- flvor.py
  |   |--   |-- ingredient.py
```



이 접근방식의 단점은 작은 상호연결앱이 너무 많으면 API 구성요소가 배치된 수많은 위치를 찾기 어려울 수 있다는 것입니다. 따라서 이전 섹션에서 다른 접근방식을 고려했었습니다.



### 17.3.4 API 뷰에 비즈니스 로직을 넣지 않도록 하기

어떤 아키텍처를 취하든 API views 이외에 가능한 많이 로직을 위치시키는 것이 좋은 생각입니다. "Section 8.5: Try to Keep Business Logic Out of Views" 에서 다뤘던 내용입니다. 결국 API views 는 단지 또다른 views 일 뿐이라는 걸 기억하세요.



![image-20211117182058275](/Users/jungjinhwan/Library/Application Support/typora-user-images/image-20211117182058275.png)

> 그림 17.1 : 아이스크림 서비스 API



### 17.3.5 API URL 들을 그룹핑하기

여러 앱에 대한 REST API 의 view 가 있는경우, 다음과 같은 프로젝트 전체 API 를 어떻게 만들까요?

##### example 17.9: 전반적인 프로젝트 API 디자인

```
api/flavors/  # GET, POST
api/flavors/:uuid/  # GET, PUT, DELETE
api/users/  # GET
api/users/:uuid/  # GET, PUT, DELETE
```



이전에는, `api`  혹은 `apiv1` 이라는 장고앱에 REST views, serializers 등 커스텀 로직을 두기로 했습니다. 이는 꽤 괜찮은 방식이지만 하나이상의 위치에 특정앱에 대한 로직을 갖게되는 것을 의미합니다. 우리의 현재 접근 방식은 URL 구성에 의존하는 것입니다. 프로젝트 전체의 API를 만들 때 api/views.py 또는 api/viewsets.py 모듈에 REST views를 작성하고 연결합니다.



##### 여러 앱에 대한 API views 를 하나로 통합하기

```python
# core/api_urls.py
"""Called from the project root's urls.py URLConf thus:
			path('api/', include('core.api_urls', namespace='api')),
"""
from django.urls import path
from flavors.api import views as flavor_views
from users.api import views as user_views


urlpatterns = [
       # {% url 'api:flavors' %}
       path(
           route='flavors/',
           view=flavor_views.FlavorCreateReadView.as_view(),
           name='flavors'
),
       # {% url 'api:flavors' flavor.uuid %}
       path(
           route='flavors/<uuid:uuid>/',
           view=flavor_views.FlavorReadUpdateDeleteView.as_view(),
           name='flavors'
),
       # {% url 'api:users' %}
       path(
           route='users/',
           view=user_views.UserCreateReadView.as_view(),
           name='users'
       ),
       # {% url 'api:users' user.uuid %}
       path(
           route='users/<uuid:uuid>/',
           view=user_views.UserReadUpdateDeleteView.as_view(),
           name='users'
), ]
```



### 17.3.6 API 테스트

API 구현에 대한 테스트를 쉽게 만드는 Django 의 테스트 슈트가 있습니다. `curl` 결과를 보는것 보다 훨씬 쉽습니다. 테스트는 "Chapter 24: Testing Stinks and Is a Waste of Money!" 에서 자세히 다룹니다. 간단한 JSON API 에 대한 테스트도 포함합니다.("Section 24.3.1: 각 테스트는 한가지만 테스트 해야합니다." 를 보세요)



### 17.3.7 API 버전

API 의 URL 을 축약된 버전번호를 사용하는 것이 좋습니다. 예를들어, /api/v1/flavors, /api/v1/users 와 같이 하고 이후 API 가 변경됨에 따라 /api/v2/flavors, /api/v2/users 으로 합니다. 우리는 호스트명에 버저닝을 하는것을 더 선호합니다. 예를들어, v1.icescream.com/api/users 와 같이 말입니다. 버전번호가 변경되면 기존 사용자는 자신도 모르게 버전이 변경되서 중단하는 일이 없어 이전 버전을 계속 사용할 수 있습니다.

또한 기존 API 사용자가 화나지 않게 하기위해 업그레이드 이후와 이전 API들 모두 유지하는것은 중요합니다. 사용하지 않는 API 는 몇달동안이나 게속 사용될 수 있습니다.

API 의 새 버전을 구현할 때 기존 API 중단 및 변경을 훨씬 이전에 사용자에게 중단에 대한 경고를 제공하여, 업그레이드 이후 자체 애플리케이션을 중단하지 않도록 해야합니다. 개인적인 경험에 따르면 사용자에게 API 중단에 대한 경고를 보내기 위해 오픈소스에서 API 사용자에 대한 이메일을 요청하는 것도 하나의 이유입니다.

Djano REST Framework 에는 위에 나열된 버저닝 체계와 다른 접근방식을 지원합니다. 그 내용은 이 문서에 있습니다. [django-rest-framework.org/api-guide/versioning/](https://www.django-rest-framework.org/api-guide/versioning/)



### 17.3.8 커스텀 인증 체계 주의하기



## 17.4 DRF 가 방해될 때



### 17.4.1 RPC(Remote Procedure Call) vs REST API





### 17.4.2 복잡한 데이터 문제



### 17.4.3 단순하게! 원자적으로!



## 17.5 외부 API 종료



### 17.5.1 단계1: 유저에게 외부 종료에 대해 알리기



### 17.5.2 단계2: 410 에러를 응답하는 API 로 교체하기



## 17.6 API 속도제한



### 17.6.API 접근을 규제하지 않는것은 위험하다



### 17.6.2 REST 프레임워크는 반드시 속도 제한을 도입해야 한다



### 17.6.3 속도제한은 비즈니스플랜이 될 수 있다.



## 17.7 REST API 광고



### 17.7.1 문서화



### 17.7.2 클라이언트 SDK 제공



## 17.8 추가적으로 읽어보기



## 17.9 API 를 만드는 다른 접근법



### 17.9.1 CBV 접근법 : JsonResponse 를 사용하는 뷰



### 17.9.2 FBV 접근법 : django-jsonview



### 17.9.3 django-tastypie



## 17.10 요약







