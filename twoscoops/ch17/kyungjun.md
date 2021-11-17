# 17장. Django REST Framework로 REST APIs 구현하기

REST(representational state transfer) API는 다양한 환경과 용도에 맞는 데이터를 제공하는 디자인을 정의하고 있다. <br/>
<a href="http://meetup.toast.com/posts/92">REST API</a>
<a href="http://www.django-rest-framework.org/tutorial/quickstart/">DRF 문서</a>
<a href="http://www.django-rest-framework.org/tutorial/1-serializtion/">DRF 문서</a>


## 17.1 기본 REST API 디자인의 핵심
REST API는 HTTP를 기반으로 삼고 있으므로 각 액션에 알맞는 HTTP 메서드를 사용하면 된다.
- 읽기전용 API만 구현한다면 GET 메서드만 구현
- 읽기/쓰기 API를 구현한다면 최소 POST 구현, PUT과 DELETE 또한 고려
- 단순화하기 위해 때로 GET과 POST 만으로도 구현되도록 설계
- API가 PUT 요청을 지원한다면 PATCH 또한 구현하는 것이 좋다.

| 요청의 목적 | HTTP Method | Rough SQL equivalent |
| 새로운 자원 생성 | POST | INSERT |
| 기존의 자원 읽기 | GET | SELECT |
| 기존 자원 업데이트 | PUT | UPDATE |
| 기존 자원 부분 업데이트 | PATCH | UPDATE |
| 기존 삭제 | DELETE | DELETE |
| Returns same HTTP headers as GET, but no body content | HEAD | - |
| Return the supported HTTP methods for the given URL | OPTIONS | - |
| Echo back the request | TRACE | - |

> If you’re implementing a read-only API, you might only need to implement GET methods.
> If you’re implementing a read-write API, you should use the GET, POST, PUT, and DELETE methods.
> Relying on just GET and POST for all actions can be a frustrating pattern for API users.
> By definition, GET, PUT, and DELETE are idempotent. POST and PATCH are not.
> PATCH is often not implemented, but it’s a good idea to implement it if your API supports PUT requests.
> Django Rest Framework is designed around these methods, understand them and DRF itself becomes easier to understand.

<a href="http://en.wikipedia.org/wiki/List_of_HTTP_status_codes/">List_of_HTTP_status_codes</a>

| HTTP 상태 코드 | 성공/실패 | 의미 |
| 200 OK | Success | GET - Return resource, PUT - Provide status message or return resource |
| 201 Created | 성공| POST - Provide status message or return newly created resource |
| 204 No Content | 성공| POST - Provide status message or return newly created resource |
| 304 Not Modified | 성공| POST - Provide status message or return newly created resource |
| 400 Bad Request | 성공| POST - Provide status message or return newly created resource |
| 401 Unauthorized | 성공| POST - Provide status message or return newly created resource |
| 403 Forbidden | 성공| POST - Provide status message or return newly created resource |
| 404 Not Found | 성공| POST - Provide status message or return newly created resource |
| 410 Gone | 성공| POST - Provide status message or return newly created resource |
| 429 Too Many Requests| 성공| POST - Provide status message or return newly created resource |


## 16.2 간단한 JSON API 구현하기
~~~python
# flavors/models.py
import uuid as uuid_lib from django.db import models
from django.urls import reverse
class Flavor(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True) # Used to find the web URL
    uuid = models.UUIDField( # Used by the API to look up the record 
      db_index=True,
      default=uuid_lib.uuid4,
      editable=False)
    scoops_remaining = models.IntegerField(default=0)
    def get_absolute_url(self):
    return reverse('flavors:detail', kwargs={'slug': self.slug})
~~~
> WARNING : Sequential Keys as Public Identifiers
> 위의 예에서는 UUID를 priamry key로 사용할 예정

serializer 클래스
~~~python
# flavors/api/serializers.py
from rest_framework import serializers
from ..models import Flavor
class FlavorSerializer(serializers.ModelSerializer): class Meta:
		model = Flavor
    fields = ['title', 'slug', 'uuid', 'scoops_remaining']
~~~

view
~~~python
# flavors/api/views.py
from rest_framework.generics import ( ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from .models import Flavor
from .serializers import FlavorSerializer
class FlavorListCreateAPIView(ListCreateAPIView): 
    queryset = Flavor.objects.all() 
    permission_classes = (IsAuthenticated, ) 
    serializer_class = FlavorSerializer 
    lookup_field = 'uuid' # Don't use Flavor.id!
class FlavorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView): 
		queryset = Flavor.objects.all()
		permission_classes = (IsAuthenticated, )
		serializer_class = FlavorSerializer
		lookup_field = 'uuid'  # Don't use Flavor.id!
