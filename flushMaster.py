import redis
from config import HOST
r = redis.Redis(host=HOST, port=6379, db=0)
print('flushing Redis master ...')
result = r.flushdb()
print(result)
print('Succ ! have a good day :D')