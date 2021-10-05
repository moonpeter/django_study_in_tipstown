### 9 Best Practices for Function-Based Views



> Since the beginning of the Django project, function-based views have been in frequent use
> by developers around the world. 
> While class-based views have risen in usage, the simplicity of using a function is appealing to both new and experienced developers alike.
> While the authors are in the camp of preferring CBVs, we work on projects that use FBVs and here are some patterns we’ve grown to enjoy.



jango 프로젝트가 시작된 이후로 함수 기반 `View`는 전 세계 개발자들에 의해 자주 사용되었습니다.

클래스 기반 뷰의 사용이 증가했지만 함수 사용의 단순성은 
신규 개발자와 숙련된 개발자 모두에게 매력적입니다.

저자가 CBV를 선호하는 진영에 있는 동안 우리는 FBV를 사용하는 프로젝트에서 
작업하고 있으며 여기에 우리가 즐길 수 있게 된 몇 가지 패턴이 있습니다.



#### 9.1 Advantages of FBVs - FBV 장점

> The simplicity of FBVs comes at the expense of code reuse: 
> FBVs don’t have the same ability to inherit from superclasses the way that CBVs do. 
> They do have the advantage of being more functional in nature, which lends itself to a number of interesting strategies.



FBV의 단순성은 코드 재사용을 희생시키면서 옵니다.  
FBV는 CBV와 같은 방식으로 슈퍼클래스에서 상속할 수 있는 능력이 없습니다. 
그들은 본질적으로 더 기능적이라는 이점이 있으며, 이는 여러 흥미로운 전략에 적합합니다.



> We follow these guidelines when writing FBVs: 
> ➤ Less view code is better. 
> ➤ Never repeat code in views. 
> ➤ Views should handle presentation logic.
>      Try to keep business logic in models when possible, or in forms if you must. 
>
> ➤ Keep your views simple. 
> ➤ Use them to write custom 403, 404, and 500 error handlers.
> ➤ Complex nested-if blocks are to be avoided.


FBV를 작성할 때 다음 지침을 따릅니다. 
➤ View 코드가 적을수록 좋습니다. 
➤ Views 에서 코드를 반복하지 마십시오. 
➤ Views 는 프레젠테이션 논리를 처리해야 합니다. 
     가능한 경우 비즈니스 논리를 모델로 유지하거나 필요한 경우 양식으로 유지하십시오. 
➤ Views 를 단순하게 유지하십시오. 
➤ 이를 사용하여 사용자 지정 403, 404 및 500 오류 처리기를 작성합니다. 
➤ 복잡한 nested-if (중첩된 if) 블록은 피해야 합니다.



#### 9.2 Passing the HttpRequest Object - HttpRequest 객체 전달

> There are times where we want to reuse code in views, 
> but not tie it into global actions such as middleware or context processors.
>
> Starting in the introduction of this book,  we advised creating utility functions that can be used across the project.



뷰에서 코드를 재사용하고 싶지만  미들웨어나 컨텍스트 프로세서와 같은 전역 작업에
묶고 싶지 않은 경우가 있습니다. 
이 책의 도입부 부터 프로젝트 전반에 걸쳐 사용할 수 있는 유틸리티 함수를 만드는 것이 좋습니다.



```python
# sprinkes/utils.py

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

def check_sprinkle_rights(request: HttpRequest) -> HttpRequest:
	if request.user.can_sprinkle or request.user.is_staff:
		return request
	
  # Return a HTTP 403 back to the user
	raise PermissionDenied
```



> The check_sprinkle_rights() function does a quick check against the rights of the user,
> raising a django.core.exceptions.PermissionDenied exception,  
> which triggers a custom HTTP 403 view as we describe in Section 31.4.3: django.core.exceptions.PermissionDenied.


check_sprinkle_rights() 함수는 섹션 31.4.3절- django.core.exceptions.PermissionDenied 에서  
설명한 것처럼 사용자 정의 HTTP 403 보기를 트리거하는 `django.core.exceptions.PermissionDenied` 
예외를 발생시켜 사용자의  권한을 빠르게 확인합니다.



> You’ll note that we return back a HttpRequest object rather than an arbitrary value
> or evena None object.
> We do this because as Python is a dynamically typed language,  we can attach additional attributes to the HttpRequest. For example