~~~

urls.py
~~~python
# flavors/urls.py
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
       # /flavors/api/:uuid/
       path(
           route='api/<uuid:uuid>/',
           view=views.FlavorRetrieveUpdateDestroyAPIView.as_view(),
           name='flavor_rest_api'
) ]
~~~
| Url | View | Url Name (same) |
| /flavors/api/ | FlavorListCreateAPIView | flavor_rest_api |
| /flavors/api/:uuid/ | FlavorRetrieveUpdateDestroyAPIView | flavor_rest_api |
  
전통적인 REST 스타일의 API 정의
~~~
flavors/api/
flavors/api/:slug/
~~~

> It’s not uncommon to see syntax like what is described in the Wiring in API Views code example. In this particular case, /flavors/api/:uuid/ includes a :uuid value. This represents a variable, but in a manner suited for documentation across frameworks and languages, and you’ll see it used in many third-party REST API descriptions.

# 17.3 REST API 아키텍쳐

## 17.3.1 지속적인 API Module Naming 사용하기
~~~
flavors/
├── api/
│   ├── __init__.py
│   ├── authentication.py
│   ├── parsers.py
│   ├── permissions.py
│   ├── renders.py
│   ├── validators.py
│   ├── views.py
│   ├── viewsets.py
~~~
제발 다음의 것을 준수하자
- 우리는 우리의 API componets를 api/로 불리는 앱안의 패키지 넣는 것을 좋아한다. 이것은 우리의 API components를 일정한 위치에 두도록 만든다. 만약 우리가 우리의 앱의 root에 그것을 넣었으면, we would en up with a huge list of API-specific modules in the general area of the app.
- Viewsets belong in their own module
- We alwyas place routers in urls.py. Either at the app or project level, routes belong in urls.py

## 17.3.2 Code for a Project Should Be Neatly Organized
For projects with a lot of small, interconnecting apps, it can be hard to hunt down where a particular API view lives. In contrast to placing all API code within each relevant app, sometimes it makes more sense to build an app specifically for the API. This is where all the serializers, renderers, and views are placed.
Therefore, the name of the app should reflect its API version (see Section 17.3.7: Version Your API).

For example, we might place all our views, serializers, and other API components in an app titled apiv4.

The downside is the possibility for the API app to become too large and disconnected from the apps that power it. Hence we consider an alternative in the next subsection.

## 17.3.3 Code for an App Should Remain in the App
When it comes down to it, REST API는 단지 view다.. For simpler, smaller projects, REST API views should go into views.py or viewsets.py modules and follow the same guidelines we
endorse when it comes to any other view. The same goes for app- or model-specific serializers and renderers. If we do have app-specific serializers or renderers, the same applies.
For apps with so many REST API view classes that it makes it hard to navigate a single api/views.py or api/viewsets.py module, we can break them up. Specifically, we move our view (or viewset) classes into a api/views/ (or api/viewsets/) package containing Python modules typically named after our models. So you might see:

```python
flavors/
│   ├── api/
│   │		├── __init__.py
│   │   ├── ... other modules here
│		├── views
│   │   ├── __init__.py
│   │   ├── flavoer.py
│   │   ├── ingredient
```
- The downside with this approach is that if there are too many small, interconnecting apps, it can be hard to keep track of the myriad of places API components are placed. Hence we considered another approach in the previous subsection.

## 17.3.4 비즈니스 로직을 API Views로 부터 분리하는 것을 유지하기
니가 취한 구조적 접근에 관계 없이 가능한 API views들로 부터 많은 logic을 분리하는 것이 좋다.기억해라, at the end of the day, API views are just another type of view.

## 17.3.5 API URLs 그룹화하기
니가 만약 다양한 Django app들 내에 REST API views가 있다면, 
~~~
api/flavors/ # GET, POST
api/flavors/:uuid/ # GET, PUT, DELETE
api/users/ # GET, POST
api/users/:uuid/ # GET, PUT, DELETE
~~~

In the past, we placed all API view code into a dedicated Django app called api or apiv1, with custom logic in some of the REST views, serializers, and more. In theory it’s a pretty good approach, but in practice it means we have logic for a particular app in more than just one location.
Our current approach is to lean on URL configuration. When building a project-wide API we write the REST views in the api/views.py or api/viewsets.py modules, wire them into a URLConf called something like core/api_urls.py or core/apiv1_urls.py, and include that from the project root’s urls.py module. This means that we might have something like the following code:

