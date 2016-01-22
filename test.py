from django.core.cache import cache

def a():
    cache.set(1,2)
    print "I was in A"
    print cache.get(1)

def b():
    print "I was in B"
    if cache.get(1):
        print cache.get(1)
    else:
        print "Nothing"
