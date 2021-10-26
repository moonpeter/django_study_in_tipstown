#### 14장 Tamplates:  Best Practices

>Django의 초기 디자인 결정 중 하나는 템플릿 언어의 기능을 제한하는 것이었습니다.
>이것은 Django 템플릿으로 수행할 수 있는 작업을 크게 제한합니다.
>
>생각해 보세요.
>Django 템플릿의 한계로 인해 프로젝트의 가장 중요하고 복잡하며 세부적인 부분을 
>템플릿 파일이 아닌  .py 파일에 넣습니다.
>
>Python은 지구상에서 가장 명확하고 간결하며 우아한 프로그래밍 언어 중 하나인데 
>왜 우리가 다른 방식을 원할까요?



##### TIP: Using Jinja2 With Django

> 1.8 릴리스 이후 Django는 기본적으로 Jinja2를 지원했습니다.
> 또한 다른 템플릿 언어를 포함하기 위한 인터페이스를 제공합니다.
>
> 16장: Django 템플릿과 Jinja2에서 이 주제를 다룹니다.



##### 14.1 Keep Templates Mostly in `templates/` 

> 우리 프로젝트에서는 대부분의 템플릿을 기본 'templates/' 디렉토리에 보관합니다.
> 다음과 같이 각 앱에 해당하는 하위 디렉토리를 'templates/'에 넣습니다.

```text
예제 14.1: 템플릿 디렉토리를 구성하는 방법

templates/
├── base.html
├── ... (other sitewide templates in here)
├── freezers/
│   ├── ("freezers" app templates in here)

```

> 그러나 일부 자습서에서는 각 앱의 하위 디렉터리에 템플릿을 넣는 것을 권장합니다.
> 다음과 같이 추가 중첩은 처리하기 힘든 문제입니다.



```
예제 14.2: 지나치게 복잡한 템플릿 디렉토리 구조
freezers/
├── templates/
│   ├── freezers/
│   │   ├── ... ("freezers" app templates in here)
templates/
├── base.html
├── ... (other sitewide templates in here)
```



> 즉, 일부 사람들은 두 번째 방법을 좋아하고 괜찮습니다.
>
> 이 모든 것에 대한 예외는 플러그인 가능한 패키지로 설치된 Django 앱으로 작업할 때입니다.
> Django 패키지는 일반적으로 자체 인앱 'templates/' 디렉토리를 포함합니다. (예제 보여줄것??)
>
> 그런 다음 디자인과 스타일을 추가하기 위해 프로젝트의 기본 'templates/' 디렉터리에서 
> 해당 템플릿을 재정의합니다. 
> 섹션 23.9: 자신만의 Django 패키지 릴리스에서 이에 대해 살펴보겠습니다.



##### 14.2 템플릿 아키텍처 패턴

> 우리는 우리의 목적을 위해 단순한 `2-Tier` 또는 `3-Tier` 템플릿 아키텍처가 이상적이라는 
> 것을 발견했습니다.
>
> 계층의 차이는 `앱의 콘텐츠가 표시되기 전에 발생해야 하는 템플릿 확장 수준의 수`입니다.
> 아래 예를 참조하십시오.



###### 14.2.1 2-Tier 템플릿 아키텍처의 예

> 2-Tier 템플릿 아키텍처를 사용하면 모든 템플릿이 단일 루트 `base.html` 파일에서 상속됩니다.

```
예제 14.3: 2-Tier 템플릿 아키텍처
templates/
├── base.html
├── dashboard.html # extends base.html
├── profiles/
│ ├── profile_detail.html # extends base.html
│ ├── profile_form.html # extends base.html
```

> 이는 앱 간에 일관된 전체 레이아웃을 가진 사이트에 가장 적합합니다.



###### 14.2.2 3-Tier 템플릿 아키텍처 예제

> 3-Tier 템플릿 아키텍처:
> ➤  각 앱에는 base_<app_name>.html 템플릿이 있습니다. 
>       앱 수준 기본 템플릿은 공통 상위 base.html 템플릿을 공유합니다.
>
> ➤ 앱 내의 템플릿은 공통 상위 base_<app_name>.html 템플릿을 공유합니다.
>
> ➤ base.html과 동일한 수준에 있는 모든 템플릿은 base.html을 상속합니다.

```
예제 14.4: 3-Tier 템플릿 설계자
templates/
├── base.html
├── dashboard.html # extends base.html
├── profiles/
│ ├── base_profiles.html # extends base.html
│ ├── profile_detail.html # extends base_profiles.html
│ ├── profile_form.html # extends base_profiles.html
```

>3계층 아키텍처는 각 섹션에 고유한 레이아웃이 필요한 웹사이트에 가장 적합합니다.
>
>예를 들어 뉴스 사이트에는 지역 뉴스 섹션, 분류된 광고 섹션 및 이벤트 섹션이 있을 수 있습니다.
>
>이러한 각 섹션에는 고유한 사용자 지정 레이아웃이 필요합니다.
>
>이것은 기능을 그룹화하는 사이트의 특정 섹션에 대해 HTML이 다르게 보이거나 
>동작하도록 할 때 매우 유용합니다.



###### 14.2.3 `Flat`이 `Nested`보다 낫다. (단조로움이 중첩된 것보다 낫다.)

