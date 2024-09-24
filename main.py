from rationalbreaks import timers
from time import sleep
from datetime import datetime, timedelta

if __name__ == "__main__":
    timer = timers.RatioNalTimer()
    timer.start()
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    s = 3
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    s = 10
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    timer.rest()
    s = 3
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    s = 3
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    timer.continue_work()
    s = 3
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    s = 3
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    timer.rest()
    s = 3
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    s = 3
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    s = 3
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    timer.continue_work()
    s = 3
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    s = 5
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    timer.rest()
    s = 2
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
    s = 2
    print(f"sleeping for {s}")
    sleep(s)
    print(timer.status())
    print(f"Worked time: {timer.work_time()}")
    print(f"Resting time: {timer.rest_time()}")
