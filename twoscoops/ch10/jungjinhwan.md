# 10. Class-Based Views 모범사례

Django 는 CBVs(Class-Based Views) 를 작성하는 표준적인 방법을 제공한다. 사실, View 는 요청객체를 받아서 응답객체를 반환하는 호출가능한(Callable) 객체다. FBVs(Function-Based Views) 는 Callable 하다. CBVs 는 Callable 을 반환하는 as_view() 클래스 메서드를 제공한다. 이러한 메커니즘은 django.views.generic.View 를 통해 구현된다. 모든 CBVs 는 직/간접적으로 해당 클래스를 상속받는다.

장고 또한 일반적인 웹 프로젝트의 공통적인 패턴과 CBVs 의 힘을 보여주는 일련의 GCBVs(Generic Class-Based Views)들을 제공한다.

TIP : Djano GCBVs 가 제공하지 않는 부분을 채우기

기본적으로 장고는 GCBVs 에 유용한 Mixin 을 제공하지 않는다. django-braces 라이브러리는 이러한 문제를 다룬다. 이 라이브러리는 GCBVs 를 좀더 쉽고 빠르게 구현할 수 있는 분명한 Mixin 들을 제공한다. 이 라이브러리는 너무 유용하여 3개의 Mixin 이 Django 에 흡수되었습니다.

## 10.1 CBVs 작업시 가이드

- 적은 View 코드가 더 좋다.
- views 에서 코드를 반복하지 말라.
- Views 는 표현에 대한 로직을 다뤄야 한다. 최대한 비즈니스로직은 models 에 넣고 반드시 필요한 경우 forms 에 넣어라.
- views 를 단순하게 유지해라.
- mixins 를 더 단순하게 유지해라.

TIP : ccbv.co.uk에 익숙해지세요

