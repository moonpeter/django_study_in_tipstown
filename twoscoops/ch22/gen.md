# Chap22. Dealing With the User Model(Django의 사용자 모델 다루기)

## 22.1 Use Django's Tools for Finding the UserModel

사용자 클래스를 찾는 방법

```python
# 기존 사용자 모델의 정의
>>> from django.contrib.auth import get_user_model 
>>> get_user_model()
<class django.contrib.auth.models.User>

# 프로젝트에서 커스텀 사용자 모델 정의를 이용할 때
>>> from django.contrib.auth import get_user_model 
>>> get_user_model()
<class profiles.models.UserProfile>
```

프로젝트설정에 따라 다른 두 개의 User 모델이 존재할 수 있고, User 모델은 커스터마이징이 가능하다는 의미입니다.

### 22.1.1 Use `settings.AUTH_USER_MODEL` for Foreign Keys to User

```python
from django.conf import settings
from django.db import models

class IceCreamStore(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
```

프로젝트가 셋팅되었다면 `settings.AUTH_USER_MODEL`을 수정하지 말자.

수정하려면 DB 스키마를 아에 맞게 수정해야만 합니다.

### 22.1.2 Don't Use `get_user_model()` for Foreign Keys to User

외래키에 `get_user_model()`을 사용하면 임포트 루프가 발생할 수 있습니다.

```python
# Don't Do This!!
from django.contrib.auth import get_user_model
from django.db import models

class IceCreamStore(models.Model):
    owner = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
```

## 22.2 Custom User Fields for Django Projects

규칙에 맞게 필요한 메서드와 속성을 구현하여 커스텀 유저 모댈을 생성할 수 있습니다.

