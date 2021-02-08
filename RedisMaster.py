import redis
import json
from config import HOST
### logger ###
from log.conf_log import logger
class Redis_handler :
    def __init__(self):
        self.r = redis.Redis(host=HOST, port=6379, db=0)

    def get_free_session(self):
        logger.info('getting free session...')
        result = self.r.lpop('available')
        
        logger.info('session imported from query ! {}'.format(result))
        logger.info('free sessions => {}'.format(self.r.llen('available')))
        result = json.loads(result)
        logger.info('free session => {}'.format(result))
        return result

    def get_my_session(self,my_id):
        logger.info('getting MY SESSION...')
        result = self.r.lpop(my_id)
        logger.info('session -> {}'.format(result))
        result = json.loads(result) 
        return result
    
    def save_my_session(self,my_id, session_id, executor_url):
        session = {"session_id":session_id,"executor_url":executor_url} 
        session = str(session).replace("'",'"')
        result = self.r.lpush(my_id,session)
        logger.info('session saved to query ! {}'.format(result))
    
    def init_session(self,session_id,executor_url):
        session = {"session_id":session_id,"executor_url":executor_url}
        session = str(session).replace("'",'"')
        result = self.r.rpush('available',session)
        logger.info('session added to query ! {}'.format(result))
    
    
# redis = Redis_handler()
# # TO SET 
# item = {'amine1':'aydi1','amine2':"aydi2"}

# result = redis.r.lpush('my_id',str(item))

# print(result)
# # TO DELETE
# #redis.r.hdel('test','amine1','amine2')
# # TO GET :
# print(redis.r.llen('availible'))
# #result = redis.r.lpop('availible')
# # print(result)
# # print(dir(redis.r))