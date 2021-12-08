
# 19장. JavaScript and Django

자바스크립트는 장고와 함께 사용되는 가장 일반적인 방법은 다음과 같습니다.

-  React, Vue, and 기타 프레임워크를 사용하여 실행되는 단일 페이지 앱 접근 방식
- DTL 또는 Jinja2로 작성된 템플릿을 향상 시킴.
- 장고 amin을 유용하고 효율적으로 만들기 위함.

프로젝트의 일부입니다. 
이 장에서는 다음 항목을 다룹니다.
- 19.1: 널리 사용되는 자바스크립트 접근법  
- 19.2 : 자바스크립트를 통한 장고API
- 19.3: 실시간 문제. latency
- 19.4: Django 템플릿과 자바스크립트 사용하기

## 19.1 Popular JavaScript Approaches
더 빠른 r JavaScript engin의 출현과 관련 커뮤니티의 활발함으로,
REST 또는 GraphQL API 와의 통합을 위해 설계된 새로운 자바스크립트 프레임워크가 증가하고 있다.
2021년 가장 인기 있는 세 가지는 다음과 같다.

#### React.js https://facebook.github.io/react/
    Facebook에 의해 만들어지고 유지되는 자바스크립트 프레임워크와 생태계입니다. HTML, iOS 및 Android 응용 프로그램 작성을 위해 설계되었습니다.
    React는 보통 single page apps로 사용되지만 기존 페이지를 향상시키는 데에도 사용할 수 있습니다.
  

#### Vue.js https://vuejs.org
    Vue는 점진적으로 채택될 수 있도록 설계되었습니다. 그것의 생태계가 React.js만큼 크지는 않지만, 더 단순한 데이터 모델은 배우기 쉽다고 여겨진다. 장고 세계에서는
    Vue는 기존 페이지를 개선하거나 단일 페이지 앱을 구축하는 데 자주 사용됩니다.
  
#### Angular https://angular.io
    Angular는 구글이 만든 타입스크립트 오픈소스 프레임워크이다. 장고에서 커뮤니티는 React나 Vue만큼 인기있지 않다.

#### TIP : Next.js와 Nuxt.js https://nextjs.org/ https://nuxtjs.org/
>각각 React와 Vue 위에 구축된 프레임워크입니다.
라우팅, 이미지 최적화, 서브 도메인 라우팅, pre-rendering of pages,
SEO(검색 엔진 최적화) 및 기타 일반적인 작업은 간단하며, 두 작업 모두 잘 연구된 모범 사례를 따릅니다. 우리는 그것들이 생산성 부스터라는 것을 발견했고 앞으로 나올 모든 싱글 페이지 앱에 대해 사용하고 있다.


이러한 광범위한 SPA프레임워크 외에도 서버 사이드 렌더링 HTML 템플리트 사용은 여전히 널리 사용됩니다.
이는 뒤로 물러서 가만히 보면 이 오래된 설계에 대한 새로운 접근법은 그것이 실행 가능한 접근법으로 남아있다는 것을 증명합니다.
hey.com, basecamp.com, 그리고 다른 프로젝트들과 같은 사이트들이 기존 HTML 템플리트를 사용하여 SPA와 같은 속도와 파워를 제공함을 증명합니다.


#### 소규모 집중 라이브러리 + Vanilla
Vanilla JavaScript와 DOM의 상호작용이 최근 몇 년 동안 증가하는동안, 다음과 같은 여러 유용한 라이브러리들이 있다.
개발자에게 권한을 부여하고 코드 복잡성을 줄입니다. 예를 들면 다음과 같다.


- htmlx(htmx.org)
> htmlx(htmx.org)에서는 attributes를 사용하여 AJAX, CSS Transitions, WebSockets 및 Server Sent Events에 직접 액세스할 수 있습니다.
JavaScript에 깊이 공부하지 않고도 최신 사용자 인터페이스를 구축할 수 있습니다. 특히 github.com/Adamchainz/django-htmx과 연계하여 장고 커뮤니티에서 매우 인기가 있습니다.