임의의 값이나 None 객체가 아닌 HttpRequest 객체를 반환한다는 것을 알 수 있습니다. 
Python은 동적으로 유형이 지정된 언어이므로 HttpRequest에  추가 속성을 첨부할 수 있기 때문에 
이 작업을 수행합니다. 예를 들어

```python
# Example 9.2: Enhanced sprinkles/utils.py

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

def check_sprinkle_rights(request: HttpRequest) -> HttpRequest:
	if request.user.can_sprinkle or request.user.is_staff:
		# By adding this value here it means our display templates
		# can be more generic. We don't need to have
		# {% if request.user.can_sprinkle or equest.user.is_staff %}
		# instead just using
		# {% if request.can_sprinkle %}

		# 여기에 이 값을 추가하면 디스플레이 템플릿이 더 일반적일 수 있습니다.
		# {% if request.can_sprinkle %} 를 사용하는 대신 
		# {% if request.user.can_sprinkle or request.user.is_staff %}
        # 를 가질 필요가 없습니다.
	
		request.can_sprinkle = True
		return request
	
    # Return a HTTP 403 back to the user
	raise PermissionDenied
```



> There’s another reason, which we’ll cover shortly.
> In the meantime, let’s demonstrate this code in action.

우리가 곧 다룰 또 다른 이유가 있습니다. 
그동안 이 코드가 실제로 작동하는지 시연해 보겠습니다.


```python
# Example 9.3: Passing the Request Object in FBVs
# sprinkles/views.py
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Sprinkle
from .utils import check_sprinkles

def sprinkle_list(request: HttpRequest) -> HttpResponse:
	"""Standard list view"""
	request = check_sprinkles(request)
	return render(
		request, 
		"sprinkles/sprinkle_list.html",
		{"sprinkles": Sprinkle.objects.all()}
)

def sprinkle_detail(request: HttpRequest, pk: int) -> HttpResponse:
	"""Standard detail view"""
	request = check_sprinkles(request)
	sprinkle = get_object_or_404(Sprinkle, pk=pk)
	return render(
		request,
		"sprinkles/sprinkle_detail.html",
		{"sprinkle": sprinkle}
	)

def sprinkle_preview(request: HttpRequest) -> HttpResponse:
	"""Preview of new sprinkle, but without the
	check_sprinkles function being used.
	"""
	sprinkle = Sprinkle.objects.all()
	return render(
		request,
		"sprinkles/sprinkle_preview.html",
		{"sprinkle": sprinkle}
	)
```



> Another good feature about this approach is that it’s trivial to integrate  into class-based views.

이 접근 방식의 또 다른 좋은 기능은 클래스 기반 뷰에 쉽게 통합할 수 있다는 것입니다.



```python
from django.views.generic import DetailView

from .models import Sprinkle
from .utils import check_sprinkles

class SprinkleDetail(DetailView):
	"""Standard detail view"""
	model = Sprinkle

	def dispatch(self, request, *args, **kwargs):
		request = check_sprinkles(request)
		return super().dispatch(request, *args, **kwargs)
```



```python
TIP: Specific Function Arguments Have Their Place
팁: 특정 함수 인수는 제자리에 있어야 합니다.

The downside to single argument functions is 
that specific function arguments like ‘pk’, ‘flavor’ or ‘text’ 
make it easier to understand the purpose of a function at a glance.

단일 인수 함수의 단점은 'pk', 'flavor' 또는 'text'와 같은 특정 함수 인수를 
사용하여 함수의 목적을 한 눈에 더 쉽게 이해할 수 있다는 것입니다.

In other words, try to use this technique for actions that are as generic as possible.
즉, 가능한 한 일반적인 작업에 이 기술을 사용하십시오.
```



> Since we’re repeatedly reusing functions inside functions, 
> wouldn’t it be nice to easily recognize when this is being done? 
> This is when we bring decorators into play.

함수 내에서 함수를 반복적으로 재사용하고 있기 때문에 이것이 언제 수행되는지 
쉽게 인식하는 것이 좋지 않을까요? 
이것은 데코레이터를 사용할 때입니다.



