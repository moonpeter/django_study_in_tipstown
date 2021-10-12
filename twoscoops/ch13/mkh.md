# Form Fundamentals

장고 폼은 강력한 기능을 가지고 있으며, 데이터를 입력받을 때 폼을 이용하는 법을 아는 것은 데이터를 깨끗하게 유지할 수 있습니다..(validation?)

폼이 구성되는 구조와 호출하는 방법을 이해한다면 대부분의 극단적인 상황을 해결할 수 있습니다.

장고 폼을 들어오는 모든 데이터의 유효성 검사하는 데 사용한다는 것을 꼭 기억하세요!


## 13.1 장고 폼 유효성 검사

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

## 13.2 HTML 폼에서 POST 메서드 사용하는 법

데이터를 변경하는 모든 HTML 양식은 POST 메서드를 통해 데이터를 제출해야 합니다.
```html
<form action="{% url 'flavor_add' %}" method="POST">
```
다만, 데이터를 변경하지 않는 쿼리를 제출하는 검색(멱등성)에서는 GET 메서드를 사용해야 합니다.

## 13.3 데이터를 수정하는 HTTP Form에는 CSRF(Cross-Site Request Forgery) Protection를 사용하라

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

## 13.3.1 Posting Data via AJAX

AJAX를 통해 데이터를 게시할 때도 장고의 CSRF Protection 기능을 꼭 사용해야 합니다.

대신? AJAX를 통해 게시할 때 "X-CSRF Token" HTTP 헤더를 설정해야 합니다.

장고 공식문서에서는 jQuery 1.5.1 이상의 도메인간 크로스 체킹과 POST 요청에 대해서만 이 헤더를 설정하는 방법을 소개하고 있습니다.
docs.djangoproject.com/en/3.2/ref/csrf/#ajax 자세한 내용은 Section 19.3.5를 참고

## 13.4 장고 폼에 인스턴스 속성을 추가하는 법

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

---

## PACKAGE TIP : django-braces's ModelForm Mixins

request.user 객체를 장고 폼에 삽입하는 것은 자주 수행되며, django-braces는 사용자를 대신할 수 있습니다. 그럼에도(자동으로 해주지만) 작동 방식을 아는 것은 request.user 객체가 아닌 것을 추가할 때 유용합니다.

- https://django-braces.readthedocs.io/en/latest/form.html#userformkwargsmixin
- https://django-braces.readthedocs.io/en/latest/form.html#userkwargmodelformmixin

---

## 13.5 폼 유효성 검사 작동 원리
form.is_valid()를 호출 했을 때 workflow:
    1) 폼에 바인딩 된 데이터가 있는 경우 form.full_clean() 메서드를 호출합니다.
    2) form.full_clean() 메서드는 폼 필드를 순회하며 각 필드를 자체 유효성 검사를 합니다.
        a) 필드로 들어오는 데이터는 to_python() 메서드를 통해서 Python으로 강제변환되거나 ValidationError가 발생합니다.
        b) 데이터는 커스텀 검사기(validators)를 포함하여 필르별 규칙에 따라 검증됩니다.
        c) 사용자 정의 clean_<field>()메서드가 있으면 이 때 호출됩니다.
    3) form.full_clean() 메서드는 form.clean() 메서드를 실행합니다.
    4) ModelForm 인스턴스인 경우, form.post_clean()은 다음을 실행합니다.
        a) form.is_valid()가 True인지 False인지에 관계없이 ModelForm 데이터를 Model 인스턴스로 설정합니다.
        b) 모델의 clean()메서드를 호출합니다. 참고로 ORM을 통해 모델 인스턴스를 저장하는 것은 모델의 clean()메서드를 호출하지 않습니다.
    
## 13.5.1 폼에 저장된 모델폼 데이터와 모델 인스턴스
ModelForm에서 폼 데이터는 아래 두 가지 단계를 거쳐 저장됩니다.
    1) 폼 데이터가 폼 인스턴스에 저장됩니다.
    2) 다음, 폼 데이터가 모델 인스턴스에 저장됩니다.
    
ModelForms는 form.save()메서드에 의해 활성화 될 때까지 모델 인스턴스에 저장하지 않으므로 유용하게 활용 가능합니다.
    
예를 들어, 사용자가 제공한 폼 데이터와 의도한 모델 인스턴스의 변경 사항을 모두 저장하여 폼에 대한 실패 세부 정보를 파악할 수 있습니다.
    
form_invalid()는 잘못된 데이터가 입력되어 폼의 유효성 검사가 실패한 후에 호출됩니다. 
    
아래 예 에서는 호출되면 ModelFormFailureHistory 레코드로 저장됩니다.
    
```python
# core/models.py
from django.db import models
    
class ModelFormFailureHistory(models.Model):
    form_data = models.TextField()
    model_data = models.TextFiled()
    
# flavors/views.py
import json
    
from django.contrib import messages
from django.core import serializers
    
from core.models import ModelFormFailureHistory
    
class FlavorActionMixin:
    
    @property
    def success_msg(self):
        return NotImplemented
    
    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Save invalid form and model data for later reference.
        form_data = json.dumps(form.cleaned_data)
        # Serialize the form.instance
        model_data = serializers.serialize('json', [form.instance])
        # Strip away leading and ending bracket leaving only a dict
        model_data = model_data[1:-1]
        ModelFormFailureHistory.objects.create(
            form_data=form_data,
            model_data=model_data
        )
        return super().form_invalid(form)
```
    
## 13.6 Form_add_error()를 사용하여 폼에 오류 추가
Form.add_error() 메서드를 사용하여 Form.clean()을 간소화 할 수 있습니다. 

```python
from django import forms
    
class IceCreamReviewForm(forms.Form):
    # Rest of tester form goes here
    
    def clean(self):
        cleaned_data = super().clean()
        flavor = cleaned_data.get('flavor')
        age = cleaned_data.get('age')
    
        if flavor == 'coffee' and age < 3:
            # Record errors that will be displayed later.
            msg = 'Coffee Ice Cream is not for Babies.'
            self.add_error('flavor', msg)
            self.add_error('age', msg)
                                          
        # Always return the full collection of cleaned data.
        return cleaned_data
```
    
                                          
                                          
