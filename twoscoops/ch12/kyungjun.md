# 12. 흔한 폼의 패턴

## 12.1 간단한 모델폼 with 기본 validators

- 모델폼을 CBV와 같이 사용하면, form을 수정하고, 추가하는 것을 몇 줄의 코드로 할 수 있다.
```python
# import 는 생략하겠습니다.
class FlavorCreateView(LoginRequiredMixin, CreateView):
    model = Flavor
    fields = ['title', 'slug', 'scoops_remaining']

class FlavorUpdateView(LoginRequiredMixin, UpdateView):
    model = Flavor
    fields = ['title', 'slug', 'scoops_remaining']
```
- 핵심 : 
1) Flavor 모델에 기반해서 자동적으로 ModelForm을 생성한다.
2) Flavor 모델 내의 필드의 기본 validation rule을 따른다.

## 12.2 Custom Form Field Validators in 모델 폼
- 만약 우리 프로젝트의 'dessert 앱'에서 사용되는 모든 title field가 "Tasty"로 시작해야 한다면?
- (해결) custom field validator
- 우선 validators.py 를 만들어라

# Example 12.2 validators.py
```python

```

- Tip : 너의 Validators를 주의해서 Test 해라

# Example 12.3 Adding Custom Validator to a Model
```python
class TastyTitlesAbstractModel(models.Model):
    class Meta:
        abstract = True
```
# 추상화 모델을 만들어서 사용해라. 단) 모델을 상속할 때는 주의해서 사용해라

# Example 12.4 Iheriting Validators

```python

```


- 만약 validate_tasty를 그냥 form 에서만 쓰고 싶다면?
- 만약 title field를 제외하고 다른 field에도 할당하고 싶다면?
- (이를 위해서는) 우리의 custom field를 사용한 custom FlavorForm이 필요하다

# Example 12.5 Adding Custom Validators to a Model Form
```python
from django import forms
from .models import Flavor
from core.validatos import validate_tasty

class FlavorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].validators.append(validate_tasty) # 필드 자체에 이렇게 .validotrs 쓰고 append로 custom validator 함수 넣음
        self.fields['slug'].validators.append(validate_tasty)

    class Meta:
        model = Flavor
        fields = ['title', 'slug']

```
custom form을 우리의 view에 붙여보자. 장고의 model 기반 edit view 는 model = Flavor(이런형태의 attribute설정으로) 자동적으로 Model Form을 만들어 준다.
우리는 기본을 override해서 custom FlavorForm을 넘겨줄거다. 

```python
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView

from .models import Flavor
from .forms import FlavorForm

class FlavorActionMixin:

    model = Flavor
    fields = ['title', 'slug', 'scoops_remaining']

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(slef, form):
        messages.info(self.request, self.succes_msg)
        return super().form_valid(form)

class FlavorCreateView(LoginRequiredMixin, FlavorActionMixin, CreateView):
    success_msg = 'created'
    # Explicitly attach the FlavorForm class
    form_class = FlavorForm


# mixin 에서 유효성 검증을 할 field들을 명시해 둠
class FlavorUpdateView(LoginRequiredMixin, FlavorActionMixin, UpdateView):
    success_msg = "updated"
    # Explicitly attach the FlavorForm class
    form_class = FlavorForm

class FlavorDetailView(DetailView):
    model = Flavor


```
- 이러한 수정사항들고 주목해야하는 것은 12장 챕터 시작에 나온 Flavor model과 지금이 동일하거나, TastyTitleAbstractModel을 상속받은 것으로 부터 변경될 수 있다. (이게 무슨말이지?)

## 12.3 Clean Stage of Validation의 재정의
- 다양한 필드 유효성 검사
- 이미 유효성검사가 완료된 데이터베이스의 기존 데이터의 유효성 검사? (이게 무슨말이지?)
- clean, clean_필드명 함수를 활용해서 custom validation logic 만들기
> 데이터 사용할 경우 cleand_data['필드명'] 으로 접근해서 활용하기
> clean은 2개이상의 필드 서로간의 검증 필요할 때, 특정 필드 검증시에는 clean_필드명

- Tip : 흔한 다양한 필드들에 대한 유효성 검사
1) 처음부터 강화된 비밀번호를 받아라
2) If the email model field isn't set to unique=True, whether or not the email is unique (이게 무슨 말인지?)

## 12.4 Hacking Form Fields (2 CBVs, 2 Forms, 1 Model)

# Example 12.10 Repeated Heavily Duplicated Code
```python
form에서 field 지정하는 방식으로 model Form에서 field 정의하는 방식은 절대로 사용하지마라, 코드의 중복 및 복잡해진다.
```
# __init__ () method를 활용해서 재정의해라.
# 장고 폼도 기본적으로 파이썬 클래스다. 핵심(상속, superclass 활용)

# Don't Use ModelFroms.Meta.exclude.

## 12.5 Reusable Search mixin View

- Single CBV가 2개의 모델에 serach 기능을 추가할 수 있다는 걸 보여주는 좋은 예
- 처음에 Mixin을 만들어서 활용하기




