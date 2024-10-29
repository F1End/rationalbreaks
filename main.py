from rationalbreaks import timers
from datetime import datetime, timedelta
from time import sleep
from frontend import st_front_objects

if __name__ == "__main__":
    # timer = timers.RatioNalTimer()
    # # timer.start()
    # t = datetime.now()
    # print(type(t))
    # # t2 = isinstance(t, datetime.datetime)
    # # print(t2)
    # sleep(1)
    # t3 = datetime.now() - t
    # print(t3)
    # if t3 < timedelta(seconds=1.5):
    #     print("1")
    # print(timedelta(seconds=5))
    alarm = st_front_objects.Alarm()
    sleep(1)
    alarm.play()
    sleep(5)


