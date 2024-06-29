# 作   者：林枭熠
# 开发时间:2024/6/18 下午6:21

import os

from celery import Celery
from django.conf import settings
from django.utils import timezone

# 设置django的环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'E_djangoProject.settings')

# 创建celery app
app = Celery('E_djangoProject')

# 从django的设置中读取配置信息
app.config_from_object('django.conf:settings', namespace='CELERY')

# 设置时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC时间
app.conf.enable_utc = False

# 发现任务文件每个app下的task.py
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# 解决时区问题,定时任务启动就循环输出
app.now = timezone.now


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# 设置定时任务
# app.conf.beat_schedule = {
#     '更新预约状态': {
#         'task': 'api.appointment.tasks.test',  # 任务函数
#         'schedule': timedelta(seconds=10),  # 每10秒钟执行一次
#         'args': (111, 222)  # 任务函数的参数
#     },
# }