# core/api.py
"""프로젝트 루트 폴더에 위치한 urls.py의 URLConf에서 호출됨, 따라서:
        url(r"^api/", include("core.api", namespace="api")),
"""
from django.conf.urls import url

from flavors import views as flavor_views
from users import views as user_views

```python
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
       ), 
]
```

## 17.3.6 API 테스트하기 
22장에서...

## 17.3.7 API 버저닝하기

It’s a good practice to abbreviate the urls of your API with the version number e.g. /api/v1/flavors or /api/v1/users and then as the API changes, /api/v2/flavors or /api/v2/users. We prefer this method or the host name style of versioning v1.icecreamlandia.com/api/users. When the version number changes, existing cus- tomers can continue to use the previous version without unknowingly breaking their calls to the API.
Also, in order to avoid angering API consumers, it’s critical to maintain both the existing API and the predecessor API during and after upgrades. It’s not uncommon for the depre- cated API to remain in use for several months.
When we implement a new version of the API, we provide customers/users with a dep- recation warning well in advance of breaking API changes so they can perform necessary upgrades and not break their own applications. From personal experience, the ability to send a deprecation warning to end users is an excellent reason to request email addresses from users of even free and open source API services.
Django REST Framework has built-in mechanisms for supporting the preferred scheme we list above as well as other approaches. Documentation for this exists at
https://www.django-rest-framework.org/api-guide/versioning/
  
  
<a href="http://channy.creation.net/articles/microservices-by-james_lewes-martin_fowler#.WbgZINNJbUo">
서비스 지향 아키텍처(SOA, service-oriented architecture)
웹 애플리케이션은 독립적이고 분리된 컴포넌트로 구성된다.각 장고 앱이 독립된 장고 프로젝트로 나뉠 수 있음.

## 17.3.8 Customized 인증 스키마 조심하기

- If we’re creating a new authentication scheme, we keep it simple and well tested.
- Outside of the code, we document why existing standard authentication schemes are
insufficient. See the tipbox below.
- Also outside of the code, we document in depth how our authentication scheme is
designed to work. See the tipbox below.
- Unless we are writing a non-cookie based scheme, we don’t disable CSRF.

# TIP: Documentation Is Critical for Customized Authentication
Writing out the why and how of a customized authentication scheme is a critical part of the process. Don’t skip it! Here’s why:
> Helps us validate our reasoning for coming up with something new. If we can’t describe the problem in writing, then we don’t fully understand it.
> Documentation forces us to architect the solution before we code it.
> After the system is in place, later the documentation allows us (or others) to
understand why we made particular design decisions.

# 17.4 When DRF Gets in the Way
Django Rest Framework is a powerful tool that comes with a lot of abstractions. Trying to work through these abstractions can prove to be extremely frustrating. Let’s take a look on overcoming them.

## 17.4.1 Remote Procedure Calls vs REST APIs
> https://stackoverflow.com/questions/26488915/implementing-rpc-in-restful-api-using-drf/26502402
The resource model used by REST frameworks to expose data is very powerful, but it doesn’t cover every case. Specifically, resources don’t always match the reality of application design. For example, it is easy to represent syrup and a sundae as two resources, but what about the action of pouring syrup? Using this analogy, 
we change the state of the sundae and decrease the syrup inventory by one. 
While we could have the API user change things individually, that can generate issues with database integrity. 
Therefore in some cases it can be a good idea to present a method like sundae.pour_syrup(syrup) to the client as part of the RESTful API.
In computer science terms, sundae.pour_syrup(syrup) could be classified as a Remote Procedure Call or RPC.
References:
> https://en.wikipedia.org/wiki/Remote_Procedure_Call
> https://en.wikipedia.org/wiki/Resource-oriented_architecture
Fortunately, RPC calls are easy to implement with Django Rest Framework. All we have to do is ignore the abstraction tools of DRF and rely instead on its base APIView:

