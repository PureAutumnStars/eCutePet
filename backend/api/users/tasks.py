# 作   者：林枭熠
# 开发时间:2024/6/19 下午8:04
from celery import shared_task
from django.core.mail import send_mail

from E_djangoProject import settings


# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s
@shared_task(bind=True, name='send_verify_code', retry_backoff=3)
def send_register_email(self, to_email, verify_code):
    """定义发送验证邮件的任务"""

    # send_mail(‘标题’,'普通邮件正文','发件人','收件人列表','富文本邮件正文（html）')

    subject = 'E萌宠注册邮箱验证'
    html_message = '<p>尊敬的E萌宠用户您好</p>' \
                   '<p>感谢您使用E萌宠平台</p>' \
                   '<p>您的邮箱为：%s。验证码为：%s。</p>' \
                   '<p>如果您未申请注册，请忽略此邮件。</p>' % (to_email, verify_code)
    try:
        send_mail(subject, '', settings.EMAIL_FROM, [to_email], html_message=html_message)
        # send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    except Exception as e:
        # 有异常自动重试三次
        raise self.retry(exc=e, max_retries=3)
