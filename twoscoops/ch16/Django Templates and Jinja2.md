# Django Templates and Jinja2

장고 1.8에서는 여러 개의 템플릿 엔진이 지원되었다. 현재 장고 템플릿 시스템에 사용할 수 있는 내장 백엔드는 DTL(Dango Template Language)과 Jinja2뿐입니다.

##  What’s the Syntactical Difference?

 DTL과 Jinja2는 매우 유사하다. 사실 Jinja2는 DTL에서 영감을 받았습니다. 가장 중요한 구문 차이는 다음과 같습니다.

| Subject             | DTL                      | Jinja2                       |
| ------------------- | ------------------------ | ---------------------------- |
| Method Calls        | {{user.get_favorites}}   | {{user.get_favorites()}}     |
| Filter Arguments    | {{ toppings join:','}}   | {{toppings\|join(',')}}      |
| Loop Empty Argument | {%empty%}                | {% else %}                   |
| Loop Variable       | {{ forloop}}             | {{loop}}                     |
| Cycle               | {% cycle 'odd' 'even' %} | {{ loop.cycle('odd','even)}} |



## 16.2 Should I Switch?

우선 장고를 사용할 때 DTL과 진자2 중 선택할 필요가 없습니다. 세팅 할 수 있어요.템플릿 일부 템플릿 디렉토리에는 DTL을 사용하고 다른 템플릿에는 Jinja2를 사용합니다. 코드베이스에 템플릿이 많으면 기존 템플릿을 그대로 유지하고 필요한 곳에 Jinja2의 이점을 활용할 수 있습니다. 이를 통해 양쪽의 장점을 모두 누릴 수 있습니다. 방대한 타사 패키지의 Django 생태계와 DTL에 대한 대안 기능을 이용할 수 있습니다.

즉, 여러 템플릿 언어를 조화롭게 사용할 수 있습니다.

예를 들어, 대부분의 사이트는 DTL을 사용하여 렌더링할 수 있으며, 더 큰 페이지는 Jinja2로 콘텐츠를 렌더링할 수 있다. 이러한 동작의 좋은 예는 djangopackages.org/grids이다. 크기와 복잡성으로 인해 향후 이러한 페이지는 리팩터링될 수 있습니다.

---



Chapter 16: Django Templates and Jinja2

---



(프로젝트가 단일 페이지 앱(SPA)이 되지 않는 한) DTL 대신 Jinja2에 의해 구동된다.

### 16.2.1 Advantages of DTL

다음은 장고 템플리트 언어를 사용하는 이유입니다.

- batteries-included(표준 라이브러리만으로 모든 작업을 수행 가능) 장고 문서에 명확하게 기록된 모든 기능이 포함되어 있습니다. DTL에 대한 공식 장고 문서는 매우 광범위하고 따르기 쉽다. 장고 문서의 템플릿 코드 예제는 DTL을 사용합니다.
- 장고 패키지는 대부분 DTL을 사용한다. 그것들을 진자2로 변환하는 것은 추가 작업입니다.
- 대규모 코드베이스를 DTL에서 Jinja2로 변환하는 것은 많은 작업입니다.



### 16.2.2 Advantages of Jinja2

- 장고와 별개로 사용할 수 있습니다.
- 진자2의 구문이 파이썬의 구문에 가까울수록 많은 사람들이 더 직관적이라고 생각한다.
- 일반적으로 Jinja2는 보다 명확합니다. 예를 들어 템플릿의 함수 호출은 괄호를 사용합니다.
- Jinja2는 로직에 대한 임의 제한이 적습니다. 예를 들어, 필터를 사용할 때 Jinja2는 인수를 무제한으로 전달할 수 있습니다.  DTL을 사용하는 경우 인자 1개.
- 온라인 벤치마크와 자체 실험에 따르면 진자2가 더 빠르다. 즉, 템플리트는 항상 데이터베이스 최적화보다 성능 병목 현상이 훨씬 작습니다. 26장 "병목 현상 찾기 및 감소"를 참조하십시오.

### 16.2.3  Which One Wins?

상황에 따라 다릅니다.

- 새로운 장고넛은 항상 DTL을 고수해야 한다.

- 코드베이스가 큰 기존 프로젝트들은 성능 개선이 필요한 몇 페이지를 제외하고 DTL을 고수하기를 원할 것이다.

- 경험 많은 장고넛은 둘 다 시도해보고, DTL과 진자의 장점을 따져보고,
  그들 스스로 결정을 내리다.



#### 팁: 기본 템플릿 언어 선택

여러 템플릿 언어를 프로젝트에 걸쳐 혼합할 수 있지만 그렇게 하면 프로젝트의 정신적 과부하가 크게 가중될 위험이 있습니다. 이 위험을 완화하려면 단일 기본 템플리트 언어를 선택하십시오.



### 16.3   Considerations When Using Jinja With Django

다음은 진자 템플릿을 장고와 함께 사용할 때 주의해야 할 몇 가지 사항입니다.

### 16.3.1  CSRF and Jinja

Jinja는 DTL과 다르게 Django의 CSRF 메커니즘에 접근합니다. CSRF를 Jinja2 템플릿에 통합하려면 양식을 렌더링할 때 필요한 HTML을 포함해야 합니다. :

#### Example 16.1:  Using  Django’s  CSRF  Token  with  Jinja2  Templates

```bash
<div style="display:none">
	<input type="hidden" name="csrfmiddlewaretoken" value="{{
→	csrf_token }}">

</div>
```



### 16.3.2 Using Template Tags in Jinja Templates

현재 진자에서는 장고 스타일의 템플릿 태그를 사용할 수 없습니다. 특정 템플릿 태그의 기능이 필요한 경우 다음 기술 중 하나를 사용하여 변환합니다.

- 기능을 함수로 변환합니다.
- 진자 확장을 만듭니다.  jinja.palletsprojects.com/en/latest/ extensions/#module-jinja2.ext



### 16.3.3 Using Django-Style Template Filters in Jinja Templates

DTL에 익숙해진 한 가지는 Django의 기본 템플릿 필터입니다. 다행히 Django 필터는 기능일 뿐이므로(섹션 15.1: 필터는 기능 참조), 템플릿 필터를 포함하는 사용자 지정 Jinja2 환경을 쉽게 지정할 수 있습니다.



#### Example 16.2:  Injecting  Django  Filters  Into  Jinja2  Templates

``` python
# core/jinja2.py
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import defaultfilters
from django.urls import reverse

from jinja2 import Environment

 
def environment(**options):
    env = Environment(**options) env.globals.update({
    'static': staticfiles_storage.url, 'url': reverse,
    'dj': defaultfilters })
return env
```



다음은 Jango 템플릿 필터를 Jinja2 템플릿의 함수로 사용하는 예입니다.



#### Example 16.3:  Using  Django  Filters  in  a  Jinja2  Template

```bash
<table><tbody>
{% for purchase in purchase_list %}
	<tr>
		<a href="{{ url('purchase:detail', pk=purchase.pk) }}"> {{ 						purchase.title }}
		</a> 
	</tr>
	<tr>{{ dj.date(purchase.created, 'SHORT_DATE_FORMAT') }}</tr>
    <tr>{{ dj.floatformat(purchase.amount, 2) }}</tr>
{% endfor %} 
</tbody></table>
```



덜 전역적인 접근 방식을 원할 경우 섹션 10.4.3: 잘못된 양식으로 뷰에 대한 사용자 정의 수행에서 살펴본 기술을 사용할 수 있습니다. 여기서는 뷰의 속성으로 Django 템플릿 필터를 부착하기 위한 혼합물을 작성합니다.

#### Example 16.4: Django Filter View Mixin for Jinja2

```bash
# core/mixins.py
from django.template import defaultfilters 

class DjFilterMixin:
	dj = defaultfilters
```

뷰가 core.mixins에서 상속되는 경우.DjFilterMixinclass의 Jinja2 템플릿에서는 다음을 수행할 수 있습니다.



#### Example 16.5:  Using  View-Injected  Django  Filters  in  Jinja2

```bash
<table><tbody>
{% for purchase in purchase_list %}
	<tr>
		<a href="{{ url('purchase:detail', pk=purchase.pk) }}"> 
			{{ purchase.title }}
		</a> 
	</tr>
	<!-- Call the django.template.defaultfilters functions from the 
→	view -->
	<tr>{{ view.dj.date(purchase.created, 'SHORT_DATE_FORMAT') 
→	}}</tr>
	<tr>{{ view.dj.floatformat(purchase.amount, 2) }}</tr>
{% endfor %}
</tbody></table>
```



#### TIP: Avoid Using Context Processors With Jinja2

장고 문서에서는 컨텍스트 프로세서를 Jinja2와 함께 사용하지 말 것을 권장합니다. docs.djangoproject.com/en/3.2/topics/ 템플릿/#django.backends.jinja2의 경고 상자를 참조하십시오.Jinja2. 대신 그들이 요구하는 것은 필요에 따라 호출할 수 있는 함수를 템플릿에 전달하는 것이다. 이 작업은 뷰 단위로 수행하거나 이 하위 섹션에 설명된 대로 호출 가능 함수를 주입하여 수행할 수 있습니다.



### 16.3.4 Jinja2 환경 객체는 정적으로 간주되어야 한다.

예 15.1에서는 진자2의 핵심 구성 요소의 사용을 시연한다.
진자2 환경 클래스. 
이 개체는 Jinja2가 구성, 필터, 테스트, 전역 등을 공유하는 곳입니다. 프로젝트의 첫 번째 템플릿이 로드되면 Jinja2는 이 클래스를 정적 개체로 인스턴스화합니다.



#### Example 16.6: 진자2 환경의 정적 특성

```py
# core/jinja2.py
from jinja2 import Environment
import random
def environment(**options): 
	env = Environment(**options) 
	env.globals.update({
	# Runs only on the first template load! The three displays
→		below
	#  will all present the same number.
	#  {{ random_once }} {{ random_once }} {{ random_once }} 'random_once': 	random.randint(1, 5)
	# Can be called repeated as a function in templates. Each
→	call
	#  returns a random number:
	#  {{ random() }} {{ random() }} {{ random() }} 
	'random': lambda: random.randint(1, 5),
	})
	return env

```



#### 경고: 진자를 바꾸지 마십시오.인스턴스화 후 환경

 Jinja.Environment 객체를 수정하는것은 위험하다. Jinja2 API 설명서에 따르면, "첫 번째 템플릿이 로드된 후 환경을 수정하면 놀라운 효과와 정의되지 않은 동작이 발생합니다."

Reference:   jinja.palletsprojects.com/en/3.0.x/api/#jinja2. Environment



### 16.4 Resources

- ➤     Django’s   documentation   on   using   Jinja2:   docs.djangoproject.com/en/3.2/ topics/templates/#django.template.backends.jinja2.Jinja2
- jinja.pocoo.org



### 16.5       Summary

이 챕터에서는 DTL과 Jinja2의 유사점과 차이점을 다루었습니다.  또한 프로젝트에서 Jinja2를 사용할 경우 발생하는 영향과 해결 방법을 살펴보았습니다.

다음 장부터는 템플릿을 뒤로하고 서버 측과 클라이언트 측 모두에서 REST의 세계를 살펴보겠습니다.

