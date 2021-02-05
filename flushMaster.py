import redis
r = redis.Redis(host='161.97.178.112', port=6379, db=0)
print('flushing Redis master ...')
result = r.flushdb()
print(result)
print('Succ ! have a good day :D')