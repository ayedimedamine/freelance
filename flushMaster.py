import redis
from config import HOST
r = redis.Redis(host=HOST, port=49167, db=0, password="my_master_password")
print('flushing Redis master ...')
result = r.delete('available_ovh')
print(result)
print('Succ ! have a good day :D')
