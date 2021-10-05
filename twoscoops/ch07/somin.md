
## 7. 쿼리와 데이터베이스 계층

- 장고의 object-relational model과 orm은 SQL쿼리 뿐만 아니라 모델에 접근, 업데이트하는 기능도 제공한다.
- 또한 여러 데이터베이스 엔진에서 작동하는 코드를 제공한다
- 장고 orm은 다른 orm처럼 데이터를 지원되는 데이터베이스에서 일관되게 사용할 수 있는 object로 변환한다.

# 7.1 Use get_object_or_404() for single objects
1. 디테일 페이지 같은 view에서는 get()대신 get_object_or_404()를 사용하라
2. views에서만 사용하라

=> 도경님 : api 서버 작성시에는 오류를 날 가능성이 있으니 주의하자! (확인필요)

# 7.2 예외가 발생가능한 쿼리를 주의하라

## 7.2.1 ObjectDoesNotExist vs DoesNotExist
1. ObjectDoesNotExist는 모델 obejct에 적용할 수 있는 것
2. DoesNotExist는 특정 model를 상속받은 메서드에서 적용할 수 있는 것

## 7.2.2 우리는 하나의 object를 원하지만 3개가 리턴되는 경우
1. 이경우 MultipleObjectsReturned 예외를 확인하라
ex) except Flavor.MultipleObjectsReturned:
        예외발생시 수행할 코드
~~~python
def list_flavor_line_item(sku):
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0)
    except Flavor.DoseNotExist:
        msg = 'We are out of {}'.format(sku)
        raise OutOfStock(msg)
    except Flavor.MultipleObjectsReturned:
        msg = 'Multiple items have SKU {}. Please fix!'.format(sku)
        raise CorruptedDatabase(msg)
~~~

# 7.3 쿼리를 알아볼 수 있게 하기 위해 게으른(?) 평가(지연평가)를 사용하라
[x이렇게 하지 마세요x]

~~~python
# 쿼리 체이닝이 화면이나 페이지를 넘지 않도록 하는 것이 좋다.
def ex_function(name=None):
    return Promo.objects.active()
    .filter(Q(name="테스트")|Q(description__icontains=name))
~~~

[o이렇게 하세요o]

~~~python
def ex_function(name=None):
    results = Promo.objects.active()
    results = results.filter(Q(name="테스트")|Q(description__icontains=name))
    results = results.exclude(status='melted')
    results = results.select_related('flavors')
    return results
~~~

1. 게으른(?) 평가에 따르면 장고 ORM은 우리가 실제로 데이터를 사용하지 않을때까지 SQL을 콜하지 않는다.
2. 우리가 사용하고자하는 메서드와 기능들을 여러 줄로 나누면 가독성이 향상되고, 관리의 용이성을 높일 수 있다.

추가적으로 생각해볼 내용 : reverse_lazy

# 7.3.1 가독성을 위한 쿼리

