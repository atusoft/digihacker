import redis

r = redis.Redis(host='192.168.1.250', port=6379, decode_responses=True)

if __name__ == '__main__':
    keys = r.scan()
    print(keys)
    for key in keys[1]:
        value = r.get(key)
        print(f"{key}:{value.}")