> 복잡한 템플릿 계층 구조로 인해 HTML 페이지를 디버그, 수정 및 확장하고 CSS 스타일을 연결하는
> 것이 매우 어렵습니다.
>
> 템플릿 블록 레이아웃이 불필요하게 중첩되면 상자의 너비를 변경하기 위해 파일 뒤에서 파일을 
> 파헤치게 됩니다.
>
> 템플릿 블록을 가능한 한 얕은 상속 구조로 지정하면 템플릿을 보다 쉽게 작업하고 유지 관리할 수 있습니다.디자이너와 함께 일하면 디자이너가 고마워할 것입니다.
>
> 즉, 지나치게 복잡한 템플릿 블록 계층과 코드 재사용을 위해 블록을 현명하게 사용하는 템플릿 사이에는 
> 차이가 있습니다.
>
> 별도의 템플릿에 같거나 매우 유사한 코드의 여러 줄짜리 큰 청크가 있는 경우 해당 코드를 재사용 가능한 
> 블록으로 리팩토링하면 코드를 보다 쉽게 유지 관리할 수 있습니다.
>
> Zen of Python에는 "Flat is better than nested"라는 격언이 포함되어 있습니다.
>
> 중첩의 각 수준은 정신적 오버헤드를 추가합니다. (정신적인 처리 시간)
> Django 템플릿을 설계할 때 이를 염두에 두십시오.



###### TIP: The Zen of Python

> 명령줄에서 다음을 수행합니다.
> ```python -c 'import this```'
>
> 여러분이 보게 될 것은 Python 프로그래밍 언어의 설계를 위한 웅변적으로 표현된 일련의 지침 원칙인 
> Zen of Python입니다.
>
> Beautiful is better than ugly. 아름다움이 추한 것보다 낫다.
> Explicit is better than implicit. 명확함이 함축된 것보다 낫다.
> Simple is better than complex. 단순함이 복잡한 것보다 낫다.
> Complex is better than complicated. 복잡함이 난해한 것보다 낫다.
> Flat is better than nested. 단조로움이 중접된 것보다 낫다.
> Sparse is better than dense. 여유로움이 밀집된 것보다 낫다.
> Readability counts. 가독성은 중요하다.
>
> Special cases aren't special enough to break the rules. 규칙을 깨야할 정도로 특별한 경우란 없다. Although practicality beats purity. 비록 실용성이 이상을 능가한다 하더라도.
>
> Errors should never pass silently. 오류는 결코 조용히 지나가지 않는다. Unless explicitly silenced. 알고도 침묵하지 않는 한.
>
> In the face of ambiguity, refuse the temptation to guess. 
> 모호함을 마주하고 추측하려는 유혹을 거절하라. 
> There should be one-- and preferably only one --obvious way to do it. 
> 문제를 해결할 하나의 - 바람직하고 유일한 - 명백한 방법이 있을 것이다. 
> Although that way may not be obvious at first unless you're Dutch. 
> 비록 당신이 우둔해서 처음에는 명백해 보이지 않을 수도 있겠지만.
>
> Now is better than never. 
> 지금 하는 것이 전혀 안하는 것보다 낫다. 
> Although never is often better than *right* now.
> 비록 하지않는 것이 지금 하는 것보다 나을 때도 있지만.
>
> If the implementation is hard to explain, it's a bad idea. 
> 설명하기 어려운 구현이라면 좋은 아이디어가 아니다. 
>
> If the implementation is easy to explain, it may be a good idea. 
> 쉽게 설명할 수 있는 구현이라면 좋은 아이디어일 수 있다. 
>
> Namespaces are one honking great idea -- let's do more of those! 
> 네임스페이스는 정말 대단한 아이디어다. -- 자주 사용하자!



##### 14.3 템플릿에서 처리 제한

> 템플릿에서 수행하려는 처리가 적을수록 좋습니다.
> 이는 템플릿 계층에서 수행되는 쿼리 및 반복과 관련하여 특히 문제입니다.
>
> 템플릿의 쿼리 세트를 반복할 때마다 다음 질문을 스스로에게 물어보세요.
>
> 1. 쿼리 세트의 크기는 얼마입니까?
>    템플릿에서 거대한 쿼리 세트를 반복하는 것은 거의 항상 나쁜 생각입니다.
> 2. 검색되는 개체의 크기는 얼마나 됩니까?
>    이 템플릿에 모든 필드가 필요합니까?
> 3. 루프의 각 반복 동안 얼마나 많은 처리가 발생합니까?
>
>
> 머리 속에서 경고음이 울리면 템플릿 코드를 다시 작성하는 더 좋은 방법이 있을 수 있습니다.



###### 경고: 그냥 캐시하면 안 되나요?

> 때로는 템플릿의 비효율성을 캐시에 저장할 수 있습니다.
> 괜찮지만 캐시하기 전에 먼저 문제의 근본 원인을 공격해야 합니다.
> 템플릿 코드를 정신적으로 추적하고, 몇 가지 빠른 런타임 분석을 수행하고,
> 리팩토링하면 많은 작업을 절약할 수 있습니다.