[`django-authtools`](https://github.com/fusionbox/django-authtools)는 커스텀 사용자 모델을 더 쉽게 정의하는 라이브러리입니다. `AbstractEmailUser`, `AbsteactNameUser` 모델을 이용합니다. Django 3.x에서는 지원하지 않지만, 한 번 살펴볼 가치는 있습니다.

### 22.2.1 Option1: Subclass AbstractUser

Django의 User 모델을 그대로 유지하면서 몇몇 필드를 추가할때 사용합니다.

```python
# profiles/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class KarmaUser(AbstractUser):
    karma = models.PositiveIntegerField(verbose_name='karma',
        default=0, blank=True)
```

해당 모델을 사용하려면 settings에 추가 설정을 해주어야 합니다.

```python
AUTH_USER_MODEL = 'profiles.KarmaUser'
```

### 22.2.2 Option2: Subclass AbstactBaseUser

`password`, `last_login`, `is_active` 필드만 가진 기본 형태의 옵션입니다.

> `is_active` 는 생성되지 않네요.

- User 모델이 기본으로 제공하는 필드(`first_name`, `last_name`)에 만족하지 못할 때
- 기본 형태만 가진 가벼운 상태로부터 새로 서브 클래스를 생성하면서, 패스워드를 저장하기 위해 `AbstractBaseUser`의 기본 환경의 장점을 이용하고 싶을 때
- [https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#a-full-example](https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#a-full-example)
- https://github.com/fusionbox/django-authtools

### 22.2.3 Option3: Linking Back Form a Related Model
관련 모델로부터 역으로 링크하기 

- 이용사례: 서드 파티 패키지 제작
    - PyPI에 올릴 서드 파티 애플리케이션을 제작할 때
    - 사용자당 추가로 저장해야 할 정보가 있을 때
    - 최대한 느슨한 연관된 관계를 원할 때
- 이용사례: 내부적으로 필요한 경우
    - 우리만의 Django 프로젝트를 작업할 때
    - 각기 다른 필드를 가진 전혀 다른 사용자 타입을 원할 때
    - 사용자 중 일부가 다른 사용자 타입을 가지는 사용자들과 섞여 있을 때
    - 다른 레벨단이 아닌 모델 레벨에서 모든 것을 처리하고 싶을 때
    - 옵션1, 2애서 다룬 커스텀 사용자 모델과 결합하여 이용하고 싶을 때

```python
# profiles/models.py
from django.conf import settings
from django.db import models
from flavors.models import Flavor

class EaterProfile(models.Model):
    # 기존 사용자 프로필
    # 이러한 방식을 이용한다면 post_save 시그널이나
    # 최초 로그인시 profile_edit 뷰로 리다이렉트하는 절차가 필요하다.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    favorite_ice_cream = models.ForeignKey(Flavor, null=True, blank=True)

class ScooperProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    scoops_scooped = models.IntegerField(default=0)

class InventorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    flavors_invented = models.ManyToManyField(Flavor, null=True, blank=True)
```

ORM(`user.eaterprofile.favorite_ice_cream`)을 통해 손쉽게 역으로 정보를 가져올 수 있습니다.  
Scooper, Inventor 역시 해당 사용자에게만 해당하는 개인 데이터를 제공할 수 있습니다.  
이렇게 구성하면 사용자 모델과는 독립된 정보이기 때문에 사용자 타입 사이에서 문제가 발행될 확률이 **매우 낮아진다.**


프로파일이나 그와 관련된 파일들이 너무 단순해져버릴 수 있지만, 코드를 단순하게 유지하는 것이 꼭 단점이자 장점이 될 수도 있습니다.

## 22.3 Handling Multiple User Types

여러 사용자 유형(직원, 관리자, 일반 사용자 등)을 처리할 때는, 하나의 모델을 사용하고 적절히 표시만 해주면 됩니다.

### 22.3.1 Add a User Type Field

User 모델에 사용자 유형을 구분하는 필드를 추가합니다.

```python
class User(AbstractUser):
    class Types(models.TextChoices):
        EATER = "EATER", "Eater"
        SCOOPER = "SCOOPER", "Scooper"
        INVENTOR = "INVENTOR", "Inventor"

    type = models.CharField(
        _("Type"), max_length=50,
        choices=Types.choices, default=Types.EATER
        )
```

시간의 지남에 따라 사이트의 크기와 복잡성의 증가하기 때문에 유형 구분을 위한 필드에 boolean보다는 char의 단일 필드를 상하는 것이 좋습니다.

 사용자가 여러 역할을 가져야 한다면 `ManyToManyField`를 이용하거나 Django의 내장 그룹 시스템을 이용하세요.

### 22.3.2 Add a User Type Field Plus Proxy Models

다른 유형의 사용자는 다른 메서드와 속성을 가집니다.

프록시 모델을 사용하면 쉽게 구현할 수 있습니다.

```python
class User(AbstractUser):
    class Types(models.TextChoices):
        EATER = "EATER", "Eater"
        SCOOPER = "SCOOPER", "Scooper"
        INVENTOR = "INVENTOR", "Inventor"

    # 프록시 모델을 통해 새로운 사용자가 생성되는지 확인
    base_type = Types.EATER

    type = models.CharField(
        _("Type"), max_length=50,
        choices=Types.choices,
        default=Types.EATER
        )

    def save(self, *args, **kwargs):
        # 신규 사용자라면, base_type을 기반으로 유형을 지정
        if not self.pk:
            self.type = self.base_type
        return super().save(*args, **kwargs)
```

```python
# users/models.py
class InventorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=User.Types.INVENTOR)

class Inventor(User):
    # 사용자 유형을 INVENTOR으로 설정
    base_type = User.Types.INVENTOR
    # Inventor 모델에 대한 쿼리가 Inventors만 반환하는지 확인
    objects = InventorManager()

    # True이면 이 레코드에 대한 테이블을 생성하지 않음
    class Meta:
        proxy = True

    def invent(self):
        return "Delicious!"
```

프록시 모델은 필드를 추가하지 않습니다.

프록시 모델은 커스텀 매니저, 메서드, 속성을 걸 수 있는 모델 개체에 대한 참조입니다.

```bash
>>> from users.models import User, Inventor
>>> User.objects.count() # Over 300 million users! 323482357
>>> Inventor.objects.count() # But only 3 inventors 3

# Calling someone as both a User and an Inventor
>>> user = User.objects.get(username='uma')
>>> user
<User: uma>
>>> inventor = Inventor.objects.get(username='uma')
>>> inventor
<Inventor: uma>

# Calling a method that's only for inventors
>>> user.invent()
AttributeError
>>> inventor.invent()
'Delicious'
```

프록시 접근 방식은 `django.contrib.auth` 를 극적으로 확장하지 않고, 새로운 사용자 테이블을 생성하거나 타사 라이브러리를 사용하지 않고도 여러 유형의 사용자를 제공합니다.

프록시 모델이 자체 모델 매니저를 가질수 있다는 것은 더 많은 명시적 쿼리를 가질 수 있다는 것을 의미합니다.

```bash
>>> User.objects.filter(type=User.Types.INVENTOR)
>>> Inventor.objects.filter()  # Our preference
```

### 22.3.3 Adding Extra Data Fields

다양한 유형의 사용자의 추가 데이터 필드를 처리하는 방법입니다.

1. `OneToOneField` 관계를 프로파일 모델에 사용
    - [Chap22.2.3: Option 3: Linking Back From a Related Model]()


2. 모든 필드에 기본 User 모델을 넣습니다.
    - User 테이블이 느려질 수 있음
    - 사용하지도 않는 데이터들을 보관하게 될 수도 있음

```python
class Inventor(User):
    objects = InventorManager()

    class Meta:
        proxy = True

    @property
    def extra(self):
        return self.inventorprofile

class Scooper(User):
    objects = ScooperManager()

    class Meta:
        proxy = True

    @property
    def extra(self):
        return self.scooperprofile

class Eater(User):
    objects = EaterManager()

    class Meta:
        proxy = True

    @property
    def extra(self):
        return self.eaterprofile
```

User 유형에 관계없이 일대일 관계의 프로필에 액세스할 수 있습니다.

- `invented.extra.flavors_invented`
- `scooper.extra.scoops_scooped`
- `eater.extra.favorite_ice_cream`

### 22.3.4 Additional Resources on Multiple User Types

- [https://www.youtube.com/watch?v=f0hdXr2MOEA](https://www.youtube.com/watch?v=f0hdXr2MOEA)
- [https://docs.djangoproject.com/en/3.1/topics/db/models/#proxy-models](https://docs.djangoproject.com/en/3.1/topics/db/models/#proxy-models)
- [https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html](https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html)

## 22.4 Summary

- Custom User Model을 정의하는 방법
- 프록시 모델
