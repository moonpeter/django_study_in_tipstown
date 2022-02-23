
# 18장. Django로 GraphQL API 구현하기


GraphQL은 REST와 달리 스키마, types, 실시간 업데이트(Subscriptions)를 처리하는 내장 메서드입니다.

API 클라이언트는 원하는 데이터를 지정하고 스키마와 type을 통해 검사 도구를 쉽게 구축 및 쿼리를 쉽게 파악할 수 있습니다.

cf)

불필요한 정보까지 클라이언트로 전달되는 overfetching
특정 엔드포인트가 필요한 정보를 충분히 전달하지 못하는 underfetching

https://devsoyoung.github.io/posts/underfetching-overfetching/

GraphQL 응답은 JSON이나 YAML로 직렬화됩니다.

https://graphql.org/learn/(링크삽입 필요)
초보자에겐 REST보단 GraphQL이 더 쉬울 수 있습니다.


REST에 익숙한 개발자들은 GraphQL의 API 호출 성공 여부를 HTTP 메서드로 판단하려하지만, 이것은 문제가 될 수 있습니다. REST같은 경우 GET, POST 등 여러 메서드를 사용하지만, GraphQL은 POST만 사용하여 200, 500 응답만 합니다.
> 그러므로 대부분의 GraphQL 실행이 errors array field를 응답에 포함합니다. API 호출의 성공을 판단하기 위해서, 우리는 해당 필드가 비어 있다는 것을 통해 알 수 있음.
```json
{
  "data": null,
  "errors": [
    {
      "message": "Syntax Error GraphQL (30:3) Expected Name, found )\n\n29:     \n30:   ){\n      ^\n31:     filename\n",
      "locations": [
        {
          "line": 30,
          "column": 3
        }
      ]
    }
  ]
}
```

```json
{
  "data": {
    "test1": {
      "message": null,
      "filename": "2021-11-10/21IHPA02592A_211110_184432_F272EABD1637.mp4",
      "success": true
    },
    "test2": {
      "message": null,
      "filename": "2021-11-10/21IHPA02592A_211110_184548_F272EABD1637.mp4",
      "success": true
    },
    "test3": {
      "filename": "2021-09-27/21IHPA01111A_210927_144703_F6AD376A17D8.mp4",
      "success": true,
      "message": null
    }
  }
}
```


| GraphQL Method | REST Method | Action |
| :---------------------------------------------------- | :---------: | :------------------- |
| query GetRecords()       |    GET /records     | Read-only Query               |
| subscription GetRecords()                  |     no equivalent     | websocket을 열고 변경 사항 업데이트 |
| query GetRecord(id: X)                     |     GET /record/:id     | Read-only Query     |
| subscription GetRecord(id: X)              |    GET /record/:id    | websocket을 열고 변경 사항 업데이트       |
| mutation CreateRecord()                    |   POST /records/    |  레코드 생성  |
| mutation UpdateRe- cord(id: X) |    PUT /records/:id     |   레코드 업데이트          |
| mutation DeleteRecord(id: X)   |   DELETE /records/:id   |     레코드 삭제             | 


  
## 18.1 Dispelling the Performance Myth(퍼포먼스 관련)
모든 액세스 요청이 다를 경우 쿼리에 의해 제기된 데이터를 어떻게 캐시?

1. 필요한 데이터만 지정한 응답을 사용함으로 클라이언트는 REST보다 훨씬 적은 데이터를 소비합니다. 이는 서버와 데이터베이스 오버헤드 모두 영향이 미칩니다.
2. REST API와 마찬가지로 캐싱, 인덱싱, 코드 최적화를 통해 공통 액세스 패턴을 식별하고 처리할 수 있습니다.

그래프QL API가 병목현상에 대한 면역이라고 말하는 것은 아닙니다. 단순히 REST API만큼 관리 가능한 것이 아니라, REST API 보다 더는 아닐 지라도 더 낮은 대역폭으로 인한 것이 아닙니다.

