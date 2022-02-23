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

각 task queue 패키지는 고유한 특성이 있지만, 모든 특성에 적용할 수 있는 몇 가지 조건이 있다. 이러한 방법의 장점은 task 기능의 이식성에 도움이 된다는 것입니다. 장고 채널은 유용했지만 재시도 메커니즘이 없기 때문에 셀러리로 전환해야 한다는 사실을 알게 되면 매우 유용할 수 있습니다.

### 27.3.1 Treat Tasks Like Views
>Throughout this book we recommend that views contain as little code as possible, calling methods and functions from other places in the code base. We believe the same thing applies to tasks.

이 책을 통해 우리는 뷰가 가능한 적은 코드를 포함하고 코드 베이스의 다른 곳에서 메소드와 함수를 호출할 것을 권고한다. 우리는 같은 것이 업무에도 적용된다고 믿습니다.

>A common trap is for the code inside task functions to become long and ugly, because the assumption is that “the task queue hides it from the user.” We’ve been guilty of this ourselves. To avoid this, you can put your task code into a function, put that function into a helper module, and then call that function from a task function.

일반적인 트랩은 작업 함수에 있는 코드가 길고 못생겨지는 것인데, 그 이유는 "task queue이 사용자로부터 코드를 숨긴다"는 가정 때문이다. 우리 스스로 죄를 지었어요 이를 방지하려면 작업 코드를 함수에 넣고 해당 함수를 도우미 모듈에 넣은 다음 작업 함수에서 해당 함수를 호출하면 됩니다.

> All task queue packages do some kind of serialization/abstraction of our task functions and their arguments. This makes debugging them much more difficult. By using our task func- tions to call more easily tested normal functions, we not only make writing and debugging our code easier, we also encourage more reuse.

모든 task queue 패키지는 우리의 작업 함수와 인수의 어떤 종류의 직렬화/추상 작업을 한다. 이것은 그것들을 디버깅하는 것을 훨씬 더 어렵게 만든다. 작업 기능을 사용하여 테스트된 일반 함수를 더 쉽게 호출함으로써 코드를 더 쉽게 작성하고 디버깅할 수 있을 뿐만 아니라 더 많은 재사용을 장려한다.

> The same goes for Serverless code. Rather than put a lot of logic into our AWS lambda functions, we create installable, testable packages that we import from. This means a gigantic reduction of production-style debugging.

서버리스 코드도 마찬가지입니다. AWS 람다 함수에 많은 논리를 넣는 대신, 우리는 우리가 가져오는 설치 가능한 테스트 가능한 패키지를 만듭니다. 이는 프로덕션 스타일의 디버깅이 크게 감소함을 의미합니다.




### 27.3.2 Tasks Aren’t Free
> Remember that the memory and resources to process a task have to come from somewhere. Overly resource-heavy tasks might be hidden, but they can still cause site problems.

작업을 처리하기 위한 메모리와 리소스는 어딘가에서 나와야 한다는 것을 기억하라. 리소스가 너무 많이 사용되는 작업은 숨겨질 수 있지만 여전히 사이트 문제를 일으킬 수 있습니다.

> Even if resource-intensive code is executed from a task, it should still be written as cleanly as possible, minimizing any unnecessary resource usage. Optimization and profiling can help here.

비록 자원집약적인 코드가 태스크에서 실행되더라도, 불필요한 자원 사용을 최소화하면서, 가능한 깨끗하게 작성되어야 한다. 최적화 및 프로파일링이 도움이 될 수 있습니다.


> Even Serverless tasks are not free. Remember, the term ‘Serverless’ is a misnomer, the code is being run in servers. Slow Serverless-tasks can literally run out of time or create a surpris- ingly large bill at the end of the month.
### 27.3.3 Only Pass JSON-Serializable Values to Task Functions
> Just like views, for task function arguments, only pass JSON-serializable values. That limits us to integers, floats, strings, lists, tuples, and dictionaries. Don’t pass in complex objects. Here’s why:

1.  Passing in an object representing persistent data. For example, ORM instances can cause a race condition. This is when the underlying persistent data changes before the task is run. Instead, pass in a primary key or some other identifier that can be used to call fresh data.
2.  Passing in complex objects that have to be serialized into the task queue is time and memory consuming. This is counter-productive to the benefits we’re trying to achieve by using a task queue.
3.  We’ve found debugging JSON-serializable values easier than debugging more com- plex objects.
4.  Depending on the task queue in use, only JSON-serializable primitives are accepted.

### 27.3.4 Write Tasks as Idempotent Whenever Possible
> When we say idempotent (en.wikipedia.org/wiki/Idempotence) we mean that you can run the task multiple times and get the same result. This is important with task queues because retries are expected, even with successfully completed tasks (not uncommon with broker restarts). When a retry, intentional or not, occurs, you want the task to respond with the same result each time it runs.

---
### TIP: Pure Functions Over Idempotent Functions
 
> * Nathan Cox, Djangonaut and bleeding edge language enthusiast, encourages us to write tasks using pure functions (en.wikipedia.org/wiki/Pure_function). The main difference being:
 >> * pure functions either do not allow or strongly discourage side effects, while
 >> * idempotent functions don’t mind if there are side effects just so long as the direct result is the same over two function calls. 