#### 9.3 Decorators Are Sweeet - 데코레이션 멍꿀

> For once, this isn’t about ice cream, it’s about code!
> In computer science parlance, syntactic sugar is a syntax added  to a programming language in order to make things easier to read or to express.

일단 이것은 아이스크림에 관한 것이 아니라 코드에 관한 것입니다!
컴퓨터 과학 용어에서 구문 설탕은 더 쉽게 읽거나 표현하기 위해 프로그래밍 언어에 추가된 구문입니다.



> In Python, decorators are a feature added not out of necessity, 
> but in order to make code cleaner and sweeter for humans to read.

파이썬에서 데코레이터는 필요에 의해 추가된 기능이 아니라 
인간이 읽을 수 있도록 코드를 더 깔끔하고 달콤하게 만들기 위해 추가된 기능입니다.

> So yes, Decorators Are Sweet.  
> When we combine the power of simple functions with the syntactic sugar of decorators,  
> we get handy, reusable tools like the extremely useful to the point of being ubiquitous django.contrib.auth.decorators.login_required decorator.



간단한 함수의 힘과 데코레이터의 문법적 설탕을 결합하면, 
우리는 어디에나 있을 정도로 매우 유용하고 편리하고 재사용이 가능한 도구를 얻습니다.



> Here’s a sample decorator template for use in function-based views.

다음은 함수 기반 보기에서 사용하기 위한 샘플 데코레이터 템플릿입니다.

```python
# Example 9.5: Simple Decorator Template
import functools

def decorator(view_func):
	@functools.wraps(view_func)
	def new_view_func(request, *args, **kwargs):
		# You can modify the request (HttpRequest) object here.
		# 여기에서 request(HttpRequest) 개체를 수정할 수 있습니다.
		response = view_func(request, *args, **kwargs)

		# You can modify the response (HttpResponse) object here.
		# 여기에서 response(HttpResponse) 개체를 수정할 수 있습니다.
		return response
	return new_view_func
```



> That might not make too much sense, 
> so we’ll go through it step-by-step, using in-line code comments to clarify what we are doing.

너무 의미가 없을 수도 있으므로 
인라인 코드 주석을 사용하여 우리가 하는 일을 명확히 하여  단계별로 살펴보겠습니다.

> First, let’s modify the decorator template from the previous example to match our needs 

먼저 필요에 맞게 이전 예제의 데코레이터 템플릿을 수정해 보겠습니다.



```python
# Example 9.6: Decorator Example

# sprinkles/decorators.py
import functools

from . import utils

# based off the decorator template from the previous example
def check_sprinkles(view_func):
	"""Check if a user can add sprinkles"""
	@functools.wraps(view_func)
	def new_view_func(request, *args, **kwargs):
		# Act on the request object with utils.can_sprinkle()
		request = utils.can_sprinkle(request)

		# Call the view function
		response = view_func(request, *args, **kwargs)

		# Return the HttpResponse object
		return response
	return new_view_func
```

> Then we attach it to the function thus

그런 다음 함수에 다음과 같이 연결합니다.

```python
# Example 9.7: Example of Using a Decorator

# sprinkles/views.py
from django.shortcuts import get_object_or_404, render

from .decorators import check_sprinkles
from .models import Sprinkle

# Attach the decorator to the view
@check_sprinkles
def sprinkle_detail(request: HttpRequest, pk: int) -> HttpResponse:
	"""Standard detail view"""
	sprinkle = get_object_or_404(Sprinkle, pk=pk)

	return render(request, "sprinkles/sprinkle_detail.html",
	{"sprinkle": sprinkle})
```



```python
TIP: What About functools.wraps()

Astute readers may have noticed that our decorator examples used 
the functools.wraps() decorator function from the Python standard library.
예리한 독자는 우리의 데코레이터 예제가 Python 표준 라이브러리의 functools.wraps() 
데코레이터 함수를 사용했음을 알아차렸을 것입니다.

This is a convenience tool that copies over metadata including 
critical info like docstrings to the newly decorated function.
이것은 독스트링과 같은 중요한 정보를 포함하는 메타데이터를 
새로 장식된 함수에 복사하는 편리한 도구입니다.

It’s not necessary, but it makes project maintenance much easier.
필수는 아니지만 프로젝트 유지 관리가 훨씬 쉬워집니다.
```



