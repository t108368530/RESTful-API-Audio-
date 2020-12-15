from webservice.core.config import message_queue2, settings
import os
path = os.getcwd()
print(path)
print(settings.REDUS_UNIX_SOCKET_PATH)
# settings.REDUS_UNIX_SOCKET_PATH = "../../docker/redis/redis-socket/redis.sock"
# /Users/mbp/Documents/my-project/python-snippets/notebook
print(message_queue2.ping())
# message_queue2.s