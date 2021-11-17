def foo(result, index):
    # print('hello {0}'.format(bar))
    
    result[index] = "foo"

from threading import Thread

threads = [None]
results = [None]

for i in range(len(threads)):
    threads[i] = Thread(target=foo, args=(results, i))
    threads[i].start()

# do some other stuff

for i in range(len(threads)):
    threads[i].join()

a = " ".join(results)
print(len(a))