- Hotwired (hotwired.dev) 
> 핫와이어드(hotwired.dev)는 최신 웹을 구축하는 대안적 접근 방식입니다.
애플리케이션 전송 시 JSON 대신 HTML을 사용합니다.
Hotwire Django project(https://github.com/hotwire-django)로 지원됩니다.


#### Vanilla JavaScript https://developer.mozilla.org/en-US/docs/Web/JavaScript
    Vanilla JavaScript는 React, Vue, jQuery와 같은 추가 라이브러리가 없는 일반 자바스크립트이다. 그런 라이브러리가 절대적으로 필요했던 시절이 있었다.
    그러나 브라우저의 JavaScript는 프로젝트를 구축하기 위한 강력하고 기능이 풍부한 도구가 되었다.


#### jQuery https://jquery.com
    한때 자바스크립트 세계의 중추였던 JQuery가 제공하는 많은 기능들은 이제 새로운 프로젝트에는 사용되지 않는 바닐라 자바스크립트에 영향을 주었다.
    그러나 기존 장고 프로젝트의 군단은 이를 광범위하게 사용하고 있으며 향후 몇 년 동안 다른 도구로 계속 유지되거나 업그레이드되어야 한다.


이러한 7가지 옵션(및 다양한 경쟁사)은 이른바 'immediate user experience'을 개선할 수 있습니다.
하지만, 모든 좋은 일에는 항상 고려해야 할 것과 해야 할 것이 있습니다.
다음은 컨텐츠용 API를 소비하는 프런트엔드 프로젝트에서 발견한 여러 가지 anti-patterns입니다.


### 19.1.1 Multi-Page Apps으로 충분할 때  Single Page Apps로 구축
19.1.1 다중 페이지 앱으로 충분할 때 단일 페이지 앱 구축
React, Vue 및 Angular와 같은 프레임워크가 있는 단일 페이지 앱은 구축하기에 재미있지만, 기존  CMS-site(예시:워드프레스)가 구축되어야 합니까? 물론 콘텐츠 페이지에는 API 기반 editing controls이 포함될 수 있지만, 이러한 종류의 사이트를 구축할 때는 전통적인 HTML 페이지에 대해 언급할 것이 있다.

예를 들어, 2017년에 우리의 health provider는 SPA 스타일의 사이트를 가지고 있었습니다. 그것은 사랑스러웠다. 모든 것이 함께 움직이는 방식은 경이로웠다. 그리고 우리가 비교 연구를 해야 할 때는 전혀 쓸모가 없었습니다.

그 사이트의 최악의 예는 우리가 쉽게 비교할 수 없는 의사들의 명단을 검색 시스템이 반환했을 때였다. 하나를 클릭했을 때 더 많은 정보를 얻을 수 있었고, 그들의 데이터는 슬라이딩 모달입니다. 마우스 오른쪽 버튼을 클릭하고 독립 탭에서 여러 개를 열 수 없어 루트 검색 페이지로 이동했습니다. 우리는 의사 개개인에 대한 정보를 인쇄하거나 이메일로 보낼 수 있지만 PDF와 이메일은 탭 사이를 뛰어다니는 것과 비교할 때 끔찍한 비교 도구입니다.

사이트에서 제공해야 하는 것은 각 의사에게 개별 도메인 참조 자료(즉, URL)입니다. 백엔드의 서버에 의해 구문 분석되거나 프런트엔드의 자바스크립트 URL 관리에 의해서 분석됩니다. 이것은 어려운 일이 아니지만, 우리가 다른 의료진에게 가기 전까지는 고통스러울 정도로 흔한 문제로 남아 있었습니다.


### 19.1.2 Upgrading Legacy Sites
새로운 버전을 위해 전체 사이트를 폐기하는 경우가 아니라면 전체 프런트엔드를 한 번에 업그레이드하지 마십시오.
기존 프로젝트로 작업할 때 한 페이지 앱으로 새 기능을 추가하는 것이 더 쉬운 경우가 많습니다. 이를 통해 기존 코드베이스의 안정성을 유지하면서 프로젝트의 유지보수자들이 새로운 기능으로 개선된 경험을 전달할 수 있습니다. 이에 대한 좋은 예로 기존 프로젝트에 캘린더 응용 프로그램을 추가하는 것이 있습니다. 이것은 Vue에서는 쉽게 가능하지만, React에서는 덜 가능합니다.

### 19.1.3 Not Writing Tests
클라이언트 측을 포함한 새로운 언어 또는 프레임워크에서 처음 작업을 시작할 때
자바스크립트 test를 건너뛰고 싶은 유혹이 있어도 하지 마세요.(test는 꼭 하세요) 고객사 업무는 매년 더 복잡하고 정교해지고 있습니다. 진화하는 클라이언트측 표준들 사이에서, 서버측처럼 읽기 쉽지 않습니다.
우리는 Chapter 24: Testing Stinks and Is a Waste of Money! 에서 Django/Python testing을 다룹니다!
자바스크립트 테스트를 위한 좋은 참조 https://stackoverflow.com/questions/300855/javascript-unit-test-tools-for-tdd

### 19.1.4 Not Understanding JavaScript Memory Management
단일 페이지 앱은 좋지만 사용자가 지속적으로 열어두는 복잡한 구현은 매우 오랜 시간 동안 객체를 브라우저에 보관합니다. 관리되지 않으면 브라우저 속도가 느려지고 충돌이 발생할 수 있습니다. 각 JavaScript 프레임워크에는 이러한 잠재적인 문제를 해결하는 방법에 대한 도구 또는 조언이 함께 제공되므로 권장 방법을 알고 있는 것이 좋습니다.

### 19.1.5 Storing Data in the DOM When It’s Not jQuery
jQuery를 수 년 동안 사용한 후, 우리들 중 일부는 저장된 데이터(특히 다니엘)에 DOM 요소를 사용하는 데 익숙해졌다. 그러나 다른 자바스크립트 프레임워크를 사용할 때는 이상적이지 않다.
이들은 클라이언트 데이터를 처리하기 위한 자체 메커니즘을 가지고 있으며, 이를 따르지 않음으로써 이러한 프레임워크가 약속하는 기능 중 일부가 손실될 위험이 있습니다.
선택한 JavaScript 프레임워크에 대한 데이터 관리 방법을 찾아보고 최대한 깊이 수용하는 것이 좋습니다.

## 19.2 Consuming Django-served APIs with JavaScript
지금까지 REST API 생성과 템플릿 모범 사례에 대해 설명했으므로 이 두 가지를 결합해 보겠습니다. 다시 말해, REST/GraphQL API가 관리하고 현대 자바스크립트 프레임워크가 제공하는 콘텐츠를 사용하여 최종 사용자에게 콘텐츠를 표시하는 장고기반 도구를 사용하는 것이 모범 사례이다.

### 19.2.1 Learn How to Debug the Client
클라이언트측 자바스크립트를 디버깅하는 것은 console.log()와
console.dirs 문. 디버깅과 오류 찾기를 위한 수많은 도구들이 있으며, 그 중 일부는 특정한 자바스크립트 프레임워크를 위해 특별히 작성되었다. 도구가 선택되면 클라이언트 측 테스트 작성 방법을 익히는 데 하루를 보내는 것이 좋습니다.

Reference material:
- developers.google.com/web/tools/chrome-devtools
- developer.mozilla.org/en-US/docs/Mozilla/Debugging/Debugging_JavaScript

### 19.2.2 When Possible, Use JavaScript-Powered Static Asset Preprocessors
약 2017년까지 우리는 자바스크립트, CSS 미니화를 포함한 모든 곳에서 파이썬을 사용했습니다. 그러나 JavaScript 커뮤니티는 이러한 도구 버전을 더 잘 유지하고 있습니다.
파이썬 커뮤니티보다 낫죠 괜찮습니다, 툴체인의 이 부분에 대한 작업을 마쳤기 때문에 다른 부분에 집중할 수 있습니다.
우리가 이것을 쓰면서 이런 종류의 작업에 가장 많이 사용되는 도구는 웹팩입니다. React, Vue 및 모든 주요 프레임워크에서 사용되는 웹 팩은 브라우저 기반 스크립트를 자산으로 제공합니다. Vue 또는 React CLI 툴에서 제공하는 스톡 웹 팩 설정을 사용하는 것을 선호하지만 웹 팩을 이해하는 것은 매우 강력한 기술입니다.

References:
- webpack.js.org
- github.com/owais/django-webpack-loader - Owais Lone’s Django package for transparently using webpack with Django

## 19.3 Real-Time Woes a.k.a. Latency
세계에서 가장 넓은 대역폭 파이프 컨텐츠를 사용하여 잘 설계되고 인덱싱되고 캐싱된 실시간 프로젝트를 구축했다고 가정해 보겠습니다. 우리는 모든 부하를 처리할 수 있으며, 테스트 사용자는 프로젝트의 속도와 기능에 박수를 보냅니다. 상황이 좋아 보이니 보너스와 임금 인상을 기대하겠습니다.
그러자 지구 반대편에서 애플리케이션의 느린 속도에 대한 불만이 들어오기 시작했습니다. 우리의 노력은 잠재적인 대규모 사용자 블록에 '실시간'이 아니며, 우리의 고객/상사는 매우 불만족스러워합니다.
축하합니다, 빛의 속도에 도달했습니다!
이건 농담이 아니라 정말 심각한 문제야. 여기, 장고는 문제가 아닙니다. 대신 물리학이죠.
HTTP 요청이 지구 둘레의 절반에 걸쳐 왔다 갔다 하는 데 걸리는 시간은 인간에게 매우 주목할 만합니다. 서버 측 및 클라이언트 측 프로세싱을 추가하면 잠재적인 사용자나 기존 사용자가 소외될 위험이 있습니다.
또한, 가장 빠른 지역 연결도 , 일시적 고장과 속도가 느리다는 것을 기억하세요. 따라서 '실시간' 응용 프로그램이 이러한 종류의 동작을 처리할 수 있는 방법을 갖는 것은 드문 일이 아닙니다.
