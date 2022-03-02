# 27  AsynchronousTaskQueues

> An asynchronous task queue is one where tasks are executed at a different time from when they are created, and possibly not in the same order they were created. Here is an example of a human-powered asynchronous task queue:

비동기 태스크 큐는  태스크가 생성될 때와 다른 시간에 실행되는 큐이며, 생성된 순서와 다를 수 있습니다. 다음은 휴먼 파워 비동기 태스크 큐의 예입니다. 

> 1. In their spare time, Audrey and Daniel make ice cream cakes, taking orders from friends and family. They use an issue tracker to track their tasks for scooping, spread- ing, and decorating each cake.
> 2. Every so often, when they have spare time, they review the list of tasks and pick one to do. Audrey prefers scooping and decorating, always doing those tasks first. Daniel prefers scooping and spreading, finishing those before decorating. The result is asynchronous completion of cake-making tasks.
> 3. As a cake-making task is completed and delivered, they mark the issue as closed.
> 
1. 여가 시간에, 오드리와 다니엘은 친구들과 가족들의 주문을 받아 아이스크림 케이크를 만듭니다. issue tracker를 사용하여 각 케이크 퍼내기, 스프레드 및 장식 작업을 추적합니다.
2.  그들이 여가 시간이 있을 때 매우 자주 과제 목록을 검토하고 할 일을 고릅니다. 오드리는 항상 퍼내거나 장식하는 것을 먼저 하는 것을 선호합니다. 대니얼은 장식하기 전에 퍼내기와 펴바르기를 끝내는 것을 선호해요. 그 결과 케이크 만들기 작업이 비동기식으로 완료됩니다.
3.  케이크 제작 작업이 완료되어 전달되면, 그들은 이슈를 종결로 표시합니다.

---

#### TIP: Task Queue vs Asynchronous Task Queue
> In the Django world, both terms are used to describe asynchronous task queue. When someone writes task queue in the context of Django, they usually mean asyn- chronous task queue.
 
장고 세계에서 두 용어는 비동기 task queue를 기술하는 데 사용된다. 누군가가 Django의 컨텍스트에서 task queue을 작성할 때 일반적으로 비동기식 task queue을 의미합니다.

---

> Before we get into best practices, let’s go over some definitions:

모범 사례를 시작하기 전에 몇 가지 정의를 살펴보겠습니다.

> * **Broker**
  >> The storage for the tasks themselves. This can be implemented using any sort of persistence tool, although in Django the most common ones in use are RabbitMQ and Redis. In the human-powered example, the storage is an online issue tracker. 
> * **Producer** 
  >> The code that adds tasks to the queue to be executed later. This is application code, the stuff that makes up a Django project. In the human-powered example, this would be Audrey and Daniel, plus anyone they can get to pitch in to help.
> * **Worker** 
  >> The code that takes tasks from the broker and performs them. Usually there is more than one worker. Most commonly each worker runs as a daemon under supervision. In the human-powered example, this is Audrey and Daniel. 

* **Broker**
  * 작업 자체를 위한 저장소입니다. 이것은 어떤 종류의 지속성 도구를 사용하여 구현할 수 있지만 장고에서 가장 흔히 사용되는 것은 RabbitMQ와 Redis이다. human-powered예에서 스토리지는 online issue tracker입니다.
* **Producer** 
  * 나중에 실행할 작업을 큐에 추가하는 코드입니다. 장고 프로젝트를 구성하는 애플리케이션 코드입니다. human-powered예를 들어, 이 사람은 오드리와 다니엘 그리고 그들이 도울 수 있는 누구라도 될 것입니다.
* **Worker** 
    * 브로커에서 작업을 가져와 수행하는 코드입니다. 보통 한 개 이상의 Worker가 있습니다. 가장 일반적으로 각 Worker는 통제 하에 데몬으로 실행됩니다. human-powered예에서, 이것은 오드리와 다니엘입니다.


