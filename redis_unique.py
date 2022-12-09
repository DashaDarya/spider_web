from collections import defaultdict
import redis

r = redis.Redis()
r.ping()

d = defaultdict(lambda: 0)

for key in r.keys("doc:*"):
    url = r.hget(key, "url")
    d[url] += 1

print(d)