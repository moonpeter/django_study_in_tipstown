# 26  Finding and Reducing Bottlenecks



>  This chapter covers a few basic strategies for identifying bottlenecks and speeding up your Django projects.

이 장에서는 병목 현상을 식별하고  Django 프로젝트의 속도를 높이는 몇가지 기본 전략을 다룹니다. 



## 26.1 Should You Even Care?(신경써야 합니까?)

> Remember, premature optimization is bad. 
> If your site is small- or medium-sized and the pages are loading fine, then it’s okay to skip this chapter

조기 최적화는 좋지 않다는 것을 기억하십시오.
당신의 사이트가 `중소 규모`이고 페이지가 제대로 로드되면 이장을 건너 뛰어도  됩니다.



## 26.2 Speed Up Query-Heavy Page (쿼리 처리량이 많은 페이지 속도 향상)

> This section describes how to reduce bottlenecks caused by having too many queries, 
> as well as those caused by queries that aren’t as snappy as they could be.

이 섹션에서는 너무 많은 쿼리로 인해 발생하는 병목 현상을 줄이는 방법뿐만 아니라
그렇게 간단하지 않은 쿼리로 인해 발생하는 병목 현상을 줄이는 방법에 대해 설명합니다.

> We also urge you to read up on database access optimization in the official Django docs:
> docs.djangoproject.com/en/3.2/topics/db/optimization/

또한 공식 Django 문서에서 `데이터베이스 액세스 최적화`에 대해 자세히 읽어보시기 바랍니다.
[docs.djangoproject.com/en/3.2/topics/db/optimization/](docs.djangoproject.com/en/3.2/topics/db/optimization/)



### 26.2.1 Find Excessive Queries With Django Debug Toolbar

### (Django 디버그 도구 모음을 사용하여 과도한 쿼리 찾기)

> You can use django-debug-toolbar to help you determine where most of your queries are coming from. 
> You’ll find bottlenecks such as:
> ➤ Duplicate queries in a page. 
> ➤ ORM calls that resolve to many more queries than you expected.
> ➤ Slow queries.

`django-debug-toolbar`를 사용하여 대부분의 쿼리가 어디서 오는지 확인할 수 있습니다.

다음과 같은 병목 현상을 발견할 수 있습니다.
➤ 페이지 내 중복 조회.
➤ ORM 호출을 통해 예상보다 더 많은 쿼리를 해결 할 수 있습니다.
➤ 느린 질의



> You probably have a rough idea of some of the URLs to start with.
> For example, which pages don’t feel snappy when they load?


당신은 아마도 시작할 URL들 중 일부를 대략적으로 알고 있을 것입니다.
예를 들어, 어떤 페이지가 로드될 때 매끄럽지 않게 느껴지나요?



> Install `django-debug-toolbar` locally if you don’t have it yet.
> Look at your project in a web browser, and expand the SQL panel.
> It’ll show you how many queries the current page contains.

아직 `django-debug-toolbar`가 없다면 로컬에 설치하세요.
웹 브라우저에서 프로젝트를 보고 SQL 패널을 확장합니다.
현재 페이지에 포함된 쿼리 수가 표시됩니다.

---

##### PACKAGE TIP : Packages for Profiling and Performance Analysis
##### (프로파일링 및 성능 분석을 위한 패키지)

> `django-debug-toolbar` is a critical development tool and an invaluable aid in page-by-page analysis. 
> We also recommend adding django-cache-panel to your project, but only configured to run when settings/local.py module is called. 
> This will increase visibility into what your cache is doing.

`django-debug-toolbar` 는 중요한 개발 도구이자 페이지별 분석에 있어 매우 유용한 도구입니다.
또한 프로젝트에 `django-cache-panel`을 추가하는 것이 좋지만 settings/local.py 모듈이 호출될 때만 실행되도록 구성되어 있습니다.
이렇게 하면 캐시가 수행하는 작업에 대한 가시성이 향상됩니다.



> `django-extensions` comes with a tool called `RunProfileServer` that starts Django’s runserver command with hotshot/profiling tools enabled.