- PDB(Python Debugger) => python 표준 라이브러리, 대화형 디버거
- IPDB(IPython-enabled Python Debugger

# 7.4 발전된 쿼리 툴을 사용
- python으로 데이터를 관리하는 대신 Django의 쿼리 툴을 사용하자
- 모든 데이터베이스가 python보다 빠르게 데이터를 관리하고 변환할 수 있기 때문!
- python을 사용하여 db의 모든 레코드를 하나씩 루프하게 되면 느리고, 메모리도 소모하게 된다.

[x 이렇게 하지마세요 x]
~~~python
customers = []
for customer in Customer.objects.iterator():
    if customer.scoops_ordered > customer.store_visits:
        customers.append(customer)
~~~

[o 이렇게 하세요 o]
~~~python
customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
~~~

- http://raccoonyy.github.io/using-django-querysets-effectively-translate/
star_set = Star.objects.all()

# iterator() 메서드는 전체 레코드의 일부씩만 DB에서 가져오므로
# 메모리를 절약할 수 있다.
for star in star_set.iterator():
    print(star.name)


## 7.4.2 DB Functions
upper()
>>> author = Author.objects.annotate(name_upper=Upper('name')).get()
>>> print(author.name_upper)
MARGARET SMITH

lower()
>>> Author.objects.update(alias=Lower(Substr('name', 1, 5)))
1
>>> print(Author.objects.get(name='Margaret Smith').alias)
marga

coalesce()
>>>total_price = cls.objects.filter(created_at__year=year, created_at__month=month).aggregate(total=Coalesce(Sum('price'), 0))['total']
=> 왼쪽부터 인자값을 검사하고 null이 아닌 첫번째 값을 리턴

concat()
>>> author = Author.objects.annotate(
...     screen_name=Concat(
...         'name', V(' ('), 'goes_by', V(')'),
...         output_field=CharField()
...     )
... ).get()
>>> print(author.screen_name)
Margaret Smith (Maggie)

length()
substr()

# 7.5 필요할때까지 Raw SQL을 사용하지 마세요.
- Raw SQL을 작성하게 되면 보안 및 재사용성이 저하됩니다.
- Raw SQL을 사용해야하는 시기는 ? 여러 querySet을 묶는 경우, 대규모 데이터인 경우에는 더 Raw SQL을 쓰는게 더 효율적일 수 있습니다.

# 7.6 필요에 따라 indexes를 추가하세요.
- 모델필드에 db_index=True를 추가하는건 쉽지만 언제 해야하는지 이해해야합니다.
- 인덱스 추가를 고려해야 하는 시기:
    - 모든 쿼리의 10-25%에서 인덱스가 사용되는 경우
    - 실제 데이터에서 우리는 indexing의 결과를 분석할 수 있다.
    - indexing이 얼마나 향상된 결과를 가져오는지 테스트할 수 있다.

# 7.7 처리과정
- orm의 default 처리과정은 호출될 때 모든 쿼리를 자동으로 커밋한다.
- 그래서 create() or update()가 호출될때 마다 즉시 반영된다.
- 이것은 개발을 막 시작한 사람들에게는 쉽게 다가오지만 만약 2개의 수정중 하나의 수정이 성공하고 다른 수정이 실패하면 데이터베이스가 손상될 위험이 있다.
- 이 손상 위험을 해결하기 위해 데이터베이스 트랜잭션을 사용한다.
- 데이터베이스 트랜잭션은 두 개 이상의 업데이트가 단일 작업단위에 포함되는 곳이다.
- 만약 하나의 업데이트가 실패하면 트랜잭션의 모든 업데이트가 롤백된다.

업무에 바로쓰는 SQL 튜닝
- Storage Engine: 사용자가 요청한 SQL 문을 토대로 DB에 저장된 디스크나 메모리에서 필요한 데이터를 가져오는 역할
일반적으로 트랜잭션 발생은 데이터를 처리하는 OLTP(online transaction processing) 환경이 대다수인 만큼 주로 InnoDB 엔진을 사용.
대량의 쓰기 트랜잭션이 발생하면 MyISAM 엔진을 사용.
메모리 데이터를 로드하여 빠르게 읽는 효과를 내려면 Memory 엔진
MySQL 설정이 트랜잭션을 지원하지 않으면 Django는 항상 자동 커밋 모드입니다.
MYSQL 설정이 트랜잭션을 지원한다면 앞서 언급한 대로 트랜잭션을 처리합니다.


## 7.7.1 Wrapping Each HTTP Request in a Transaction
~~~python
DATABASES = {
    'default': {
    # ...
    'ATOMIC_REQUESTS': True,
    },
}
~~~
- 위의 처럼 설정을 해주면 모든 요청이 래핑된다.
- 모든 데이터베이스 쿼리가 보호되므로 성능이 저하되는 단점이 있다.
- ATOMIC_REQUESTS를 사용하면 에러가 있을시 데이터베이스 상태가 롤백된다.

# 7.8 요약
- 인덱스를 사용했을때 데이터의 작동방식이 더 좋아진다면 인덱스를 사용하는 걸 추천합니다.
