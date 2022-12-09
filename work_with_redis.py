import redis
from redis.commands.search.field import TextField



class WorkWithRedis:
    @staticmethod
    def create_index_redis() :
        redisearch_obj = redis.Redis()
        redisearch_obj.flushall()

        s = redisearch_obj.ft("myIdx")
        s.create_index(fields=[TextField("title", weight=5.0), TextField("body"), TextField("url")])

        return redisearch_obj, s

    @staticmethod
    def save_to_redis(redisearch_obj, number, page_info, link):
        title = page_info.title
        body = page_info.body
            
        redisearch_obj.hset(f"doc:{number}", mapping={"title": title, "body": body, "url": link})
        return f"doc:{number} was saved"

    @staticmethod
    def get_resources(phrase_to_search) -> str:
        r = redis.Redis()
        answer = r.ft("myIdx").search(phrase_to_search)
        return answer
    