`django-extensions`는 `hotshot/profiling` 도구가 활성화된 상태에서 Django의 runserver 명령을 시작하는 `RunProfileServer`라는 도구와 
함께 제공됩니다.



> silk ([github.com/mtford90/silk](github.com/mtford90/silk)) Silk is a live profiling Django app that intercepts and stores HTTP requests and database queries before presenting them in a user interface for further inspection.

실크는 HTTP 요청과 데이터베이스 쿼리를 인터셉트하고 저장한 후 추가 검사를 위해 사용자 인터페이스에 표시하는 라이브 프로파일링 Django 앱입니다.



---



### 26.2.2 Reduce the Number of Queries (쿼리 수 줄이기)

> Once you know which pages contain an undesirable number of queries, figure out ways to reduce that number.
> Some of the things you can attempt:

바람직하지 않은 수의 질의가 포함된 페이지를 파악한 후 해당 수를 줄일 수 있는 방법을 모색하십시오.
시도할 수 있는 몇 가지 방법은 다음과 같습니다.

> ➤ Try using select_related() in your ORM calls to combine queries. 
> It follows ForeignKey relations and combines more data into a larger query. 
> If using CBVs, django-braces makes doing this trivial with the SelectRelatedMixin.
> Beware of queries that get too large by explicitly passing the related field names you are interested in.
> Only the specified relations will be followed. Combine that with careful testing!

ORM 호출에서 `select_related()`를 사용하여 쿼리를 결합해 보십시오.
`ForeignKey` 관계를 따르며 더 많은 데이터를 더 큰 쿼리로 결합한다.
`CBV`를 사용할 경우, `django-braces`는 `SelectRelatedMixin`을 사용하여 이 작업을 간단하게 만듭니다.
관심 있는 관련 필드 이름을 명시적으로 전달하여 너무 커지는 쿼리에 주의하십시오.
지정된 관계만 따릅니다. 세심한 테스트와 결합하세요!

> ➤ For `many-to-many` and `many-to-one` relationships that can’t be optimized with `select_related()`,
> explore using `prefetch_related()` instead.

`select_related()`로 최적화할 수 없는 `다-대-다` 및 `다-대-일` 관계인 경우 대신 `prefetch_related()`를 사용하여 탐색합니다.



> ➤ If the same query is being generated more than once per template, move the query into the Python view, 
> add it to the context as a variable, and point the template ORM calls at this new context variable.

동일한 쿼리가 템플릿당 두 번 이상 생성되는 경우 쿼리를 `Python View`로 이동하고 
컨텍스트에 변수로 추가하고 템플릿 ORM 호출이 이 새 컨텍스트 변수를 가리키도록 합니다.



> ➤ Implement caching using a key/value store such as Memcached or Redis. 
> Then write tests to assert the number of queries run in a view.
> See docs.djangoproject.com/en/3.2/topics/testing/tools/#django.
> test.TransactionTestCase.assertNumQueries for instructions.

`Memcached` 또는 `Redis`와 같은 `키/값 저장소`를 사용하여 `캐싱`을 구현합니다.
그런 다음 보기에서 실행되는 쿼리 수를 나타내는 테스트를 작성합니다.