## 27.2 Choosing Task Queue Software
> Celery, Django Channels, or calls to serverless services such as AWS Lambda, which to choose? Let’s go over their pros and cons:

셀러리, 장고 Channels 또는 AWS 람다와 같은 서버리스 서비스에 대한 호출 중 어떤 것을 선택할 수 있습니까? 그들의 장단점을 살펴보자.

| 소프트웨어 | 장점 | 단점 |
| --- | --- | --- |
| Celery | Django 및 Python 표준, 다양한 스토리지 유형, 유연하고 full-featured,  대용량에 아주 적합| 어려운 setup, 기본적인 내용을 제외한 모든 항목에 대한 가파른 학습 곡선 |
| DjangoChannels | Defacto Django 표준, 유연하고 사용하기 쉬우며 Django에 websocket 지원 | 재시도 메커니즘 없음, Redis 전용 |
| AWSLambda| 유연하고 확장 가능하며 쉬운 설정| API 호출이 느릴 수 있으며, 외부 로깅 서비스를 필요로하고, 복잡성을 가중시키며, 알림을 위한 REST API를 생성해야 합니다.|
| Redis-Queue, Huey, etc| Celery에 비해 메모리 설치 공간이 적고 비교적 쉽게 설정 가능 |셀러리만큼 기능이 많지 않음, usually Redis-only, 소규모 커뮤니티|

> Here is our general rule of thumb: 
>> * If time permits, move all asynchronous processes to Serverless systems such as AWS Lambda.
>> * If API calls to Serverless become an issue, encapsulate these calls in Celery tasks. For us, this has only been a problem with bulk API calls to AWS Lambda.
>> * Use Django Channels for websockets. The lack of retry mechanism forces you to invent things that Celery provides out-of-the-box.
>> * For security and performance reasons, any and all API calls to user-defined URLs are done through task queues.

일반적인 경험을 통해 얻은 법칙은 다음과 같습니다.
* 시간이 허락하면, 모든 비동기 프로세스를 AWS 람다와 같은 서버리스 시스템으로 이동합니다.
* Serverless에 대한 API 호출이 문제가 될 경우, 해당 호출을 Celery 작업에 캡슐화합니다. 우리는 AWS 람다에 대한 대량 API 호출에만 문제가 있었습니다.
* websockets에 장고 채널을 사용합니다. 재시도 매커니즘의 부재 때문에 Celery가 즉시 제공하도록 구현해야합니다.
* 보안 및 성능상의 이유로 사용자정의 URL에 대한 모든 API 호출은  task queues를 통해 수행됩니다.

>Your own experience and knowledge should be used to determine which task queue system you use for a project. Examples:
>> * If you have a good amount of Celery experience and are comfortable with it, then by all means use it for small volume or toy projects.
>> * Most Serverless systems have hard-limits on disk drive space (Example: AWS Lambda limits you to 512MB tmp directory storage). This can be a problem when manipulating large files (transcoding of video) or using certain libraries. In these cases, you can either use third-party services or construct dedicated servers running Celery to handle such tasks.
>> * The extensibility of the Django Channel’s Generic Consumers are so nice that we’ve been tempted to write our own retry mechanisms. While we haven’t had the time to do it, you might. Just be aware that it’s a larger, more complicated task than you might expect.

프로젝트에 사용할 태스크 대기열 시스템을 결정하려면 자신의 경험과 지식을 사용해야 합니다. 예:
* 셀러리 경험이 풍부하고 셀러리에 익숙하다면 소규모 프로젝트나 토이 프로젝트에 반드시 사용하십시오.
* 대부분의 서버리스 시스템은 디스크 공간에 대한 제한이 있습니다.(예: AWS 람다는 512MB tmp 디렉터리 스토리지로 제한됩니다). 이 문제는 대용량 파일을 조작하거나(비디오 변환) 특정 라이브러리를 사용할 때 발생할 수 있습니다. 이런 경우, 이러한 태스크를 처리하기 위해 타사 서비스를 사용하거나 Celery를 실행하는 전용 서버를 구성할 수 있습니다.
* Django Channel의 Generic Consumers(General Consumer)의 확장성이 너무 좋아서 당사는 자체적인 재시도 메커니즘을 개발하고자 합니다. 아직 그럴 시간이 없었으니까, 그럴 수도 있어. 당신이 생각하는 것보다 더 크고 복잡한 작업이라는 것만 알아두세요