> 이제 더 효율적으로 재작성할 수 있는 템플릿 코드의 몇 가지 예를 살펴보겠습니다.
>
> 잠시 동안 불신을 멈추고 Two Scoops 뒤에 있는 열성적인 듀오가 슈퍼볼 기간 동안 30초 광고를 
> 진행했다고 가정해 보십시오. (지난해 2020년 **슈퍼볼 광고** 단가는 30초 기준 560만 달러(한화 66억 원))
>
> “최초로 요청하는 100만 개발자를 위한 무료 아이스크림 파인트! 상점에서 교환 가능한 바우처를 받으려면 양식을 작성하기만 하면 됩니다!”
>
> 당연히 무료 파인트 바우처를 요청한 모든 사람의 이름과 이메일 주소를 추적하는 "바우처" 앱이 있습니다.
>
> 이 앱의 모델은 다음과 같습니다.



###### 예제 14.5: 바우처 모델 예제

```python
# vouchers/models.py
from django.db import models
from .managers import VoucherManager

class Voucher(models.Model):
	"""Vouchers for free pints of ice cream."""
	name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    birth_date = models.DateField(blank=True)
    sent = models.DateTimeField(null=True, default=None)
    redeemed = models.DateTimeField(null=True, default=None)
    objects = VoucherManager()

```



> 이 모델은 다음 예에서 사용하여 피해야 하는 몇 가지 "문제"를 설명합니다.



##### 14.3.1 Gotcha 1: 템플릿의 집계

> 우리는 생년월일 정보를 가지고 있기 때문에 바우처 요청 및 사용의 연령대별로 대략적인 분석을 표시하는
> 것이 흥미로울 것입니다.
>
> 이것을 구현하는 아주 나쁜 방법은 템플릿 수준에서 모든 처리를 수행하는 것입니다.
> 이 예의 맥락에서 더 구체적으로 말하자면:
>
> ➤ 연령 범위 계산을 유지하기 위해 JavaScript 변수를 사용하여 템플릿의 JavaScript 섹션에 있는 
> 	 전체 바우처 목록을 반복하지 마십시오.
>
> ➤ 바우처 수를 합산하기 위해 템플릿 추가 필터를 사용하지 마십시오.
>
> 이러한 구현은 템플릿에서 Django의 `논리 제한을 해결하는 방법`이지만 페이지 속도를 크게 저하시킵니다.
> 더 좋은 방법은 이 처리를 템플릿에서 Python 코드로 옮기는 것입니다.
>
> 템플릿을 사용하여 이미 처리된 데이터만 표시하는 최소한의 접근 방식을 고수하면 템플릿은 다음과 
> 같습니다.

```html
<!-- 예제 14.6: 템플릿을 사용하여 사전 처리된 데이터를 표시합니다. -->

{# templates/vouchers/ages.html #}
{% extends "base.html" %}
{% block content %}
<table>
    <thead>
        <tr>
            <th>Age Bracket</th>
            <th>Number of Vouchers Issued</th>
        </tr>
    </thead>
    <tbody>
        {% for age_bracket in age_brackets %}
        <tr>
            <td>{{ age_bracket.title }}</td>
            <td>{{ age_bracket.count }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock content %}

```



> 이 예제에서는 Django ORM의 집계 방법과 `37장: 부록 A: 이 책에 언급된 패키지`에 설명된 편리한 
> `dateutil` 라이브러리를 사용하여 모델 관리자로 처리를 수행할 수 있습니다.



```python
# 예제 14.7: 템플릿 표시 전 데이터 사전 처리
# vouchers/managers.py
from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class VoucherManager(models.Manager):
    def age_breakdown(self):
        """Returns a dict of age brackets/counts."""
        age_brackets = []
        delta = timezone.now() - relativedelta(years=18)
        
        count = self.model.objects.filter(
            birth_date__gt=delta
        ).count()
        
        age_brackets.append(
        	{'title': '0-17', 'count': count}
        )
        
		count = self.model.objects.s.filter(
            birth_date__lte=delta
        ).count()
        age_brackets.append(
        	{'title': '18+', 'count': count}
        )
        
        return age_brackets
		
```



> 이 메서드는 뷰에서 호출되고 결과는 컨텍스트 변수로 템플릿에 전달됩니다.



##### 14.3.2 Gotcha 2: 템플릿에서 조건부 필터링

> 가족 모임에 초대할 수 있도록 무료 파인트 상품권을 요청한 모든 Greenfelds와 Roys의 목록을
> 표시하려고 한다고 가정합니다.
>
> 이름 필드에서 레코드를 필터링하려고 합니다.
> 이것을 구현하는 아주 `나쁜 방법`은 템플릿 수준에서 거대한 루프와 if 문을 사용하는 것입니다.

```django
<!-- # 예제 14.8: 데이터 필터링의 비참한 방법 -->

<h2>Greenfelds Who Want Ice Cream</h2>
<ul>
    {% for voucher in voucher_list %}
        {# Don't do this: conditional filtering in templates #}
        {% if 'greenfeld' in voucher.name.lower %}
        	<li>{{ voucher.name }}</li>
        {% endif %}
    {% endfor %}
</ul>
<h2>Roys Who Want Ice Cream</h2>
<ul>
    {% for voucher in voucher_list %}
        {# Don't do this: conditional filtering in templates #}
        {% if 'roy' in voucher.name.lower %}
        	<li>{{ voucher.name }}</li>
        {% endif %}
    {% endfor %}
</ul>
```



