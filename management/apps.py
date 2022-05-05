from django.apps import AppConfig
from django.conf import settings
from .utils.redis_utils import RedisUtils
import os


class ManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'management'

    def ready(self):
        if not os.environ.get('RUN_MAIN'):
            from .bot import check_bot
            # 项目启动的时候会来执行这个方法
            bot = check_bot.CheckBot()
            bot.start()
            os.environ['RUN_MAIN'] = '1'