## 27.3 Best Practices for Task Queues
> While each of the different task queue packages has their own quirks, there are some con- stants we can apply to all of them. A nice feature about these practices is that they help with the portability of your task functions. This can be incredibly useful when you discover that while Django Channels has been useful, the lack of a retry mechanism requires you to switch to Celery.

각 task queue 패키지마다 자체적인 특성이 있지만, 모든 task queue 패키지에 적용할 수 있는 방법이 있다. 이러한 방법의 장점은 task 기능의 이식성에 도움이 된다는 것입니다. 장고 채널은 유용했지만 재시도 메커니즘이 없기 때문에 셀러리로 전환해야 한다는 사실을 알게 되면 매우 유용할 수 있습니다.

### 27.3.1 Treat Tasks Like Views
>Throughout this book we recommend that views contain as little code as possible, calling methods and functions from other places in the code base. We believe the same thing applies to tasks.

이 책 전반에 걸쳐 우리는 views에 코드 베이스의 다른 위치에서 호출 메서드 및 함수가 가능한 적게 포함되도록 권장합니다. tasks에도 같은 방법을 적용할 수 있습니다.

>A common trap is for the code inside task functions to become long and ugly, because the assumption is that “the task queue hides it from the user.” We’ve been guilty of this ourselves. To avoid this, you can put your task code into a function, put that function into a helper module, and then call that function from a task function.

일반적인 트랩은 task 함수의 코드가 길고 못생겨지는 것인데, 그 이유는 " task queue가 사용자로부터 코드를 숨긴다"는 가정 때문입니다. 이 문제를 방지하려면 task 코드를 함수에 넣고 해당 함수를  helper module에 넣은 후 해당 함수를 태스크 함수로 부터 호출할 수 있습니다.

> All task queue packages do some kind of serialization/abstraction of our task functions and their arguments. This makes debugging them much more difficult. By using our task func- tions to call more easily tested normal functions, we not only make writing and debugging our code easier, we also encourage more reuse.

모든 task queue 패키지는 task 함수와 arguments의 일종의 직렬화/추상 작업을 수행합니다. 이것은 디버깅하는 것을 훨씬 더 어렵게 만듭니다. task 함수를 사용하여 테스트된 일반 함수를 호출함으로써 코드를 더 쉽게 작성하고 디버깅할 수 있을 뿐만 아니라 더 많은 재사용이 가능합니다.

> The same goes for Serverless code. Rather than put a lot of logic into our AWS lambda functions, we create installable, testable packages that we import from. This means a gigantic reduction of production-style debugging.

서버리스 코드도 마찬가지입니다. AWS 람다 함수에 많은 로직을 적용하는 대신 설치 및 테스트 가능한 패키지를 만듭니다. 이는 프로덕션의 디버깅이 크게 감소함을 의미합니다.

### 27.3.2 Tasks Aren’t Free
> Remember that the memory and resources to process a task have to come from somewhere. Overly resource-heavy tasks might be hidden, but they can still cause site problems.

 task를 실행하기 위한 메모리와 리소스도 필요하다는 것을 기억하세요. 리소스를 너무 많이 사용하는 것은 보이지 않지만 여전히 사이트에 문제를 일으킬 수 있습니다.

> Even if resource-intensive code is executed from a task, it should still be written as cleanly as possible, minimizing any unnecessary resource usage. Optimization and profiling can help here.

