# Form Fundamentals

장고 폼은 강력한 기능을 가지고 있으며, 데이터를 입력받을 때 폼을 이용하는 법을 아는 것은 데이터를 깨끗하게 유지할 수 있습니다..(validation?)

폼이 구성되는 구조와 호출하는 방법을 이해한다면 대부분의 극단적인 상황을 해결할 수 있습니다.

장고 폼을 들어오는 모든 데이터의 유효성 검사하는 데 사용한다는 것을 꼭 기억하세요!


## 장고 폼 유효성 검사

대부분의 경우 POST 메서드의 HTTP 요청의 유효성 검사하는데 장고 폼을 사용하지만 꼭 이렇게만 사용하도록 제한하지는 않습니다.

다른 프로젝트에서 가져온 CSV 파일을 통해 모델을 업데이트 하는 장고 앱이 있다고 가정해봅시다.(흔한 경우는 아님)
<img src="https://user-images.githubusercontent.com/57426244/136874655-6e9192c0-825d-4158-b350-85b3337c0fbb.png" width="50%" />

add_csv_purchases() 함수에 유효성 검사 코드를 추가 할 수 있지만 재사용성을 고려하여 장고 폼을 사용하는 것이 좋습니다.

아래 방법을 사용하면 자체 유효성 검사 시스템을 구성하는 대신 장고에서 제공하는 데이터 테스트 프레임워크를 사용한다는 것입니다.

```python
import csv

from django.utils.six import StringIO

from django import forms

from .models import Purchase, Seller

class PurchaseForm(form.ModelForm):
    class Meta:
        model = Purchase
    
    def clean_seller(self):
        seller = self.cleaned_data['seller']
        try:
            Seller.objects.get(name=seller)
        except Seller.DoseNotExist:
            msg = '{0} does not exist in purchase #{1}.'.format(
                seller, self.cleaned_data['purchase_number']
            )
            raise forms.ValidationError(msg)
        return seller
        
def add_csv_purchases(rows):

    rows = StringIO.StringIO(rows)
    
    records_added = 0
    errors = []
    # Generate a dict per row, with the first CSV row being the keys.
    for row in csv.DictReader(rows, delimiter=','):
        # Bind the row data to the PurchaseForm.
        form = PurchaseForm(row)
        # Check to see if the row data is valid.
        if form.is_valid():
            # Row data is valid so save the record.
            form.save()
            records_added += 1
        else:
            errors.append(form.errors)
            
    return records_added, errors
```

---
## TIP : 코드 파라메타

아르노 림부르(장고 공동 설립자?)는 장고 공식 문서에서 아래와 같이 ValidationError에 코드 매개변수를 전달할 것을 권장합니다.

```python
# 의미를 잘 모르겠네요...;;;
forms.ValidationError(__('Invalid value'), code='invalid')
```

위의 우리 예제에서는 사용하지 않았지만 필요하다면 추가 가능합니다.

장고 코어 개발자 마크 탐린에 의하면, "장고 공식 문서가 모든 곳에서 모법 사례로 코드 사용을 권장하는 데 다소 무리가 있다고 생각합니다. 물론 타사 응용 프로그램에서는 권장되어야 합니다.
그러나 오류의 특성을 확인하려는 상황에서는 모범 사례 입니다. 이는 복사 변경 사항(?)이 적용 될 수 있으므로 유효성 검사 오류 메시지를 확인하는 것보다 훨신 났습니다."

---

## HTML 폼에서 POST 메서드 사용하는 법

데이터를 변경하는 모든 HTML 양식은 POST 메서드를 통해 데이터를 제출해야 합니다.
```html
<form action="{% url 'flavor_add' %}" method="POST">
```
다만, 데이터를 변경하지 않는 쿼리를 제출하는 검색(멱등성)에서는 GET 메서드를 사용해야 합니다.

## 데이터를 수정하는 HTTP Form에는 CSRF(Cross-Site Request Forgery) Protection를 사용하라

장고는 CSRF Protection 기능을 내장하고 있으며, 사용하는 것을 잊으면 친절히 경고 메시지를 제공합니다. 

이것은 중요한 보안 이슈이며, 항상 이 기능을 사용할 것을 권장합니다.

```html
<form>
  {% csrf_token %}
  <input type="text" name="name"/>
</form>
```

저자의 경험에 따르면, CSRF 보호 기능을 사용하지 않아도 되는 때는 입증된 라이브러리에 의해 인증된 머신 엑세스(?????) 가능한 API를 생성할 때입니다.

API 요청은 요청별로 서명/인증되어야하니 인증을 위해서 HTTP 쿠키에 의존하는 것은 현실적이지 않습니다. 따라서 프레임워크를 사용할 때 CSRF가 항상 문제가 되는 것은 아닙니다.

???????????? 무슨 이야기인지 잘 모르겠네요...

데이터를 변경하는 API를 작성하는 경우 처음부터 장고의 CSRF 문서에 익숙해지는 것이 좋습니다. (https://docs.djangoproject.com/en/3.2/ref/csrf/)

---
## TIP: HTML Search Forms
HTML search form의 경우 데이터를 변경하지 않기 때문에 GET 메서드를 사용하며, 장고 CSRF protection은 사용하지 않아도 됩니다.

---

뷰에서 데코레이터를 사용하여 수동으로 csrf_protection를 사용하는 대신에, 장고 CsrfViewMiddleware를 사이트 전체에 포괄적으로 사용해야 합니다.

Jinja2(템플릿 엔진) 템플릿에서 CSRF 작동을 확인하려면 Section 16.3(Considerations When Using Jinja with Dajngo)를 보세요.

## Posting Data via AJAX

AJAX를 통해 데이터를 게시할 때도 장고의 CSRF Protection 기능을 꼭 사용해야 합니다.

대신? AJAX를 통해 게시할 때 "X-CSRF Token" HTTP 헤더를 설정해야 합니다.

장고 공식문서에서는 jQuery 1.5.1 이상의 도메인간 크로스 체킹과 POST 요청에 대해서만 이 헤더를 설정하는 방법을 소개하고 있습니다.
docs.djangoproject.com/en/3.2/ref/csrf/#ajax 자세한 내용은 Section 19.3.5를 참고

## 장고 폼에 인스턴스 속성을 추가하는 법

때때로 장고 폼의 claen(), clean_FOO(), save() 메서드에서 추가적인 폼 인스턴스 속성을 사용할 수 있어야 합니다.

request.user 객체를 사용 할 수 있도록 하는 것이 그 예 입니다.

```python
# Tester Form
from django import forms

from .models import Taster

class TasterForm(forms.ModelForm):

    class Meta:
        model = Taster
        
    def __init __(self, *args, **kwargs):
        # set the user as an attribute of the form
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

# Taster Update View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from .forms import TasterForm
from .models import Taster

class TasterUpdateView(LoginrequiredMixin, UpdateView):
    model = Taster
    form_class = TasterForm
    success_url = '/someplace/'
    
    def get_form_kwargs(self):
        # This method is what injects forms with keyword arguments.
        
        # grab the current set of form #kwargs
        kwargs = super().get_form_kwargs()
        # update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs

```



