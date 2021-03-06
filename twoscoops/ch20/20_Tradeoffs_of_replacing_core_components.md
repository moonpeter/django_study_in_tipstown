### 20 Tradeoffs of Replacing Core Components

>  어떤 사람들은 Django 스택의 핵심 부분을 다른 부분으로 교체하는 것을 옹호합니다. 해야 합니까?


짧은 답변:

하지 마십시오.
Instagram의 창립자 중 한 명(Kevin Systrom)도 Forbes.com에 다음과 같이 말했습니다.

> 그것은 완전히 불필요합니다 (bit.ly/2pZxOBO)



긴 답변: 
Django 모듈은 단순히 Python 모듈이기 때문에 가능합니다.
그만한 가치가 있습니까? 

다음과 같은 경우에만 가치가 있습니다.

➤ 타사 Django 패키지를 사용하는 능력의 일부 또는 전부를 희생해도 괜찮습니다.

➤ 강력한 Django 관리자를 포기하는 데 문제가 없습니다.

➤ 핵심 Django 구성 요소로 프로젝트를 구축하기 위해 이미 결연한 노력을 기울였지만 
주요 방해 요소인 벽에 부딪히고 있습니다.

➤ 문제의 근본 원인을 찾고 수정하기 위해 이미 자체 코드를 분석했습니다. 
예를 들어 템플릿에서 만든 쿼리 수를 줄이기 위해 할 수 있는 모든 작업을 완료했습니다.

➤ 캐싱, 비정규화 등을 포함한 다른 모든 옵션을 살펴보았습니다.

➤ 귀하의 프로젝트는 수많은 사용자가 있는 실제 라이브 프로덕션 사이트입니다.
다시 말해, 섣부른 최적화가 아니라는 확신이 듭니다.

➤ Django가 처리하는 데 문제가 있는 경우 SOA(Service Oriented Approach) 채택을 검토하고 거부했습니다.

➤ Django를 업그레이드하는 것이 앞으로 매우 고통스럽거나 불가능할 것이라는 사실을 기꺼이 받아들일 
것입니다.



#### 20.1 The Temptation to Build FrankenDjango

>  기괴한 Django를 구축하려는 유혹.


몇 년마다 새로운 유행으로 인해 개발자들이 특정 핵심 Django 구성 요소를 교체하도록 합니다.

여기 우리가 왔다가 사라지는 몇 가지 유행에 대한 요약이 있습니다.

![image-20211212175905675](C:\Users\eoeht\AppData\Roaming\Typora\typora-user-images\image-20211212175905675.png)

그림 20.1: 케이크의 더 많은 핵심 구성 요소를 아이스크림으로 대체하는 것은 좋은 생각인 것 같습니다.
어떤 케이크가 이길까요? 오른쪽에 있는거!



#### 20.2 Non-Relational Databases vs. Relational Databases

영구 데이터 저장을 위해 관계형 데이터베이스를 사용하는 Django 프로젝트조차도 비관계형 데이터베이스에 
의존합니다.

프로젝트가 캐싱을 위해 Memcached 및 Redis와 같은 도구에 의존하는 경우 큐잉하고 나면 비관계형 데이터베이스를 사용합니다.

문제는 NoSQL 솔루션이 장기적인 영향을 깊이 고려하지 않고 Django의 관계형 데이터베이스 기능을 완전히 대체하는 데 사용될 때 발생합니다.



##### 20.2.1 일부 비관계형 데이터베이스가 ACID를 준수하는 것은 아님

ACID의 다른 뜻은 다음과 같습니다.

**`Atomicity(원자성)`**은 트랜잭션의 모든 부분이 작동하거나 모두 실패함을 의미합니다. 
이것이 없으면 데이터 손상의 위험이 있습니다.

`Consistency (일관성)`이란 모든 트랜잭션이 데이터를 유효한 상태로 유지함을 의미합니다.
문자열은 문자열로 유지되고 정수는 정수로 유지됩니다. 이것이 없으면 데이터 손상의 위험이 있습니다.

`Isolation(격리)`는 트랜잭션 내에서 데이터의 동시 실행이 충돌하거나 다른 트랜잭션으로 누출되지
않음을 의미합니다. 이것이 없으면 데이터 손상의 위험이 있습니다.

`Durability (지속성)`은 트랜잭션이 커밋되면 데이터베이스 서버가 종료되더라도 그대로 유지됨을 의미합니다. 이것이 없으면 데이터 손상의 위험이 있습니다.