리소스가 많이 필요로 되는 코드가 task에서 실행되더라도, 불필요한 리소스사용을 최소화하기 위해 가능한 깨끗하게 작성되어야 합니다. 최적화 및 프로파일링이 도움이 될 수 있습니다.

> Even Serverless tasks are not free. Remember, the term ‘Serverless’ is a misnomer, the code is being run in servers. Slow Serverless-tasks can literally run out of time or create a surpris- ingly large bill at the end of the month.

Serverless 작업도 무료가 아닙니다. '서버리스'라는 용어는 잘못된 명칭이며, 코드는 서버에서 실행되고 있습니다. 느린 서버리스 작업은 말 그대로 시간이 부족하거나 월말에는 엄청나게 많은 청구서를 작성할 수 있습니다.

### 27.3.3 Only Pass JSON-Serializable Values to Task Functions
JSON 직렬화 가능한 값만 Task 함수에 전달하세요

> Just like views, for task function arguments, only pass JSON-serializable values. That limits us to integers, floats, strings, lists, tuples, and dictionaries. Don’t pass in complex objects. Here’s why:

보기와 마찬가지로 task 함수 arguments의 경우 JSON 직렬화 가능한 값만 전달합니다. 즉 integers, floats, strings, lists, tuples, dictionaries는 제한합니다. 객체를 넘기지 마세요. 이유는 다음과 같습니다.

> 1.  Passing in an object representing persistent data. For example, ORM instances can cause a race condition. This is when the underlying persistent data changes before the task is run. Instead, pass in a primary key or some other identifier that can be used to call fresh data.
> 2.  Passing in complex objects that have to be serialized into the task queue is time and memory consuming. This is counter-productive to the benefits we’re trying to achieve by using a task queue.
> 3.  We’ve found debugging JSON-serializable values easier than debugging more com- plex objects.
> 4.  Depending on the task queue in use, only JSON-serializable primitives are accepted.

1. 데이터를 나타내는 객체를 전달할 때, 예를 들어 ORM 인스턴스를 함수로 전달할 때 이로 인해 경합 상황이 발생할 수 있습니다. 이것은 task가 실행되기 전에 데이터가 변경될 때입니다. 대신 primary key나 새 데이터를 호출하는 데 사용할 수 있는 다른 식별자를 전달하십시오.
2. task queue에 직렬화해야 하는 객체를 전달하는 데는 시간과 메모리가 많이 소요됩니다. 이는 task queue을 사용하여 달성하려는 이점에 역효과를 가져옵니다.
3. JSON 직렬화 가능한 값을 디버깅하는 것이 더 많은 객체를 디버깅하는 것보다 쉽다는 것을 알게 되었습니다.
4. 사용 중인 task queue에 따라 JSON 직렬화 가능한 요소만 허용됩니다

### 27.3.4 Write Tasks as Idempotent Whenever Possible
가능한 경우 작업을 Idempotent(멱등원)로 작성합니다.

> When we say idempotent (en.wikipedia.org/wiki/Idempotence) we mean that you can run the task multiple times and get the same result. This is important with task queues because retries are expected, even with successfully completed tasks (not uncommon with broker restarts). When a retry, intentional or not, occurs, you want the task to respond with the same result each time it runs.

idempotent (en)이라고 하면요.wikipedia.org/wiki/Idempotence) 어떤 작업을 여러 번 실행하여도 동일한 결과를 얻는 것을 뜻합니다. tasks가 성공적으로 완료된 경우에도 재시도가 예상되기 때문에(브로커가 자주 재시작 되는 것처럼) task queues에서는 이 작업이 중요합니다. 의도적이든 아니든 재시도가 발생하면 태스크가 실행될 때마다 동일한 결과로 응답해야 합니다.

---
### TIP: Pure Functions Over Idempotent Functions

