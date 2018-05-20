import redis

t = redis.StrictRedis()
t.set('a','bb')

print t.get('a')