틀림없이 이것은 6번째 가이드로 위치되어야 합니다. [ccbv.co.uk](http://ccbv.co.uk) 는 매우 유용하여 자체 tipbox 를 받을 자격이 있다고 느꼈습니다. 이 사이트는 CBV 에서 정의되거나 상속된 속성과 메서드를 하나의 포괄적인 페이지를 통해 단조롭게 제공합니다. 대부분의 장고 개발자들은 과거 CBVs 튜토리얼을 진행했을텐데 이때 공식문서보다 ccbv.co.uk 를 더 의존했을 것이다.

## 10.2 CBVs 에 Mixins 사용하기

아이스크림 Mixin 과 같이 프로그래밍의 Mixin 으로 생각해보십시오. 당신은 어떤 아이스크림이라도 mixin 을 통해 맛을 풍부하게 할 수 있습니다.

소프트 아이스크림은 mixins 의 매우 강한 이점

프로그래밍에서 mixin은 그 자체로 인스턴스화가 아닌 기능 제공의 상속을 위한 클래스다. 다중상속 프로그래밍 언어에서 mixins 는 기능이나 동작을 클래스에 더하는데 사용되어 진다.

장고 앱의 클래스뷰에 구성하여 믹스인의 힘을 사용할 수 있다.

Mixins 을 통해 클래스뷰를 구성할 때, Kenneth Lov 가 말한 다음의 상속 규칙을 추천한다. 이 규칙은 파이썬의 MRO 를 따른다.

가능한 가장 단순한것 부터 왼쪽에서 오른쪽으로 정의를 진행합니다.

1. Django 의 기본 view 는 항상 오른쪽에 둡니다.
2. 기본 view 의 왼쪽에 Mixins 을 둡니다.
3. Mixins 는 어떤 다른 클래스도 상속하지 않습니다. 상속 연결을 단순하게 유지합니다.

규칙을 따른 예시

```python
# Example 10.1 : Using Mixins in a View

from django.views.generic import TemplateView

class FreshFruitMixin:
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["has_fresh_fruit"] = True
		return context

class FruityFlavorView(FreshFruitMixin, TemplateView):
	template_name = "fruity_flavor.html"
```

다소 어리석은 예시에서, FruitFlavorView 클래스는 FreshFruitMixin 과 TemplateView 를 상속받습니다.

TemplateView 로 부터 Django 의 기본 뷰를 상속받고(규칙1), 그 왼쪽에 FreshFruitMixin 을 위치시킵니다(규칙2). 이렇게 하면 메서드와 속성이 제대로 실행될 것을 우린 알고있습니다.

## 10.3 어떤 작업에 어느 GCBV 를 사용해야 할까?

GCBV 의 힘은 단순함을 희생한 비싼 지불이 있습니다. GCGV 를 가져오는 것은 최대 8개의 부모클래스를 상속하는 복잡함을 함께 가져옵니다. 어떤작업에 어떤 뷰를 사용하는것을 고르는 것은 매우 어려울 수 있습니다.

이 문제를 해결하려면, 여기 handy chart 라고 불리는 CBV 제안이 있습니다. 여기에 나열된 모든 뷰들은 django.views.generic. 접두어가 붙은 것으로 가정됩니다.

[Untitled](https://www.notion.so/372e48641bf041eeb6a505e5b5a619b3)

TIP : Django CBV/GCBV 이용에 대한 세 가지 의견

1. **제네릭 뷰의 모든 종류를 최대한 이용하자**

작업양을 최소화 하기 위해 제네릭 뷰가 제공하는 모든 종류의 뷰를 최대한 이용하기를 장려한다.

1. **심플하게 django.views.generic.View 하나로 모든 뷰를 처리하자**

장고의 기본 클래스 뷰로도 충분히 원하는 기능을 소화할 수 있다.진정한 클래스 기반 뷰란 모든 뷰가 제네릭 클래스 기반 뷰이어야 한다.1번의 리소스 기반 접근 방식이 실패한 난해한 태스크에 대해서 효율적이다.

**3. 뷰를 정말 상속할 것이 아닌 이상 그냥 무시하자**

읽기 쉽고 이해하기 쉬운 FBV로 시작하고, 반드시 필요한 경우에만 CBV를 이용하자.

10.4 Django CBVs 의 일반적인 팁

장고의 클래스 기반 뷰와 제네릭 기반 뷰는 뷰, 템플릿 그리고 뷰와 템플릿에 대한 테스트를 신속하게 제작하는 데 그 목적이 있다.

10.4.1 Django CBV/GCBV 를 통해 인증된 사용자에 대한 접근 제한

```python
# flavors/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Flavor

class FlavorDetailView(LoginRequiredMixin, DetailView):
	model = Flavor
```

10.4.2 뷰에서 유효한 폼을 이용하여 커스텀 액션 구현하기

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Flavor

class FlavorCreateView(LoginRequiredMixin, CreateView):
	model = Flavor
	fields = ['title', 'slug', 'scoops_remaining']

	def form_valid(self, form):
		# Do custom logic here
		return super().form_valid(form)
```

10.4.3 뷰에서 부적합한 폼을 이용하여 커스텀 액션 구현하기

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Flavor

class FlavorCreateView(LoginRequiredMixin, CreateView):
	model = Flavor

	def form_invalid(self, form):
		# Do custom logic here
		return super().form_invalid(form)
```

**10.4.4 뷰 객체 이용하기**

콘텐츠를 렌더링하는 것에 클래스 기반 뷰를 이용한다면 자체적인 메서드와 속성을 제공하는 뷰 객체를 이용해 다른 메서드나 속성에서 호출이 가능하다.

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.functional import cached_property
from django.views.generic import UpdateView, TemplateView
from .models import Flavor
from .tasks import update_user_who_favorited

class FavoriteMixin:

	@cached_property
	def likes_and_favorites(self):
		"""Returns a dictionary of likes and favorites"""

		likes = self.object.likes()
		favorites = self.object.favorites()
		return {
			"likes": likes,
			"favorites": favorites,
			"favorites_count": favorites.count(),
		}

class FlavorUpdateView(LoginRequiredMixin, FavoriteMixin, UpdateView):
	model = Flavor
	fields = ['title', 'slug', 'scoops_remaining']

	def form_valid(self, form):
		update_user_who_favorited(
			instance=self.object,
			favorites=self.likes_and_favorites['favorites']
		)
		return super().form_valid(form)

class FlavorDetailView(LoginRequiredMixin, FavoriteMixin, TemplateView):
	model = Flavor

{# flavors/base.html #}
{% extends "base.html" %}

{% block likes_and_favorites %}
<ul>
	<li>Likes: {{ view.likes_and_favorites.likes }}</li>
	<li>Favorites: {{ view.likes_and_favorites.favorites_count }}</li>
</ul>

{% endblock likes_and_favorites %}
```

다양한 flavors/ 앱 템플릿에서 해당 속성을 호출할 수 있다는 장점이 있음

10.5 How GCBVs and Forms Fit Together

10.5.1 Views + ModelForm Example

10.5.2 Views + Form Example

10.6 Using Just django.views.generic.View

10.7 Additional Resources

10.8 Summary