> 이 나쁜 스니펫에서 우리는 다양한 "if" 조건을 반복하고 확인하고 있습니다.
> 이는 템플릿에서 잠재적으로 거대한 레코드 목록을 필터링하는 것입니다.
> 이는 이러한 종류의 작업을 위해 설계되지 않았으며 성능 병목 현상을 일으킬 수 있습니다.
>
> 반면에 PostgreSQL, MySQL과 같은 데이터베이스는 레코드 필터링에 탁월하므로 데이터베이스 계층에서
> 수행해야 합니다.
>
> Django ORM은 다음 예제에서 볼 수 있듯이 이를 도와줄 수 있습니다.



```python
# 예제 14.9: ORM/데이터베이스를 사용하여 데이터 필터링

# vouchers/views.py
from django.views.generic import TemplateView
from .models import Voucher

class GreenfeldRoyView(TemplateView):
	
    template_name = 'vouchers/views_conditional.html'
    
	def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['greenfelds'] = Voucher.objects.filter(
            name__icontains='greenfeld'
        )
        
        context['roys'] = Voucher.objects.filter(
            name__icontains='roy'
        )
        
        return context

```



```html
<!-- 예제 14.10: 단순화된 빠른 템플릿 표시 -->

<h2>Greenfelds Who Want Ice Cream</h2>
<ul>
	{% for voucher in greenfelds %}
		<li>{{ voucher.name }}</li>
	{% endfor %}
</ul>
<h2>Roys Who Want Ice Cream</h2>
<ul>
	{% for voucher in roys %}
		<li>{{ voucher.name }}</li>
	{% endfor %}
</ul>

```



> 필터링을 보기로 이동하여 이 템플릿의 속도를 높이는 것은 쉽습니다.
> 이 변경으로 이제 템플릿을 사용하여 이미 필터링된 데이터를 표시합니다.
> 위의 템플릿은 이제 우리가 선호하는 미니멀리스트 접근 방식을 따릅니다.



##### 14.3.3 Gotcha 3: 템플릿의 복잡한 암시적 쿼리

> Django 템플릿에서 허용되는 논리의 제한에도 불구하고 보기에서 불필요한 쿼리를 반복적으로 
> 호출하는 것은 너무 쉽습니다.
>
> 예를 들어, 우리 사이트의 사용자와 그들의 모든 취향을 다음과 같이 나열한다면:

```html
{# Example 14.11: Template Code Generating Extra Queries #}

{# list generated via User.objects.all() #}
<h1>Ice Cream Fans and their favorite flavors.</h1>
<ul>
	{% for user in user_list %}
		<li>
            {{ user.name }}:
            {# DON'T DO THIS: Generated implicit query per user #}
            {{ user.flavor.title }}
            {# DON'T DO THIS: Second implicit query per user!!! #}
            {{ user.flavor.scoops_remaining }}
        </li>
	{% endfor %}
</ul>

```

> 그런 다음 각 사용자를 호출하면 두 번째 쿼리가 생성됩니다.
>
> 별 것 아닌 것 같지만, 사용자가 충분하고 이러한 실수를 충분히 자주 했다면 사이트에 많은 문제가 
> 발생했을 것입니다.
>
>
> 한 가지 빠른 수정은 Django ORM의 select_related() 메서드를 사용하는 것입니다.



```jsp
<!-- 예제 14.12: select_related로 쿼리된 데이터 -->

{% comment %}
List generated via User.objects.all().select_related('flavor')
{% endcomment %}

<h1>Ice Cream Fans and their favorite flavors.</h1>
<ul>
{% for user in user_list %}
    <li>
        {{ user.name }}:
        {{ user.flavor.title }}
        {{ user.flavor.scoops_remaining }}
    </li>
{% endfor %}
</ul>

```

> 한 가지 더: 모델 메서드를 사용하는 경우에도 마찬가지입니다.
> 템플릿에서 호출된 모델 메서드에 쿼리 로직를 너무 많이 넣는 것은 주의하십시오.



##### 14.3.4 Gotcha 4: 템플릿의 숨겨진 CPU 로드

> 집중적인 CPU 처리를 초래하는 템플릿의 순진해 보이는 호출에 주의하십시오.
>
> 템플릿이 단순해 보이고 매우 적은 코드를 포함할 수 있지만 한 줄로 많은 처리를 수행하는 개체 메서드를 
> 호출할 수 있습니다.
>
> 일반적인 예로는 `sorl-thumbnail`과 같은 라이브러리에서 제공하는 템플릿 태그와 같이 이미지를 조작하는 템플릿 태그가 있습니다.
>
> 많은 경우에 이와 같은 도구는 훌륭하게 작동하지만 몇 가지 문제가 있습니다.
>
> 특히 템플릿 내부의 파일 시스템(종종 네트워크를 통해)에 이미지 데이터를 조작하고 저장하는 것은 템플릿 내에 초크 포인트(병목 지점)가 있음을 의미합니다.
>
> 이것이 많은 이미지 또는 데이터 처리를 처리하는 프로젝트가 템플릿에서 보기, 모델, 도우미 메서드 또는 Celery 또는 Django 채널과 같은 비동기 메시지 대기열로 이미지 처리를 가져옴으로써 사이트 성능을 높이는 이유입니다.



##### 14.3.5 Gotcha 5: 템플릿의 숨겨진 REST API 호출