* https://en.wikipedia.org/wiki/Pure_function
* https://stackoverflow.com/questions/4801282/are-idempotent-functions-the-same-as-pure-functions
* https://medium.com/@atipencil/pure-functions-f38f3d49e8b0

> * Nathan Cox, Djangonaut and bleeding edge language enthusiast, encourages us to write tasks using pure functions (en.wikipedia.org/wiki/Pure_function). The main difference being:
 >> * pure functions either do not allow or strongly discourage side effects, while
 >> * idempotent functions don’t mind if there are side effects just so long as the direct result is the same over two function calls. 
> * This may seem like a fine distinction, but it’s worth keeping pure functions in mind when writing idempotent tasks as it encourages us to write more straight-forward task code. Considering the complexity that task queues can bring to a project, we should embrace anything we can do to write cleaner asynchronous code.
 
* 장고노트(Djangonaut)이자 피 흘리는 에지 언어 애호가인 Nathan Cox는 pure functions을 사용하여 작업을 작성하도록 권장합니다. 주요 차이점은 다음과 같습니다.
  * pure functions능은 부작용을 허용하지 않거나 강하게 저지합니다.
  * idempotent 함수는 두 함수 호출에 대한 결과가 같다면 부작용이 있어도 상관없습니다. 
 * 이것은 미세한 구별처럼 보일 수 있지만, idemptent tasks를 작성할 때는 보다 간단한 tasks 코드를 작성하는 것을 권장하므로 pure functions를 염두에 둘 필요가 있습니다. task queues가 프로젝트에 가져올 수 있는 복잡성을 고려하면, 더 깨끗한 비동기 코드를 작성하기 위해 할 수 있는 모든 것을 수용해야 합니다.

---

### 27.3.5 Don’t Keep Important Data in Your Queue
중요한 데이터를 대기열에 보관하지 마십시오.

> Except for Django Channels, all the asychronous task queue options we’ve presented include a built-in retry mechanism. This is great, but sometimes even the retries fail. This can occur for any reason, most commonly bugs within our own code or encountering latency when communicating with third-party APIs. What this means is that critical tasks can fail to run. We’ve seen this occur with billing customers, sending emails, or making reservations.

Django Channels를 제외하고, 우리가 제시한 모든 비동기task queue 옵션에는 재시도 메커니즘이 내장되어 있지만 때때로 재시도도 실패합니다. 이 문제는 어떤 이유로든 발생할 수 있으며, 대부분 자체 코드 내에서 버그가 발생하거나 타사 API와 통신할 때 대기 시간이 발생할 수 있습니다. 즉, 중요한 작업이 실행되지 않을 수 있습니다. 이러한 현상은 청구 고객, 이메일 전송 또는 예약 시 발생합니다.

> The solution is to track the status of an action within the affected record(s). For example, as a customer is about to be billed, mark them as not having been billed yet, then call the task. If the task succeeds, have it update the customer has having been billed. If the task fails, then it will fail to update the customer and a simple query will reveal the customer hasn’t yet paid their bill.

해결책은 영향을 받는 레코드 내에서 동작의 상태를 추적하는 것입니다. 예를 들어, 고객이 청구하려고 할 때 아직 청구되지 않은 것으로 표시한 후 작업을 호출합니다. 작업이 성공하면 고객에게 청구된 내용을 업데이트해야 합니다. 작업이 실패하면 고객을 업데이트하지 못하고 간단한 쿼리로 고객이 아직 요금을 지불하지 않았음을 알 수 있습니다.

> 더 알고싶다면 기사를 참고하세요:
> https://www.caktusgroup.com/blog/2016/10/18/dont-keep-important-data-your-celery-queue/

### 27.3.6 Learn How to Monitor Tasks and Workers
> Gaining visibility into the status of tasks and workers is critical for debugging of task func- tions. Some useful tools:
® Celery: https://pypi.org/project/flower

