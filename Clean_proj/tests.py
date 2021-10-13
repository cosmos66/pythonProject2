from datetime import datetime
from time import sleep


def filln(func):
    def wrapper(a,*args,**kwargs):
        t1=datetime.now()
        sleep(1)
        a=8
        z=func(a,*args,**kwargs)
        # print(datetime.now()-t1)
        z=z+1 if z==9 else z
        print(f"Finished {func.__name__!r} in {datetime.now()-t1} secs")
        return z

    return wrapper


@filln
def sumsome(a, b):
    return a+b

print(sumsome(5,4))