> 객체 메소드 호출에 액세스하여 템플릿 로드 지연을 도입하는 것이 얼마나 쉬운지 이전 문제에서 
> 보았습니다.
>
> 이는 로드가 많은 메서드뿐만 아니라 REST API 호출을 포함하는 메서드에서도 마찬가지입니다.
>
> 좋은 예는 불행히도 프로젝트에 절대적으로 필요한 타사 서비스에서 호스팅하는 느린 지도 API를 쿼리하는 것입니다.
>
> 뷰의 컨텍스트에 전달된 객체에 연결된 메서드를 호출하여 템플릿 코드에서 이 작업을 수행하지 마십시오.
>
> 실제 REST API 소비는 어디에서 발생해야 합니까?  다음 위치에서 이 작업을 수행하는 것이 좋습니다.
>
> ➤ "JavaScript 코드"를 사용하므로 프로젝트에서 콘텐츠를 제공한 후 클라이언트의 브라우저가 
> 	  작업을 처리합니다.
>       이렇게 하면 클라이언트가 데이터 로드를 기다리는 동안 즐겁게 하거나 주의를 분산시킬 수 있습니다.
>
> ➤ 메시지 대기열, 추가 스레드, 다중 프로세스 등을 포함하여 느린 프로세스가 다양한 방식으로 처리될 수 있는 보기의 Python 코드.



##### 14.4 생성된 HTML을 예쁘게 만드는 데 신경 쓰지 마세요.

> 솔직히 말해서 Django 프로젝트에서 생성된 HTML이 매력적인지 아무도 신경 쓰지 않습니다.
>
> 사실, 누군가가 렌더링된 HTML을 본다면 브라우저 인스펙터의 렌즈를 통해 볼 것이므로 어쨌든 
> HTML 간격을 재정렬합니다.
>
> 따라서 Django 템플릿의 코드를 뒤섞어 멋진 HTML을 렌더링하면 청중을 위해 코드를 난독화하는 데 시간을 낭비하게 됩니다.
>
> 그러나 우리는 다음과 같은 코드를 보았습니다. 
> 이 사악한 코드 조각은 멋진 형식의 HTML을 생성하지만 그 자체는 읽을 수 없고 유지 관리할 수 없는 
> 템플릿 엉망입니다.



###### Example 14.13: 예쁜 HTML 코드를 생성하기 위해 템플릿 코드를 난독화하기

```html
{% comment %}Don't do this! This code bunches everything
together to generate pretty HTML.
{% endcomment %}
{% if list_type=='unordered' %}<ul>{% else %}<ol>{% endif %}{% for
syrup in syrup_list %}<li class="{{ syrup.temperature_type|roomtemp
}}"><a href="{% url 'syrup_detail' syrup.slug %}">{% syrup.title %}
</a></li>{% endfor %}{% if list_type=='unordered' %}</ul>{% else %}
</ol>{% endif %}

```



> 위의 스니펫을 작성하는 더 좋은 방법은 들여쓰기와 한 줄에 하나의 작업을 사용하여 읽기 쉽고
> 유지 관리 가능한 템플릿을 만드는 것입니다.



###### 예제 14.14: 이해할 수 있는 템플릿 코드

```html

{# Use indentation/comments to ensure code quality #}
{# start of list elements #}
{% if list_type=='unordered' %}
	<ul>
{% else %}
	<ol>
{% endif %}
{% for syrup in syrup_list %}
    <li class="{{ syrup.temperature_type|roomtemp }}">
		<a href="{% url 'syrup_detail' syrup.slug %}">
			{% syrup.title %}
		</a>
	</li>
{% endfor %}
{# end of list elements #}
{% if list_type=='unordered' %}
</ul>
{% else %}
</ol>
{% endif %}

```



> 생성되는 공백의 양이 걱정되십니까? 하지마세요.
> 우선, 숙련된 개발자는 최적화를 위해 난독화보다 코드 가독성을 선호합니다.
>
> 둘째, 여기에서 수동으로 할 수 있는 것보다 더 많은 도움이 될 수 있는 압축 및 축소 도구가 있습니다.
>
> 자세한 내용은 26장: 병목 현상 찾기 및 줄이기를 참조하십시오.



##### 14.5 템플릿 상속 탐색

> 다른 템플릿에서 상속할 간단한 base.html 파일부터 시작하겠습니다.



###### 예제 14.15: 기본 HTML 파일

```html
{# simple base.html #}
{% load static %}
<html>
<head>
<title>
{% block title %}Two Scoops of Django{% endblock title %}
</title>
{% block stylesheets %}
<link rel="stylesheet" type="text/css" href="{% static 'css/project.css' %}">
{% endblock stylesheets %}
</head>
	<body>
		<div class="content">
			{% block content %}
			<h1>Two Scoops</h1>	
			{% endblock content %}
	    </div>
	</body>
</html>
```



> base.html 파일에는 다음 기능이 포함되어 있습니다.
>
> ➤ "Two Scoops of Django"가 포함된 제목 블록. 
> ➤ 사이트 전체에서 사용되는 project.css 파일에 대한 링크가 포함된 스타일시트 블록. 
> ➤ "<h1>Two Scoops</h1>"를 포함하는 콘텐츠 블록. 



> 이 예에서는 아래에 요약된 세 개의 템플릿 태그만 사용합니다.



