from .tasks import longtime_add
import time

if __name__ == '__main__':
    result = longtime_add.delay(1,2)
    print('Task finished? ', result.ready())
    print('Task result: ', result.result)
    time.sleep(10)
    print('Task finished? ', result.ready())
    print('Task result: ', result.result)