>  각각의 설명이 `이 정보가 없으면 데이터 손상 위험이 있습니다.`로 끝나는 것을 확인하셨습니까?
>
> 이는 많은 NoSQL 엔진의 경우 ACID 준수를 위한 메커니즘이 거의 또는 전혀 없기 때문입니다.
>
> 데이터를 손상시키는 것이 훨씬 더 쉽습니다. 
> 캐싱과 같은 문제는 대부분 문제가 되지 않지만 다른 문제입니다.



##### Table 20.1: Fad-based Reasons to Replace Components of Django

> Django의 구성 요소를 대체하는 유행 기반 이유
> Fad : 6~12개월 정도의 단기간 동안 나타났다가 사라지는 추세



###### Fad

성능상의 이유로 데이터베이스/ORM을 NoSQL 데이터베이스 및 해당 ORM으로 교체합니다.

###### Reasons

괜찮지 않음

- 아이스크림을 싫어하는 사람들을 위한 소셜 네트워크에 대한 아이디어가 있습니다.
- 지난달부터 짓기 시작했다.
- 수십억까지 확장해야 합니다!

괜찮음

- 저희 사이트의 사용자 수는 5천만 명이며 인덱스, 쿼리 최적화, 캐싱 등으로 할 수 있는 작업의 한계에
  도달했습니다.
- 우리는 또한 Postgres 클러스터의 한계를 뛰어 넘고 있습니다.
- 나는 이것에 대해 `많은 연구`를 했고 그것이 도움이 되는지 확인하기 위해 Cassandra에 
  데이터의 단순한 비정규화된 보기를 저장하려고 합니다.
- 나는 CAP 정리(en.wikipedia.org/wiki/CAP_theorem)를 알고 있으며 이 관점에서 최종 일관성은 괜찮습니다.



###### Fad

데이터 처리상의 이유로 데이터베이스/ORM을 NoSQL 데이터베이스 및 해당 ORM으로 교체합니다.

###### Reasons

괜찮지 않음

- SQL은 거지같아! 
- 우리는 MongoDB와 같은 문서 지향 데이터베이스를 사용할 것입니다!

괜찮음

- PostgreSQL 및 MySQL의 JSON 데이터 유형은 MongoDB 데이터 저장 시스템의 거의 모든 측면을
  복제합니다.
- Yes, MongoDB에는 `MapReduce` 기능이 내장되어 있지만 작업 대기열에서 실행하는 것이 더 쉽습니다.



###### Fad

Django의 템플릿 엔진을 Jinja2, Mako 또는 다른 것으로 교체합니다.

###### Reasons

괜찮지 않음 1

- Jinja2가 더 빠르다는 것을 읽었습니다.
- 캐싱이나 최적화에 대해 아무것도 모르지만 Jinja2가 필요합니다!

괜찮지 않음 2

- 나는 Python 모듈에 로직이 있는 것을 싫어합니다.
- 내 템플릿에 로직이 필요합니다!

괜찮음.

- Google에서 색인을 생성하도록 설계된 1MB 이상의 HTML 페이지를 생성하는 소수의 보기가 있습니다.
- 여러 템플릿 언어에 대한 Django의 기본 지원을 사용하여 Jinja2로 1MB 이상의 페이지를 렌더링하고 나머지는 다음으로 제공합니다. Django 템플릿 언어.



##### 20.2.2 Don’t Use Non-Relational Databases for Relational Tasks

> 관계형 작업에 비관계형 데이터베이스를 사용하지 마십시오


비관계형 데이터베이스를 사용하여 미국 50개 주에서 부동산 판매, 부동산 소유자 및 부동산 법률이 이들에게
적용되는 방식을 추적한다고 상상해 보십시오.

예측할 수 없는 세부 정보가 많이 있으므로 스키마 없는 데이터 저장소가 이 작업에 적합하지 않을까요?


아마도...

- 재산, 재산 소유자 및 50개 주의 법률 간의 관계를 추적해야 합니다.
- 우리의 Python 코드는 모든 구성 요소 간의 참조 무결성을 유지해야 합니다.
- 또한 올바른 데이터가 올바른 위치에 있는지 확인해야 합니다.


이와 같은 작업의 경우 관계형 데이터베이스를 사용하십시오.



##### 20.2.3 Ignore the Hype and Do Your Own Research

> 과대 광고를 무시하고 자신만의 연구를 하십시오


비관계형 데이터베이스가 관계형 데이터베이스보다 빠르고 확장성이 뛰어나다고 흔히 말합니다.