###### 1. Template Tag {% load %} 

> Purpose
> staticfile 내장 템플릿 태그 라이브러리를 로드합니다.

###### 2. {% block %} 

> base.html은 상위 템플릿이므로 하위 템플릿으로 채울 수 있는 하위 블록을 정의합니다.
> 필요한 경우 재정의할 수 있도록 링크와 스크립트를 내부에 배치합니다.

###### 3. {% static %}

> 정적 미디어 서버에 대한 명명된 정적 미디어 인수를 확인합니다.



> base.html이 사용 중임을 보여주기 위해 간단한 about.html이 여기에서 다음을 상속하도록 합니다.
> ➤ 사용자 정의 제목.
> ➤ 원래 스타일시트 및 추가 스타일시트.
> ➤ 원본 머리글, 하위 머리글 및 단락 내용.
> ➤ 자식 블록 사용.
> ➤ {{ block.super }} 템플릿 변수의 사용.



###### 예제 14.16: base.html에서 확장하기

```html
{% extends "base.html" %}
{% load static %}
{% block title %}About Audrey and Daniel{% endblock title %}
{% block stylesheets %}
{{ block.super }}
<link rel="stylesheet" type="text/css" href="{% static 'css/about.css' %}">
{% endblock stylesheets %}
{% block content %}
	{{ block.super }}
	<h2>About Audrey and Daniel</h2>
	<p>They enjoy eating ice cream</p>
{% endblock content %}
```



> 뷰에서 이 템플릿을 렌더링하면 다음 HTML이 생성됩니다.



###### 예제 14.17: 렌더링된 HTML

```html
<html>
<head>
<title>About Audrey and Daniel</title>
<link rel="stylesheet" type="text/css" href="/static/css/project.css">
<link rel="stylesheet" type="text/css" href="/static/css/about.css">
</head>
<body>
    <div class="content">
        <h1>Two Scoops</h1>
        <h2>About Audrey and Daniel</h2>
        <p>They enjoy eating ice cream</p>
    </div>
</body>
</html>

```

> 렌더링된 HTML에 사용자 정의 제목, 추가 스타일시트 링크 및 본문에 더 많은 자료가 있는 방법에 
> 주목하십니까?
>
> 아래 표를 사용하여 about.html 템플릿의 템플릿 태그와 변수를 검토합니다.



###### 1. Template Object  {% extends %}

> about.html이 base.html을 상속하거나 확장하고 있음을 Django에 알립니다.



###### 2. {% block %} 

> about.html은 자식 템플릿이므로 block은 base.html에서 제공하는 내용을 재정의합니다.
> 즉, 제목이 <title>Audrey and Daniel</title>으로 렌더링됩니다.



###### 3. {{ block.super }}

> 자식 템플릿의 블록에 배치하면 부모의 콘텐츠도 블록에 포함됩니다.
> about.html 템플릿의 콘텐츠 블록에서 다음이 렌더링됩니다.
> "<h1>두 스쿱</h1>"



#### 14.6 block.super는 Power of control 을 제공합니다

> base.html에서 모든 것을 상속하지만 project.css 파일에 대한 프로젝트 링크를  Dashboard.css에 대한 링크로 대체하는 템플릿이 있다고 가정해 보겠습니다.
>
> 이 사용 사례는 일반 사용자를 위한 하나의 디자인이 있는 프로젝트와 직원을 위한 다른 디자인의 대시보드가 있는 경우에 발생할 수 있습니다.
>
>
> {{ block.super }}를 사용하지 않는 경우, 종종 base_dashboard.html과 같은 이름으로 명명되는 완전히 새로운 기본 파일을 작성해야 합니다.
>
> 좋든 나쁘든 이제 우리는 두 가지 템플릿 아키텍처를 유지 관리해야 합니다.
>
> {{ block.super }}를 사용하는 경우 두 번째(또는 세 번째 또는 네 번째) 기본 템플릿이 필요하지 않습니다.
> 모든 템플릿이 base.html에서 확장된다고 가정하면 {{ block.super }}를 사용하여 템플릿을 제어할 수 
> 있습니다. 
>
> 다음은 세 가지 예입니다.



###### 1. project.css와 사용자 정의 링크를 모두 사용하는 템플릿:

###### 예제 14.18: 기본 CSS 및 사용자 정의 CSS 링크 사용

```html
{% extends "base.html" %}
{% block stylesheets %}
{{ block.super }} {# 이것은 project.css를 가져옵니다. #}
<link rel="stylesheet" type="text/css" href="{% static 'css/custom.css' %}" />
{% endblock stylesheets %}

```



###### 2. project.css 링크를 제외하는 대시보드 템플릿:

###### 예제 14.19: 기본 CSS 제외

```html
{% extends "base.html" %}
{% block stylesheets %}
<link rel="stylesheet" type="text/css" href="{% static 'css/dashboard.css' %}" />
{% comment %}
{{ block.super }}를 사용하지 않음으로써 이 블록은 base.html의 스타일시트 블록을 재정의합니다. 
{% endcomment %}
{% endblock stylesheets %}
```



###### 3. project.css 파일을 연결하는 템플릿:

###### 예제 14.20: 기본 CSS 파일 사용