> * This may seem like a fine distinction, but it’s worth keeping pure functions in mind when writing idempotent tasks as it encourages us to write more straight-forward task code. Considering the complexity that task queues can bring to a project, we should embrace anything we can do to write cleaner asynchronous code.

---

### 27.3.5 Don’t Keep Important Data in Your Queue
> Except for Django Channels, all the asychronous task queue options we’ve presented include a built-in retry mechanism. This is great, but sometimes even the retries fail. This can occur for any reason, most commonly bugs within our own code or encountering latency when communicating with third-party APIs. What this means is that critical tasks can fail to run. We’ve seen this occur with billing customers, sending emails, or making reservations.

> The solution is to track the status of an action within the affected record(s). For example, as a customer is about to be billed, mark them as not having been billed yet, then call the task. If the task succeeds, have it update the customer has having been billed. If the task fails, then it will fail to update the customer and a simple query will reveal the customer hasn’t yet paid their bill.

> If you want to know more, Dan Poirier of Caktus wrote an excellent article about this technique:
 caktusgroup.com/blog/2016/10/18/dont-keep-important-data-your-celery-queue 27.3.6 Learn How to Monitor Tasks and Workers
Gaining visibility into the status of tasks and workers is critical for debugging of task func- tions. Some useful tools:
® Celery: https://pypi.org/project/flower 27.3.7 Logging!
Since task queues are working “behind the scenes,” it can be hard to determine exactly what is going on. This is where logging (Chapter 29: Logging: What’s It For, Anyway?) and tools like Sentry become really useful. In error-prone task code, it can be a good idea to log inside of each task function. This will make debugging production code easier.
When using Serverless tasks, we’ve found that Sentry isn’t an option, it is an absolute ne- cessity. When you hit that obscure edge case no amount of logging will capture the depth of data that Sentry provides.

### 27.3.8 Monitor the Backlog
> As traffic increases, tasks can pile up if there aren’t enough workers. When we see this happening, it’s time to increase the number of workers. This doesn’t apply to Serverless tasks, as that autoscales to fit demand.

## 27.3.9 Periodically Clear Out Dead Tasks
> Sometimes a task is passed into a queue and then just sits there doing nothing for some reason. It could be caused by a bug, e.g. a resource being used by the task might no longer exist. However these things happen, they can build up over time, taking up space in our system.

> Learn how your software cleans out dead tasks, and check to make sure it’s running properly. However, this doesn’t apply to Serverless tasks, the environment removes those for you.

### 27.3.10 Ignore Results We Don’t Need
> When a task completes, the broker is designed to record whether it succeeded or failed. While useful for statistical purposes, this exit status is not the result of the job the task was performing. As recording this status takes up time and storage space, it’s a feature we usually turn off.

### 27.3.11 Use the Queue’s Error Handling
> What happens when a task fails? It can be caused by a network error, a third-party API going down, or anything else that can be imagined. Look up how to do the following for your task queue software and learn how to set them:
® Max retries for a task
® Retry delays
Retry delays deserve a lot of consideration. When a task fails, we like to wait at least 10 seconds before trying again. Even better, if the task queue software allows it, increase the delay each time an attempt is made. We set things this way in order to give the conditions that caused a failure to resolve themselves.

### 27.3.12 Learn the Features of Your Task Queue Software
> Celery, Django Channels, and Redis Queue allow for definition of multiple queues. In fact, Celery has fancy routing features that no other software package possesses.

> If we don’t take the time to explore, learn, and use these features, we’re losing out on lots of secret sauce. Staying ignorant of these features can mean that instead of leaning on our package of choice, we end up writing code that duplicates what the package provides.
> In fact, while we’ve become fans of using Boto3 to call AWS Lambda to perform tasks, half the reason we don’t let go of Celery is because it gives us so much control over execution.

##27.4 Resources for Task Queues
> General:
® vinta.com.br/blog/2016/database-concurrency-in-django-the-right-way/ Essential reading!
® fullstackpython.com/task-queues.html
® github.com/carljm/django-transaction-hooks
Django database backends that permit registering post-transaction-commit hooks.

> Celery:
® celeryproject.com Homepage of Celery
® denibertovic.com/posts/celery-best-practices/ Must-read article for
anyone learning Celery
® https://pypi.org/project/flower A web-based tool for managing Celery
clusters
® wiredcraft.com/blog/3-gotchas-for-celery
® caktusgroup.com/blog/tags/celery/ The Caktus blog has a number of in-
credibly useful articles on Celery.

> Django Channels
® channels.readthedocs.io Homepage of Django Channels ® github.com/django/channels Source repo

## 27.5 Summary
> In this chapter we explored high-level practices for working with task queues. Because of the abstraction involved in using them, we advocate treating them like views, minimizing the amount of business logic within.

> We also covered the use of Serverless tasks through mostly the lens of AWS Lambda. It’s an exciting new way of doing things, but the limitations can be overwhelming.

> In the next chapter, we’ll go over the basics of securing Django projects.