#### 9.3.1 Be Conservative With Decorators

> As with any powerful tool, decorators can be used the wrong way.

모든 강력한 도구와 마찬가지로 데코레이터는 잘못된 방식으로 사용될 수 있습니다.



> Too many decorators can create their own form of obfuscation, making even complex class-based view hierarchies seem simple in comparison.

너무 많은 데코레이터가 자체 형식의 난독화를 만들 수 있으므로  
복잡한 클래스 기반 뷰 계층도 비교적 단순해 보입니다.



> When using decorators, establish a limit of how many decorators can be set on a view and stick with it.

데코레이터를 사용할 때 뷰에 설정할 수 있는 데코레이터의 수를 제한하고 그대로 유지하세요.



Video on the subject:
 https://pyvideo.org/pycon-us-2011/pycon-2011--how-to-write-obfuscated-python.html
PyCon 2011 - How to write obfuscated python (SD quality)
 https://www.youtube.com/watch?v=eiaFUCp8dWc



#### 9.3.2 Additional Resources on Decorator

데코레이터에 대한 추가 리소스 



Decorators Explained - 없음..
https://www.jeffknupp.com/blog/2013/11/29/improve-your-python-decorators-explained/ 

Decorator Cheat Sheet by author Daniel Roy Greenfeld 저자 
Daniel Roy Greenfeld의 데코레이터 치트 시트 
https://daniel.feldroy.com/posts/python-decorator-cheatsheet



#### 9.4 Passing the HttpResponse Object

> Just as with the HttpRequest object, we can also pass around the HttpResponse
> object from function to function.
> Think of this as a selective Middleware.process_template_response() method.

HttpRequest 객체와 마찬가지로 함수에서 함수로 HttpResponse 객체를 전달할 수도 있습니다.
이것을 선택적 Middleware.process_template_response() 메소드로 생각하십시오.

See docs.djangoproject.com/en/3.2/topics/http/middleware/#process-template-response.



> Yes, this technique can be leveraged with decorators.  See Example 8.5 which gives a hint as to how this can be accomplished.

예, 이 기술은 데코레이터와 함께 활용할 수 있습니다.
이것이 어떻게 달성될 수 있는지에 대한 힌트를 제공하는 예제 8.5를 참조하십시오.



#### 9.5 Additional Resources for Function-Based Views

> Luke Plant is a core Django developer with strong opinions 
> in favor of Function-Based Views.
> While we don’t agree with most of his anti-CBV arguments he lists 
> in the article linked below,
> this nevertheless is of immeasurable value to anyone writing FBVs : 
> https://spookylukey.github.io/django-views-the-right-way/

Luke Plant는 Function-Based Views에 찬성하는 강력한 의견을 가진
핵심 Django 개발자입니다.

우리는 그가 아래 링크된 기사에 나열한 대부분의 CBV 반대 주장에 동의하지 않지만, 
그럼에도 불구하고 이것은 FBV를 작성하는 누구에게나 측정할 수 없는 가치가 있습니다.


#### 9.6 Summary

> Function-based views are still alive and well in the Django world.
> If we remember that every function accepts an HttpRequest object 
> and returns an HttpResponse object, we can use that to our advantage.
> We can leverage in generic HttpRequest and HttpResponse
> altering functions, which can also be used to construct decorator functions.

함수 기반 뷰는 Django 세계에서 여전히 유효합니다.

모든 함수가 HttpRequest 객체를 받아들이고 HttpResponse 객체를 반환한다는 것을 기억한다면
우리는 그것을 유리하게 사용할 수 있습니다.

일반 HttpRequest 및 HttpResponse에서 활용할 수 있습니다.
데코레이터 기능을 구성하는 데 사용할 수도 있습니다.

>  We’ll close this chapter by acknowledging that every lesson we’ve learned
> about function based views can be applied to what we begin to discuss next chapter, 
> classbased view.

함수 기반 뷰에 대해 배운 모든 교훈이 다음 장인 
클래스 기반 뷰에 대해 논의하기 시작하는 것에 적용될 수 있음을 인정하면서
이 장을 마무리할 것입니다.