[docs.djangoproject.com/en/3.2/topics/testing/tools/#django](docs.djangoproject.com/en/3.2/topics/testing/tools/#django) 의
`test.TransactionTestCase.assertNumQueries` 지침을 참고 하십시오.



> ➤ Use the django.utils.functional.cached_property decorator to cache in memory the result of method call for the life of an object instance. 
> This is incredibly useful, so please see Section 31.3.5: django.utils.functional.cached_property in chapter 31.

`django.utils.functional.cached_property` 데코레이터를 사용하여 객체 인스턴스의 수명 동안 메서드 호출 결과를 메모리에 캐시합니다.



### 26.2.3 Speed Up Common Queries

> The length of time it takes for individual queries can also be a bottleneck. 
> Here are some tips, but consider them just starting points:

개별 쿼리에 걸리는 시간도 병목 현상이 될 수 있습니다.
다음은 몇 가지 팁이지만 시작점에 불과하다고 생각하십시오.



> ➤ Make sure your indexes are helping speed up your most common slow queries.
> Look at the raw SQL generated by those queries, and index on the fields that you filter/sort on most frequently.
> Look at the generated WHERE and ORDER_BY clauses.

인덱스가 가장 일반적인 느린 쿼리 속도를 높이는 데 도움이 되는지 확인합니다.
해당 쿼리에 의해 생성된 원시 SQL을 살펴보고 가장 자주 필터링/정렬하는 필드에 대한 색인을 생성하십시오.
생성된 WHERE 및 ORDER_BY 절을 보십시오.



> ➤ Understand what your indexes are actually doing in production.
> Development machines will never perfectly replicate what happens in production, 
> so learn how to analyze and understand what’s really happening with your database.

인덱스가 프로덕션에서 실제로 수행하는 작업을 이해합니다.
개발 머신은 프로덕션에서 일어나는 일을 완벽하게 복제할 수 없으므로 데이터베이스에서 실제로 일어나는 일을 분석하고 이해하는 방법을 배우십시오.



> ➤ Look at the query plans generated by common queries.

일반적인 쿼리에 의해 생성된 쿼리 계획 살펴보기



> ➤  Turn on your database’s slow query logging feature and see if any slow queries occur frequently.

데이터베이스의 느린 질의 기록 기능을 설정하고 느린 질의가 자주 발생하는지 확인합니다.



> ➤ Use django-debug-toolbar in development to identify potentially-slow queries defensively, before they hit production.

개발 단계에서 `django-debug-toolbar`를 사용하여 잠재적으로 느린 쿼리가 프로덕션에 도달하기 전에 방어적으로 식별합니다.



> Once you have good indexes, and once you’ve done enough analysis to know which queries
> to rewrite, here are some starting tips on how to go about rewriting them:

좋은 인덱스가 있고 분석을 충분히 수행하여 어떤 쿼리를 파악한 경우
다시 작성하기 위해 다시 작성하는 방법에 대한 몇 가지 시작 팁이 있습니다.



> 1 Rewrite your logic to return smaller result sets when possible.
>
> 2 Re-model your data in a way that allows indexes to work more effectively.
>
> 3 Drop down to raw SQL in places where it would be more efficient than the generated query.

가능한 경우 더 작은 결과 집합을 반환하도록 로직을 다시 작성합니다.

인덱스가 보다 효과적으로 작동할 수 있도록 데이터를 다시 모델링하십시오.

생성된 쿼리보다 더 효율적인 위치에서 원시 SQL로 드롭다운합니다.



---

#### TIP: Use EXPLAIN ANALYZE / EXPLAIN

팁: 실행계획 분석 / 실행계획 사용

> If you’re using PostgreSQL, you can use EXPLAIN ANALYZE to get an extremely detailed query plan and analysis of any raw SQL query. 
> For more information, see:
> ➤ [revsys.com/writings/postgresql-performance.html](https://www.revsys.com/writings/postgresql-performance.html)
> ➤ [craigkerstiens.com/2013/01/10/more-on-postgres-performance/](https://www.craigkerstiens.com/2013/01/10/more-on-postgres-performance/)

PostgreSQL을 사용하는 경우 EXPLAIN ANALYZE를 사용하여 원시 SQL 쿼리에 대한 매우 상세한 쿼리 계획 및 분석을 얻을 수 있습니다.

자세한 내용은 다음을 참조하세요.
➤ [revsys.com/writings/postgresql-performance.html](https://www.revsys.com/writings/postgresql-performance.html)
➤ [craigkerstiens.com/2013/01/10/more-on-postgres-performance/](https://www.craigkerstiens.com/2013/01/10/more-on-postgres-performance/)



> The MySQL equivalent is the EXPLAIN command, which isn’t as detailed but is still helpful.
> For more information, see:
> ➤ [dev.mysql.com/doc/refman/5.7/en/explain.html](dev.mysql.com/doc/refman/5.7/en/explain.html)

이에 상응하는 MySQL은 EXPLAIN 명령으로, 상세하지는 않지만 여전히 유용합니다. 
자세한 내용은 다음을 참조하세요.
➤ [dev.mysql.com/doc/refman/5.7/en/explain.html](dev.mysql.com/doc/refman/5.7/en/explain.html)



> A nice feature of django-debug-toolbar is that the SQL pane has an EXPLAIN feature

`django-debug-toolbar`의 좋은 기능은 SQL 창에 EXPLAIN 기능이 있다는 것입니다.

---



### 26.2.4 Switch ATOMIC_REQUESTS to False

`ATOMIC_REQUESTS`를 False로 전환: Default True

> The clear, vast majority of Django projects will run just fine with the setting of ATOMIC_REQUESTS to True.
> Generally, the penalty of running all database queries in a transaction isn’t noticeable.
> However, if your bottleneck analysis points to transactions causing too much delay,
> it’s time to change the project run as ATOMIC_REQUESTS to False. 
> See Section 7.7.2: Explicit Transaction Declaration for guidelines on this setting.

명확하고 대다수의 Django 프로젝트는 `ATOMIC_REQUESTS`를 True로 설정하면 잘 실행됩니다.
일반적으로 트랜잭션에서 모든 데이터베이스 쿼리를 실행하는 데 따른 패널티는 눈에 띄지 않습니다.
그러나 병목 현상 분석에서 너무 많은 지연을 일으키는 트랜잭션이 지적되면,
`ATOMIC_REQUESTS`로 실행되는 프로젝트를 `False`로 변경할 때입니다.
이 설정에 대한 지침은 섹션 7.7.2: 명시적 트랜잭션 선언을 참조하십시오.



## 26.3 Get the Most Out of Your Database

데이터베이스를 최대한 활용하십시오.

> You can go a bit deeper beyond optimizing database access. 
> Optimize the database itself!
> Much of this is database-specific and already covered in other books, so we won’t go into too much detail here.

데이터베이스 액세스를 최적화하는 것 이상으로 더 깊이 들어갈 수 있습니다.
데이터베이스 자체를 최적화하십시오!
이 중 대부분은 데이터베이스에 고유하며 이미 다른 책에서 다루었으므로 여기에서 너무 자세히 설명하지 않겠습니다.



### 26.3.1 Know What Doesn’t Belong in the Database

데이터베이스에서 속하지 않는 항목을 파악합니다.

> Frank Wiles of Revolution Systems taught us that there are two things that should never go into any large site’s relational database:

레볼루션 시스템의 Frank Wiles는 어떤 대규모 사이트의 관계형 데이터베이스에도 들어가지 말아야 할 두 가지가 있다고 우리에게 가르쳤다.



> Logs. 
> Don’t add logs to the database.
> Logs may seem OK on the surface, especially in development.
> Yet adding this many writes to a production database will slow their performance.
> When the ability to easily perform complex queries against your logs is necessary, 
> we recommend third-party services such as Splunk or Loggly, or use of document-based NoSQL databases.

`로그`. 
데이터베이스에 로그를 추가하지 마십시오.
로그는 특히 개발 단계에서 표면적으로는 괜찮아 보일 수 있습니다.
그러나 프로덕션 데이터베이스에 이렇게 많은 쓰기를 추가하면 성능이 저하됩니다.
로그에 대해 복잡한 쿼리를 쉽게 수행할 수 있는 기능이 필요한 경우 Splunk 또는 Loggly와 같은 타사 서비스나 
문서 기반 NoSQL 데이터베이스 사용을 권장합니다.



> Ephemeral data. 
> Don’t store ephemeral data in the database.
> What this means is data that requires constant rewrites is not ideal for use in relational databases.
> This includes examples such as django.contrib.sessions, django.contrib.messages, and metrics. 
> Instead, move this data to things like Memcached, Redis, and other non-relational stores.

`임시 데이터.`
임시 데이터를 데이터베이스에 저장하지 마십시오. 
이것이 의미하는 바는 지속적인 재작성이 필요한 데이터는 관계형 데이터베이스에서 사용하기에 이상적이지 않다는 것입니다.
여기에는 `django.contrib.sessions`, `django.contrib.messages` 및 메트릭과 같은 예제가 포함됩니다.
대신 이 데이터를 Memcached, Redis 및 기타 비관계형 저장소로 이동하세요.







---

### TIP: Frank Wiles on Binary Data in Databases

데이터베이스의 이진 데이터에 대한 Frank Wiles

> Actually, Frank says that there are three things to never store in a database, the third item being binary data. 
> Storage of binary data in databases is addressed by django.db.models.FileField, which does the work of storing files on file servers like AWS CloudFront or S3 for you.
> Exceptions to this are detailed in Section 6.4.5: When to Use BinaryField.

사실, 프랭크는 데이터베이스에 절대 저장하지 말아야 할 세 가지가 있다고 말합니다, 세 번째 항목은 이진 데이터입니다.
데이터베이스에 있는 이진 데이터의 저장은 `django.db.models`에 의해 처리된다.
`FileField`는 `AWS CloudFront` 또는 `S3`와 같은 파일 서버에 파일을 저장하는 작업을 수행합니다.
이에 대한 예외는 섹션 6.4.5: BinaryField 사용 시기에 자세히 설명되어 있습니다.

---



### 26.2.2 Getting the Most Out of PostgreSQL

PostgreSQL 최대한 활용하기

> If using PostgreSQL, be certain that it is set up correctly in production. 
> As this is outside the scope of the book, we recommend the following articles:

`PostgreSQL`을 사용하는 경우 프로덕션에서 올바르게 설정되었는지 확인하십시오.
이것은 책의 범위를 벗어나므로 다음 기사를 권장합니다.

➤ [wiki.postgresql.org/wiki/Detailed_installation_guides](wiki.postgresql.org/wiki/Detailed_installation_guides)
➤ [wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server]() 
➤ [revsys.com/writings/postgresql-performance.html]() 
➤ [craigkerstiens.com/2012/10/01/understanding-postgres-performance]() 
➤ [craigkerstiens.com/2013/01/10/more-on-postgres-performance]()



### 26.3.3 Getting the Most Out of MySQL

MySQL 최대한 활용하기

> It’s easy to get MySQL running, but optimizing production installations requires experience and understanding.
> As this is outside the scope of this book, we recommend the following links to help you:

MySQL을 실행하는 것은 쉽지만 프로덕션 설치를 최적화하려면 경험과 이해가 필요합니다.
이것은 이 책의 범위를 벗어나므로 다음 링크를 사용하는 것이 좋습니다.

TODO - list good resources



## 26.4 Cache Queries With Memcached or Redis

Memcached 또는 Redis를 사용한 캐시 쿼리



> You can get a lot of mileage out of simply setting up Django’s built-in caching system with Memcached or Redis.
> You will have to install one of these tools, install a package that provides Python bindings for them, and configure your project.

Memcached 또는 Redis로 Django의 내장 캐싱 시스템을 설정하기만 하면 많은 마일리지를 얻을 수 있습니다.
이러한 도구 중 하나를 설치하고, 이에 대한 Python 바인딩을 제공하는 패키지를 설치하고, 프로젝트를 구성해야 합니다.

> You can easily set up the per-site cache, or you can cache the output of individual views or template fragments.
> You can also use Django’s low-level cache API to cache Python objects.

사이트별 캐시를 쉽게 설정하거나 개별 보기 또는 템플릿 조각의 출력을 캐시할 수 있습니다.
또한 Django의 로우 레벨 캐시 API를 사용하여 Python 개체를 캐시할 수 있습니다.

Reference material:

➤ [docs.djangoproject.com/en/3.2/topics/cache/]() 
➤ [github.com/niwinz/django-redis]()



## 26.5 Identify Specific Places to Cache

캐시할 특정 위치 식별

> Deciding where to cache is like being first in a long line of impatient customers at Ben and Jerry’s on free scoop day. 
> You are under pressure to make a quick decision without being able to see what any of the flavors actually look like.

캐시를 어디에 둘지 결정하는 것은 마치 무료 아이스크림 날에 벤과 제리의 긴 줄에 서 있는 참을성 없는 손님들 중 첫 번째가 되는 것과 같다.
당신은 어떤 맛도 실제로 어떻게 생겼는지 볼 수 없는 상태에서 빠른 결정을 내려야 하는 압박을 받고 있다.



> Here are things to think about:
> ➤ Which views/templates contain the most queries?
> ➤ Which URLs are being requested the most?
> ➤ When should a cache for a page be invalidated?
> Let’s go over the tools that will help you with these scenarios.

생각해 볼 사항은 다음과 같습니다.
➤ 어떤 View/템플릿에 가장 많은 쿼리가 포함되어 있습니까?
➤ 가장 많이 요청되는 URL은 무엇입니까?
➤ 페이지의 캐시는 언제 무효화해야 합니까?
이러한 시나리오에 도움이 되는 도구를 살펴보겠습니다.



## 26.6 Consider Third-Party Caching Packages

타사 캐싱 패키지 고려

> Third-party packages will give you additional features such as:
> ➤ Caching of QuerySets.
> ➤ Cache invalidation settings/mechanisms.
> ➤ Different caching backends.
> ➤ Alternative or experimental approaches to caching.

타사 패키지는 다음과 같은 추가 기능을 제공합니다.
➤ QuerySet의 캐싱.
➤ 캐시 무효화 설정/메커니즘.
➤ 다양한 캐싱 백엔드.
➤ 캐싱에 대한 대안 또는 실험적 접근 방식.



> A few of the popular Django packages for caching are:
> ➤ django-cacheops
> ➤ django-cachalot

캐싱을 위한 몇 가지 인기 있는 Django 패키지는 다음과 같습니다.
➤ [django-cacheops](https://github.com/Suor/django-cacheops)
➤ [django-cachalot](https://django-cachalot.readthedocs.io/en/latest/introduction.html)

> See [djangopackages.org/grids/g/caching/](https://djangopackages.org/grids/g/caching/) for more options.



---

### WARNING: Third-Party Caching Libraries Aren’t Always the Answer

타사 캐싱 라이브러리가 항상 정답은 아닙니다.

> Having tried many of the third-party Django cache libraries, 
> we have to ask our readers to test them very carefully and be prepared to drop them. 

많은 타사 Django 캐시 라이브러리를 사용해 본 결과 독자들에게 매우 신중하게 테스트하고 삭제할 준비를 하도록 요청해야 합니다.

> They are cheap, quick wins, but can lead to some hair-raising debugging efforts at the worst possible times.

그것들은 저렴하고 빠른 승리를 거두지만, 최악의 시기에 디버깅 노력을 과도하게 끌어올릴 수 있습니다.

___



## 26.7 Compression and Minification of HTML, CSS  and JavaScript

HTML, CSS 및 JavaScript의 압축 및 축소

> When a browser renders a web page, it usually has to load HTML, CSS, JavaScript, and image files.
> Each of these files consumes the user’s bandwidth, slowing down page loads. 
> One way to reduce bandwidth consumption is via compression and minification.
> Django even provides tools for you: GZipMiddleware and the {% spaceless %} template tag.
> Through the at-large Python community, we can even use WSGI middleware that performs the same task.

브라우저가 웹 페이지를 렌더링할 때 일반적으로 HTML, CSS, JavaScript 및 이미지 파일을 로드해야 합니다.
이러한 각 파일은 사용자의 대역폭을 소모하여 페이지 로드를 늦춥니다.
대역폭 소비를 줄이는 한 가지 방법은 압축 및 축소를 사용하는 것입니다.
Django는 [GZipMiddleware](https://docs.djangoproject.com/ko/2.1/_modules/django/middleware/gzip/) 및 [{% spaceless %} 템플릿 태그](https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#spaceless)와 같은 도구도 제공합니다.
`at-large` Python 커뮤니티를 통해 동일한 작업을 수행하는 WSGI 미들웨어를 사용할 수도 있습니다.



> The problem with making Django and Python do the work is that compression and minification take up system resources, 
> which can create bottlenecks of their own.
> A better approach is to use Nginx or Apache web servers configured to compress the outgoing content. 
> If you are maintaining your own web servers, this is absolutely the way to go.

Django와 Python이 작업을 수행할 때의 문제는 압축 및 축소가 시스템 리소스를 차지하여 자체적으로 병목 현상을 일으킬 수 있다는 것입니다.
더 나은 접근 방식은 나가는 콘텐츠를 압축하도록 구성된 `Nginx` 또는 `Apache` 웹 서버를 사용하는 것입니다.
자신의 웹 서버를 유지 관리하는 경우 이것이 절대적으로 필요한 방법입니다.



> A common approach is to use a third-party compression module or Django library to compress and minify the HTML, CSS, and JavaScript in advance. Our preference is [django-pipeline](https://django-pipeline.readthedocs.io/en/latest/) which comes recommended by Django core developer Jannis Leidel.
>

일반적인 접근 방식은 타사 압축 모듈 또는 Django 라이브러리를 사용하여 HTML, CSS 및 JavaScript를 미리 압축하고 축소하는 것입니다.
우리가 선호하는 것은 Django 핵심 개발자 Jannis Leidel이 권장하는 [django-pipeline](https://django-pipeline.readthedocs.io/en/latest/)입니다.



> For CSS and JavaScript, most people use JavaScript-powered tools for minification. 
> Tools like `django-webpack-loader` manage the JavaScript libraries within the Django context.
> The advantage of this approach is the greater mindshare of tools and solved problems in this domain space.

CSS 및 JavaScript의 경우 대부분의 사람들은 축소를 위해 JavaScript 기반 도구를 사용합니다.
[django-webpack-loader](https://pypi.org/project/django-webpack-loader/)와 같은 도구는 Django 컨텍스트 내에서 JavaScript 라이브러리를 관리합니다.
이 접근 방식의 이점은 툴의 마인드셰어를 높인다는 것 그리고, 이 도메인 공간의 문제를 해결하는 것입니다.

> Tools and libraries to reference:
> ➤ Apache and Nginx compression modules
> ➤ django-webpack-loader
> ➤ django-pipeline
> ➤ django-compressor
> ➤ django-htmlmin
> ➤ Django’s built-in spaceless tag: [docs.djangoproject.com/en/3.2/ref/templates/builtins/spaceless](https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#spaceless)
> ➤ [djangopackages.org/grids/g/asset-managers/](https://djangopackages.org/grids/g/asset-managers/)



## 26.8 Use Upstream Caching or a Content Delivery Network

[업스트림](https://ko.wikipedia.org/wiki/%EC%97%85%EC%8A%A4%ED%8A%B8%EB%A6%BC_(%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC)) 캐싱 또는 콘텐츠 전송 네트워크 사용

> Upstream caches such as Varnish are very useful. 
> They run in front of your web server and speed up web page or content serving significantly. 
> See varnish-cache.org.

Varnish와 같은 업스트림 캐시는 매우 유용합니다.
웹 서버 앞에서 실행되며 웹 페이지 또는 콘텐츠 제공 속도를 크게 높입니다.
[varnish-cache.org](https://varnish-cache.org/intro/index.html#intro)를 참조하십시오.



> Content Delivery Networks (CDNs) like Fastly, Akamai, and Amazon Cloudfront serve static media such as images, video, CSS, and JavaScript files.
> They usually have servers all over the world, which serve out your static content from the nearest location. 
> Using a CDN rather than serving static content from your application servers can speed up your projects.

Fastly, Akamai 및 Amazon Cloudfront와 같은 CDN(콘텐츠 전송 네트워크)은 이미지, 비디오, CSS 및 JavaScript 파일과 같은 정적 미디어를 제공합니다.
그들은 일반적으로 가장 가까운 위치에서 정적 콘텐츠를 제공하는 전 세계에 서버를 가지고 있습니다.
애플리케이션 서버에서 정적 콘텐츠를 제공하는 대신 CDN을 사용하면 프로젝트 속도를 높일 수 있습니다.



## 26.9 Other Resources

> Advanced techniques on scaling, performance, tuning, and optimization are beyond the scope of this book, but here are some starting points.

확장, 성능, 조정 및 최적화에 대한 고급 기술은 이 책의 범위를 벗어나지만 여기에서 몇 가지 시작점이 있습니다.



> ➤ “The Temple of Django Database Performance” is a book that dives deep into optimizing Django projects for speed and scalability.
> It’s a delightful book full of fantasy and RPG references and worth every penny. 
> [spellbookpress.com/books/temple-of-django-database-performance/](https://spellbookpress.com/books/temple-of-django-database-performance/)

"Temple of Django Database Performance"는 속도와 확장성을 위해 Django 프로젝트를 최적화하는 방법을 자세히 설명하는 책입니다.
판타지와 RPG 참고 자료로 가득 차 있고 모든 가치가 있는 유쾌한 책입니다.
[spellbookpress.com/books/temple-of-django-database-performance/]()



> ➤ Written with a focus on scaling Django, the book “High Performance Django” espouses many good practices. 
> Full tricks and tips, as well as questions in each section that force you to think about what you are doing. 
> Dated in places, but still full of useful information. highperformancedjango.com

➤ Django 확장에 중점을 두고 쓰여진 "[High Performance Django](https://kupdf.net/download/high-performance-django_5986e795dc0d60656e300d1e_pdf)" 책은 많은 모범 사례를 지지합니다.
전체 트릭과 팁, 그리고 각 섹션의 질문으로 여러분이 하고 있는 일에 대해 생각하게 합니다.
장소에 구애되었지만 여전히 유용한 정보로 가득 차 있습니다. highperformancedjango.com



> ➤ Watch videos of presentations from past DjangoCons and PyCons about different developers’ experiences. 
> Scaling practices vary from year to year and from company to company: https://www.youtube.com/results?search_query=django+scaling

➤ 다양한 개발자의 경험에 대한 과거 DjangoCon 및 PyCon의 프레젠테이션 비디오를 시청합니다.
확장 관행은 해마다 그리고 회사마다 다릅니다: https://www.youtube.com/results?search_query=django+scaling



## 26.10 Summary

> In this chapter, we explored a number of bottleneck reduction strategies including:
> ➤ Whether you should even care about bottlenecks in the first place.
> ➤ Profiling your pages and queries.
> ➤ Optimizing queries.
> ➤ Using your database wisely.
> ➤ Caching queries.
> ➤ Identifying what needs to be cached.
> ➤ Compression of HTML, CSS, and JavaScript. 
> ➤ Exploring other resources.

이 장에서 우리는 다음을 포함한 여러 병목 현상 감소 전략을 탐구했습니다.
➤ 애초에 병목 현상에 대해 신경을 써야 하는지 여부.
➤ 페이지 및 쿼리 프로파일링.
➤ 쿼리 최적화.
➤ 데이터베이스를 현명하게 사용합니다.
➤ 쿼리 캐싱.
➤ 캐시해야 하는 항목 식별.
➤ HTML, CSS 및 JavaScript의 압축.
➤ 다른 리소스 탐색.

>  In the next chapter, we’ll cover various practices involving asynchronous task queues, which may resolve our bottleneck problems.

다음 장에서는 병목 현상 문제를 해결할 수 있는 비동기 작업 대기열과 관련된 다양한 사례를 다룰 것입니다.





#### Ref.

[8퍼센트 성능개선](http://sebatyler.github.io/2016/05/31/django-performance.html)

[Django DB Transaction 1편 - Request와 DB Transaction 묶기(Feat. ATOMIC_REQUESTS)](https://blog.doosikbae.com/142)

[django Cacheops vs Cachalot](https://velog.io/@kim6515516/django-Cacheops-vs-Cachealot)

[Varnish 캐시 히트 효율을 높이는 방법](https://jonnung.dev/system/2020/03/18/increasing-varnish-cache-hit-rate/)

[Reverse Proxy란?](https://brainbackdoor.tistory.com/113)









