task 및 Worker의 상태를 시각적으로 확인하는 것은  task 함수의 디버깅에 매우 중요합니다. 유용한 도구는 다음과 같습니다.
* Celery: https://pypi.org/project/flower/


### 27.3.7 Logging!
> Since task queues are working “behind the scenes,” it can be hard to determine exactly what is going on. This is where logging (Chapter 29: Logging: What’s It For, Anyway?) and tools like Sentry become really useful. In error-prone task code, it can be a good idea to log inside of each task function. This will make debugging production code easier.
When using Serverless tasks, we’ve found that Sentry isn’t an option, it is an absolute necessity. When you hit that obscure edge case no amount of logging will capture the depth of data that Sentry provides.

task queues이 "뒤에서" 작동하기 때문에 정확히 무슨 일이 일어나고 있는지 파악하기 어려울 수 있습니다. 여기서 로깅을 수행합니다(29장: 로깅: What It For, Anything?) 및 Sentry와 같은 도구는 매우 유용하게 사용됩니다. 오류가 발생하기 쉬운 task 코드에서는 각 task 함수 내에 log를 남기는 것이 좋습니다. 이렇게 하면 프로덕션 코드를 디버깅하는 것이 쉬워집니다.
서버리스 작업을 사용할 때, 우리는 Sentry가 옵션이 아니라 필수라는 것을 알게 되었습니다.

### 27.3.8 Monitor the Backlog
> As traffic increases, tasks can pile up if there aren’t enough workers. When we see this happening, it’s time to increase the number of workers. This doesn’t apply to Serverless tasks, as that autoscales to fit demand.

트래픽 증가에 따라 workers가 부족하면 업무가 쌓일 수 있습니다. 이런 모습을 볼 때 workers를 늘려야 할 때입니다. 서버리스 tasks에는 수요에 따라 autoscales되므로  적용되지 않습니다.

## 27.3.9 Periodically Clear Out Dead Tasks
> Sometimes a task is passed into a queue and then just sits there doing nothing for some reason. It could be caused by a bug, e.g. a resource being used by the task might no longer exist. However these things happen, they can build up over time, taking up space in our system.

> Learn how your software cleans out dead tasks, and check to make sure it’s running properly. However, this doesn’t apply to Serverless tasks, the environment removes those for you.

어떤 이유로 tasks가 queue에 전달되었다가 아무 것도 하지 않고 그대로 있는 경우가 있습니다. 예를 들어 tasks에서 사용 중인 리소스가 더 이상 존재하지 않을 수 있습니다. 그것들은 시간이 지남에 따라 축적되어 우리 시스템의 공간을 차지할 수 있습니다.

소프트웨어가 불필요한 작업을 정리하고 올바르게 실행되는지 확인합니다. 그러나 Serverless 작업에는 적용되지 않으므로 환경에서 해당 작업을 제거합니다.

### 27.3.10 Ignore Results We Don’t Need
> When a task completes, the broker is designed to record whether it succeeded or failed. While useful for statistical purposes, this exit status is not the result of the job the task was performing. As recording this status takes up time and storage space, it’s a feature we usually turn off.

task가 완료되면 브로커는 성공 여부를 기록하도록 설계되어 있습니다. 통계 목적으로는 유용하지만, 이 종료 상태는 task가 수행 중인 작업의 결과가 아닙니다. 이 상태를 기록하는 것은 시간과 저장 공간을 차지하기 때문에, 일반적으로 해당기능을 꺼두도록 합니다.

### 27.3.11 Use the Queue’s Error Handling
> What happens when a task fails? It can be caused by a network error, a third-party API going down, or anything else that can be imagined. Look up how to do the following for your task queue software and learn how to set them:
® Max retries for a task
® Retry delays
Retry delays deserve a lot of consideration. When a task fails, we like to wait at least 10 seconds before trying again. Even better, if the task queue software allows it, increase the delay each time an attempt is made. We set things this way in order to give the conditions that caused a failure to resolve themselves.