```html
{% extends "base.html" %}
{% comment %}
{% block stylesheets %}를 사용하지 않음으로써 이 템플릿은 스타일시트는 기본에서 차단됩니다.
html 부모, 이 경우 기본 project.css 링크.
{% endcomment %}
```



> 이 세 가지 예는 {{ block.super }}가 제공하는 제어의 양을 보여줍니다.
> 변수는 템플릿 복잡성을 줄이는 좋은 방법이지만 완전히 이해하려면 약간의 노력이 필요할 수 있습니다. 



###### 팁: block.super는 유사하지만 super()와 동일하지 않습니다.

> 객체 지향 프로그래밍 배경에서 온 사람들의 경우 {{ block.super }} 변수의 동작을 Python 내장 함수 super()의 매우 제한된 버전과 같다고 생각하는 것이 도움이 될 수 있습니다.
>
> 본질적으로 {{ block.super }} 변수와 super() 함수는 모두 부모에 대한 액세스를 제공합니다.
>
> 그것들이 같지 않다는 것을 기억하십시오. 일부 개발자가 유용하게 사용할 수 있는 좋은 니모닉입니다.



#### 14.7 고려해야 할 유용한 사항

> 다음은 템플릿 개발 중에 염두에 두는 일련의 작은 사항입니다.



##### 14.7.1 파이썬 코드에 스타일을 너무 빡빡하게 연결하지 않기

> CSS 및 JS를 통해 렌더링된 모든 템플릿의 스타일을 완전히 제어하는 것을 목표로 합니다.
> 가능하면 CSS를 사용하여 스타일을 지정하십시오. 
>
> 메뉴 막대 너비 및 색상 선택과 같은 항목을 Python 코드에 절대 하드코딩하지 마십시오.
>
> 그런 유형의 스타일을 Django 템플릿에 넣지 마십시오.
>
> 다음은 몇 가지 팁입니다.
>
> ➤ 시각적 디자인 레이아웃과 전적으로 관련된 Python 코드에 마법 상수가 있는 경우 CSS 파일로 
> 이동해야 합니다.
>
> ➤ JavaScript에도 동일하게 적용됩니다.



##### 14.7.2 공통 협약

> 다음은 권장되는 이름 지정 및 스타일 규칙입니다.
>
> ➤ 템플릿 이름, 블록 이름 및 템플릿의 기타 이름에서 대시(-)보다 밑줄(_)을 선호합니다.
> 대부분의 Django 사용자는 이 규칙을 따르는 것 같습니다. 왜요? 글쎄, 파이썬 객체의 이름에는 밑줄이 허용되지만 대시는 금지되어 있기 때문입니다.
>
> ➤ 우리는 블록에 대해 명확하고 직관적인 이름을 사용합니다. {% block javascript %}이(가) 좋습니다.
>
> ➤ 엔드블록에 블록 태그의 이름을 포함합니다. 
> {% endblock%}만 작성하지 말고 전체 {% endblock javascript %}를 포함하십시오.
>
> ➤ 다른 템플릿에서 호출하는 템플릿에는 '_'가 접두사로 붙습니다. 
> 이는 {% include %} 또는 사용자 정의 템플릿 태그를 통해 호출된 템플릿에 적용됩니다.
>  {% extends %} 또는 {% block %}과 같은 템플릿 상속 제어에는 적용되지 않습니다.



##### 14.7.3 암시적 및 명명된 명시적 컨텍스트 개체를 적절하게 사용

> 일반 디스플레이 CBV를 사용할 때 템플릿에서 일반 {{ object_list }} 및 {{ object }}를 사용할 수 있습니다.
>
> 또 다른 옵션은 모델 이름을 따서 명명된 것을 사용하는 것입니다.
>
> 예를 들어, 토핑 모델이 있는 경우 템플릿에서 {{ object_list }} 및 {{ object }} 대신
> {{ topping_list }} 및 {{ topping }}을 사용할 수 있습니다.
>
> 즉, 다음 템플릿 예제가 모두 작동합니다.



###### 예제 14.21: 암시적 및 명시적 컨텍스트 객체

```html
{# templates/toppings/topping_list.html #}

{# 암시적 이름 사용, 코드 재사용에 좋음 #}
<ol>
{% for object in object_list %}
	<li>{{ object }} </li>
{% endfor %}
</ol>

{# 명시적 이름 사용, 개체별 코드에 적합 #}
<ol>
{% for topping in topping_list %}
	<li>{{ topping }} </li>	
{% endfor %}
</ol>
```



##### 14.7.4 하드코딩된 경로 대신 URL 이름 사용

> 일반적인 개발자 실수는 다음과 같이 템플릿의 URL을 하드코딩하는 것입니다.

```html
<a href="/flavors/">
```

> 이것의 문제는 사이트의 URL 패턴이 변경되어야 하는 경우 사이트 전체의 모든 URL을 해결해야 한다는 
> 것입니다.
>
> 이는 HTML, JavaScript 및 RESTful API에도 영향을 미칩니다.
>
> 대신 {% url %} 태그를 사용하고 URLConf 파일의 이름을 참조합니다.



###### 예제 14.23: URL 태그 사용

```html
<a href="{% url 'flavors:list' %}">
```



##### 14.7.5 복잡한 템플릿 디버깅

