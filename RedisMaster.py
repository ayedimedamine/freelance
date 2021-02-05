import redis
import json
class Redis_handler :
    def __init__(self):
        self.r = redis.Redis(host='161.97.178.112', port=6379, db=0)

    def get_free_session(self):
        print('getting free session...')
        result = self.r.lpop('available')
        
        print('session imported from query ! ',result)
        print('free sessions =>',self.r.llen('available'))
        result = json.loads(result)
        print('free session => ',result)
        return result

    def get_my_session(self,my_id):
        print('getting MY SESSION...')
        result = self.r.lpop(my_id)
        print('session ->', result)
        result = json.loads(result) 
        return result
    
    def save_my_session(self,my_id, session_id, executor_url):
        session = {"session_id":session_id,"executor_url":executor_url} 
        session = str(session).replace("'",'"')
        result = self.r.lpush(my_id,session)
        print('session saved to query !',result)
    
    def init_session(self,session_id,executor_url):
        session = {"session_id":session_id,"executor_url":executor_url}
        session = str(session).replace("'",'"')
        result = self.r.rpush('available',session)
        print('session added to query !',result)
    
    
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