task가 실패하면 어떻게 됩니까? 네트워크 오류, third-party  API의 작동 중단 또는 상상할 수 있는 기타 원인으로 인해 발생할 수 있습니다. task queue  소프트웨어에 대해 다음 작업을 수행하는 방법을 살펴보고 보고 세팅 방법에 대해 알아보십시오.
* task에 대한 최대 재시도 횟수입니다.
* Retry delays 
* Retry delays은 많은 고려가 필요합니다. 
  * task가 실패하면 최소 10초 이상 기다렸다가 다시 시도하는 것이 좋습니다. 
    또한  task queue 소프트웨어가 허용하는 경우 시도를 할 때마다 지연 시간을 늘립니다. 
    이는 스스로 해결할 수 있는 환경을 만들어 줍니다.

### 27.3.12 Learn the Features of Your Task Queue Software
> Celery, Django Channels, and Redis Queue allow for definition of multiple queues. In fact, Celery has fancy routing features that no other software package possesses.

> If we don’t take the time to explore, learn, and use these features, we’re losing out on lots of secret sauce. Staying ignorant of these features can mean that instead of leaning on our package of choice, we end up writing code that duplicates what the package provides.
> In fact, while we’ve become fans of using Boto3 to call AWS Lambda to perform tasks, half the reason we don’t let go of Celery is because it gives us so much control over execution.

Celery, Django Channels, Redis Queue를 사용하여 여러 큐를 정의할 수 있습니다. 사실, Celery는 다른 소프트웨어 패키지가 가지고 있지 않은 화려한 라우팅 기능을 가지고 있습니다.

이러한 기능을 탐색하고 학습하고 사용하지 않으면 수많은 시크릿 소스를 잃게 됩니다.

이러한 특징들에 대해 무지하다는 것은 우리가 선택한 패키지에 의존하는 대신 패키지가 제공하는 것을 복제하는 코드를 작성하게 된다는 것을 의미할 수 있습니다. 
 사실, 우리는 Boto3를 사용하여 AWS Lamda를 호출하여 작업을 수행하지만, Celery를 놓지 않는 이유 중 절반은 Boto3를 사용하여 실행을 제어할 수 있기 때문입니다.
##27.4 Resources for Task Queues
* General
* https://www.vinta.com.br/blog/2016/database-concurrency-in-django-the-right-way/
* https://www.fullstackpython.com/task-queues.html
* https://github.com/carljm/django-transaction-hooks 

* Celery
* https://docs.celeryproject.org/
* https://denibertovic.com/posts/celery-best-practices/
* https://pypi.org/project/flower/ 
* https://wiredcraft.com/blog/3-gotchas-for-celery/
* https://www.caktusgroup.com/blog/tags/celery/
  
* Django Channels
* https://channels.readthedocs.io/en/stable/
* https://github.com/django/channels

## 27.5 Summary
> In this chapter we explored high-level practices for working with task queues. Because of the abstraction involved in using them, we advocate treating them like views, minimizing the amount of business logic within.

> We also covered the use of Serverless tasks through mostly the lens of AWS Lambda. It’s an exciting new way of doing things, but the limitations can be overwhelming.

> In the next chapter, we’ll go over the basics of securing Django projects.

이 장에서는  task queues 작업을 위한 높은 수준의practices를 살펴봤습니다. 이러한 기술을 사용하는 데 수반되는 추상화 때문에, 우리는 비즈니스 로직의 양을 최소화하면서 이러한 기술을 뷰처럼 관리해야 한다고 주장합니다.

또한 서버리스 작업 활용에 대해서도 주로 AWS Lamda 렌즈로 다루었습니다. 그것은 일을 하는 흥미로운 새로운 방법이지만, 한계가 압도적일 수 있습니다.

다음 챕터에서는 장고 프로젝트 보안의 기본에 대해 알아보겠습니다.