이것이 사실이든 아니든, 특정 대체 데이터베이스 솔루션 뒤에 있는 회사의 마케팅 과대 광고를 맹목적으로 따르지 마십시오.

또한 주요 프로젝트 인프라를 크게 변경하기 전에 소규모 취미 프로젝트에서 익숙하지 않은 
NoSQL 데이터베이스를 실험해 보십시오. 주요 코드베이스는 놀이터가 아닙니다.

**기업과 개인이 배운 교훈**

➤ Pinterest: [medium.com/@Pinterest_Engineering/stop-using-shiny-3e1613c2ce14](https://medium.com/Pinterest_Engineering/learn-to-stop-using-shiny-new-things-and-love-mysql-3e1613c2ce14)
➤ Dan McKinley while at Etsy: [mcfunley.com/ why-mongodb-never-worked-out-at-etsy](http://mcfunley.com/why-mongodb-never-worked-out-at-etsy)
➤ When to use MongoDB with Django [daniel.feldroy.com/ when-to-use-mongodb-with-django.html](https://daniel.feldroy.com/when-to-use-mongodb-with-django.html)



[설레발 주도 개발](https://lazygyu.net/blog/hype_driven_development)단계로 보는 **NoSQL** 편

➤ 1단계 (진짜 문제와 해결책)

- SQL 데이타베이스들은 아주 많은 양의 요청이나 구조화되지 않은 데이터를 처리하기가 어렵습니다.
- 세계 곳곳에서 새로운 세대의 데이터베이스를 개발하기 시작합니다.
  

➤ 2단계 (발표, 자랑질, 키워드)

- 설레발 키워드 : 확장성, 빅데이터, 고성능
  

➤ 3단계 (빠돌이 탄생)

- 우리의 데이터베이스는 넘나 느리고 규모도 충분히 크지 않아! 우린 NoSQL이 필요해!
  

➤ 4단계 (실망)

- 테이블 조인이 필요한가요? 그런거 없습니다. 
- 단순한 SQL 조작도 커다란 도전이 되어 버립니다. 
- 개발 속도는 점점 느려지고 핵심적인 문제들은 해결되지 않습니다.
  

➤ 5단계 (현실인식)

- NoSQL 은 아주 특정한 문제들에 대한 해법입니다
  (아주 많은 양의 데이터, 구조화 되지 않은 데이터, 혹은 아주 많은 처리량 등). 
- SQL 은 실제로 아주 훌륭한 도구이며, 적절하게 사용하기만 한다면 많은 양의 데이터와 높은 처리량을 
  감당할 수 있습니다. 
- NoSQL 이 반드시 필요한 경우는 2016년 현재까지는 아주 드뭅니다.



##### 20.2.4 How We Use Non-Relational Databases With Django

> Django에서 비관계형 데이터베이스를 사용하는 방법



이것이 우리가 선호하는 방식입니다:

➤ 비관계형 데이터 저장소를 사용하는 경우 캐시, 대기열 및 비정규화된 데이터와 같은 단기적인 항목으로 사용을 제한합니다. 그러나 움직이는 부품의 수를 줄이기 위해 가능하면 피하십시오

➤ 장기 관계형 데이터 및 때로는 비정규화된 데이터에 관계형 데이터 저장소를 사용합니다
(PostgreSQL의 배열 및 JSON 필드는 이 작업에 적합합니다).



#### 20.3 What About Replacing the Django Template Language?

> 장고 템플릿 언어를 교체하는 방법은 무엇입니까?


우리는 거대한 크기의 렌더링된 콘텐츠를 제외하고 DTL(Django Template Language)을 완전히 고수하는 관행을 지지합니다.

그러나 이 사용 사례는 이제 Django의 대체 템플릿 시스템에 대한 기본 지원으로 다루어지기 때문에 이 주제에 대한 토론을 옮겼습니다. 16장: Django 템플릿과 Jinja2로.



#### 20.4 Summary

올바른 작업을 위해서는 항상 올바른 도구를 사용하십시오.

우리는 아이스크림을 제공할 때 스쿱을 사용하는 것처럼 스톡 장고 성분으로 하는 것을 선호합니다.
하지만 다른 도구들이 말이 되는 경우도 있습니다.

아이스크림에 야채를 섞는 유행을 따르지 마십시오.

고전적인 딸기, 초콜릿, 바닐라를 브로콜리, 옥수수, 시금치와 같은 "고성능" 맛으로 대체할 수는 없습니다. 
너무 멀리 가는 것입니다.



