```python
# sundaes/api/views.py
from django.shortcuts import get_object_or_404 from rest_framework.response import Response
from rest_framework.views import APIView from ..models import Sundae, Syrup
from .serializers import SundaeSerializer, SyrupSerializer 

class PourSyrupOnSundaeView(APIView):
       """View dedicated to adding syrup to sundaes"""
    def post(self, request, *args, **kwargs):
        # Process pouring of syrup here,
        # Limit each type of syrup to just one pour 
        # Max pours is 3 per sundae 
        # (아이스크림선디(기다란 유리잔에 아이스크림을 넣고 시럽, 견과류, 과일 조각 등을 얹은)
        sundae = get_object_or_404(Sundae, uuid=request.data['uuid']) 
        try:
        		sundae.add_syrup(request.data['syrup']) 
        except Sundae.TooManySyrups:
        		msg = "Sundae already maxed out for syrups"
        		return Response({'message': msg}, status_code=400) 
        except Syrup.DoesNotExist
            msg = "{} does not exist".format(request.data['syrup'])
            return Response({'message': msg}, status_code=404) 
				return Response(SundaeSerializer(sundae).data)
		def get(self, request, *args, **kwargs)
				# Get list of syrups already poured onto the sundae 
      	sundae = get_object_or_404(Sundae,uuid=request.data['uuid'])
				syrups = [SyrupSerializer(x).data for x in sundae.syrup_set.all()] 
        return Response(syrups)
```
And our API design would look like this now:
```
/sundae/  # GET, POST
/sundae/:uuid/  # PUT, DELETE
/sundae/:uuid/syrup/  # GET, POST
/syrup/  # GET, POST
/syrup/:uuid/  # PUT, DELETE

```
## 17.4.2 Problems With Complex Data
Okay, we’ll admit it, we make this mistake with DRF about once a month. Let’s sum up what happens in very simple terms with the following API design:
```
/api/cones/  # GET, POST
/api/cones/:uuid/  # PUT, DELETE
/api/scoops/  # GET, POST
/api/scoops/:uuid/  # PUT, DELETE
```
- We have a model (Scoop) that we want represented within another (Cone)
- We can easily write a GET of the Cone that includes a list of its Scoops
- On the other hand, writing a POST or PUT of Cones that also adds or updates
its Scoops at the same time can be challenging, especially if it requires any kind of
validation or post processing
- Frustration sets in and we leave to get some real-world ice cream

While there are nicely complex solutions for nested data, we’ve found a better solution. And that is to simplify things just a bit. Example:
> Keep the GET representation of the Cone that includes its Scoops
> Remove any capability of the POST or PUT for the Cone model to modify Scoops
for that cone.
> Create GET/POST/PUT API views for Scoops that belong to a Cone.

Our end API will now look like this:
```
/api/cones/  # GET, POST
/api/cones/:uuid/  # PUT, DELETE
/api/cones/:uuid/scoops/  # GET, POST
/api/cones/:uuid/scoops/:uuid/  # PUT, DELETE
/api/scoops/  # GET, POST
/api/scoops/:uuid/  # PUT, DELETE
```
https://stripe.com/docs/api

## 17.4.3 Simplify! Go Atomic!


# 17.5 외부 API shut down


## 17.5.1 User에게 알린다.

## 17.5.2 API를 410 Error Viwe로 교체한다.

# 17.6 횟수 제한 API

## 17.6.1 User에게 알린다.

## 17.6.2 REST Frameworks Must Come With Rate Limiting
> 속도면에서는 nginx, apache의 횟수 제한을 사용하는 것이 좋지만, 해당 기능을 파이썬 코드에서 제거한다.

## 17.6.3 Rate Limiting Can Be a Business Plan

# 17.7 너의 REST API 광고하기

## 17.7.1 문서화

## 17.7.2 Clien SDKs 제공하기
> https://www.youtube.com/watch?v=kG-fLp9BTRo

API를 널리 사용하는 데 도움이 될 수 있는 것은 다양한 프로그래밍 언어를 위한 소프트웨어 개발 키트(SDK)를 제공하는 것입니다. 더 많은 프로그래밍 언어가 더 잘 다루어졌다. 우리는 파이썬, 자바스크립트, 루비, PHP, Go, 자바를 포함한 필수 언어들을 찾았다.
경험상, 적어도 하나의 라이브러리를 직접 작성하고 데모 프로젝트를 만드는 것이 좋습니다. 그 이유는 그것이 우리의 API를 홍보할 뿐만 아니라 우리의 API를 소비자와 같은 유리한 관점에서 경험하도록 강요하기 때문입니다.

# 17.8
> (링크 추가 필요)


# 17.9 Other Approaches for Crafting APIs
For the reasons explained at the beginning of this chapter, we recommend Django Rest Frame- work. However, should you choose not to use DRF, consider the following approaches
	
	
# 17.10 Summary
In this chapter we covered:
- Why you should use Django Rest Framework
- Basic REST API concepts and how they relate to Django Rest Framework
- Security considerations
- Grouping strategies
- Simplification strategies