> Lennart Regebro가 권장하는 트릭은 템플릿이 복잡하고 변수가 실패하는 위치를 결정하기 어려워지면 TEMPLATES 설정의 OPTIONS에서 `string_if_invalid` 옵션을 사용하여 더 자세한 오류를 강제할 수 있다는 것입니다.
>
> 'string_if_invalid' : 템플릿 변수가 잘못된 경우 대신 사용할 문자열을 지정합니다.



###### 예 14.24: string_if_invalid 옵션 사용

```python
TEMPLATES = [
{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS': {
        'string_if_invalid': 'INVALID EXPRESSION: %s'
    }
}
```



#### 14.8 오류 페이지 템플릿

> 가장 많이 테스트되고 분석된 사이트라도 때때로 몇 가지 문제가 발생하지만 괜찮습니다.
> 문제는 이러한 오류를 처리하는 방법에 있습니다.
>
> 마지막으로 하고 싶은 일은 최종 사용자에게 못생긴 응답이나 빈 웹 서버 페이지를 다시 표시하는 것입니다.
>
> 최소한 404.html 및 500.html 템플릿을 만드는 것이 표준 관행입니다. GitHub 보기
> 고려할 수 있는 다른 유형의 오류 페이지에 대한 이 섹션 끝에 있는 HTML 스타일 가이드 링크.
>
> 정적 파일 서버(예: Nginx 또는 Apache)의 오류 페이지를 완전히 자체 포함된 정적 HTML 파일로 제공하는 것이 좋습니다.
>
> 그렇게 하면 전체 Django 사이트가 다운되지만 정적 파일 서버는 여전히 작동 중인 경우 오류 페이지가 계속 제공될 수 있습니다.
>
> PaaS를 사용하는 경우 오류 페이지의 설명서를 확인하십시오.
>
> 예를 들어, 그들 중 일부는 사용자가 500 오류에 사용할 사용자 정의 정적 HTML 페이지를 업로드할 수 있도록 합니다.



##### 경고: 오류 페이지를 지나치게 복잡하게 만들려는 유혹에 저항하십시오.

> 흥미롭거나 재미있는 오류 페이지는 귀하의 사이트에 끌릴 수 있지만 도취되지 마십시오.
>
> 404 페이지에 깨진 레이아웃이 있거나 500 페이지에서 CSS와 JavaScript를 로드할 수 없는 경우
> 당황스럽습니다. 
>
> 더 나쁜 것은 데이터베이스 오류 발생 시 중단되는 동적 500 오류 페이지입니다.



>
> GitHub의 500 오류 페이지는 화려하지만 완전히 정적이며 자체 포함된 오류 페이지의 좋은 예입니다. [github.com/500](https://github.com/500)의 소스를 보고 다음을 확인하십시오.
>
> ➤ 모든 CSS 스타일은 동일한 HTML 페이지의 헤드에 인라인되므로 별도의 스타일시트가 필요하지 않습니다.
>
> ➤ 모든 이미지는 HTML 페이지 내에 데이터로 완전히 포함됩니다. 
>      외부 URL에 대한 <img> 링크가 없습니다.
>
> ➤ 페이지에 필요한 모든 JavaScript는 HTML 페이지에 포함되어 있습니다. 
>      JavaScript 자산에 대한 외부 링크가 없습니다.
>
>
> 자세한 내용은 [Github HTML 스타일 가이드](https://styleguide.github.com/)를 참조하세요.



##### 14.9 미니멀리즘적 접근을 따르라

> 템플릿 코드에 최소한의 접근 방식을 취하는 것이 좋습니다.
>
> 소위 Django 템플릿의 한계를 축복으로 여기십시오.
>
> 이러한 제약 조건을 영감으로 사용하여 비즈니스 논리를 템플릿이 아닌 Python 코드에 더 많이 넣을 수 있는 간단하고 우아한 방법을 찾으십시오.
>
> 템플릿에 대한 최소한의 접근 방식을 취하면 Django 앱을 변경하는 형식 유형에 훨씬 쉽게 적용할 수 있습니다.
>
> 템플릿이 부피가 크고 중첩된 루프, 복잡한 조건 및 데이터 처리로 가득 차면 템플릿에서 비즈니스 논리 코드를 재사용하기가 더 어려워지고 API 보기와 같은 템플릿이 없는 보기에서 동일한 비즈니스 논리를 사용하는 것이 불가능하다는 것은 말할 것도 없습니다.
>
> API 및 웹 페이지가 증가하기 때문에 API 개발이 증가하는 시대로 나아가면서 코드 재사용을 위해 Django 앱을 구조화하는 것은 특히 중요합니다.
>
> 종종 다른 형식으로 동일한 데이터를 노출해야 합니다.
>
> 오늘날까지 HTML은 콘텐츠의 표준 표현으로 남아 있으며 이 장의 사례와 패턴을 제공합니다.



#### 14.10 요약

> 이 장에서는 다음을 다뤘습니다.
> ➤ {{ block.super }} 사용을 포함한 템플릿 상속.
> ➤ 읽기 쉽고 유지 관리 가능한 템플릿 작성.
> ➤ 템플릿 성능을 최적화하는 쉬운 방법.
> ➤ 템플릿 처리 제한 문제.
> ➤ 오류 페이지 템플릿.
> ➤ 템플릿에 대한 기타 유용한 정보가 많이 있습니다.
>
> 다음 장에서는 템플릿 태그와 필터를 살펴보겠습니다.