## 18.2 Libraries for Building GraphQL Applications
GraphQL은 간단한 REST API를 만들때가 아닌, GraphQL API의 기본 요소를 라이브러리로 사용하는 것이 가장 좋습니다. Ariadne, Graphene 이 선택할 수 있는 좋은 옵션입니다.
cf) https://fastapi.tiangolo.com/advanced/graphql/ 
> fastapi의 경우에는 Strawberry 라는 라이브러리가 가장 먼저 추천되는 것으로 알고 있습니다.


### 18.2.1 Ariadne
- https://ariadnegraphql.org/
- ASGI, Channels과 함께 사용하면 완전히 비동기식입니다. GraphQL을 통해 Django 프로젝트에서 실시간 업데이트가 가능합니다.
- 비동기를 사용할 준비가 되지 않았다면 WSGI에서 계속 실행할 수 있습니다.
- 스키마가 우선입니다. 코딩을 하기전에 디자인을 지정해야 합니다.
- Creating queries and mutations requires following a simple and lightweight API.
https://graphql.org/learn/queries/
- 여러 GraphQL 서버를 구성하기 위해 Apollo Federation를 지원합니다.
### 18.2.2 Graphene
Graphene은 GraphQL을 지원하는 최초의 Python 라이브러리이고, Django 통합도 지원합니다. 노드에서 Django Form이나 DRF Serializer를 사용하는 기능을 사용할 수 있습니다. 수십만명의 사용자가 있다면 Ariadne보다 더 효율적입니다.

## 18.3 GraphQL API Architecture
GraphQL API를 구축하는 것은 쉽지만, 프로젝트의 요구사항에 맞는 확장/유지/관리 하려면 고려해야 하는 사항들이 있습니다.

### 18.3.1 Don’t Use Sequential Keys as Public Identifiers
순차적인 기본키를 공개적으로 사용하는 것은 보안 문제가 될 수 있습니다.

Section 28.28: Never Display Sequential Primary Keys.
대안: UUID, etc


### 18.3.2 Use Consistent API Module Naming
프로젝트 전체의 네이밍 방법은 일관되어야 합니다.
Ariadne API는 가벼워서 하나의 schema.py 모듈에 모든 쿼리와 변형을 작성할 수 있습니다.
```sh
config/
├── schema.py # imports forms & models from flavors app
├── settings/
├── urls.py
flavors/
├── __init__.py
├── app.py
├── forms.py
├── models.py
```
schema.py 모귤이 너무 커졌다면 분할할 수 있습니다.
Queries and mutations이 개별 앱으로 이동하고 make_executable_schema()를 호출하여 schema.py 모듈을 가져옵니다.

```sh
config/
   ├── schema.py # imports queries/mutations from flavors app
   ├── settings/
   ├── urls.py
   flavors/
   ├── __init__.py
   ├── app.py
   ├── api/
   │   ├── queries.py  # imports models
   │   ├── mutations.py  # imports forms and models
   ├── forms.py
   ├── models.py
 ```
- 하지만 여전히 Django 형식과 모델에 의존
- 직관적이고 일관된 네이밍 패턴을 고수

### 18.3.3 Try to Keep Business Logic Out of API Views(API View로부터 비즈니스 로직 분리시키기)

API의 크기와 상관없이 로직은 해당 위치에 유지하세요.
유효성 검사는 forms(또는 DRF serializers)이어야 하며, 데이터베이스 처리는 models에 있어야 합니다.
Ariadne는 비즈니스 로직을 함수나 클래스 정의로 덤핑하여 사용하면 API v2를 출시할 때 로직을 테스트, 업그레이드, 재사용하기 어려워집니다.

### 18.3.4 Test Your API
Ariadne 기반 GraphQL을 테스트하는 가장 좋은 방법은 Django 내장 RequestFactory를 사용하는 것입니다.
