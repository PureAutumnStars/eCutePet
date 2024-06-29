# Generated by Django 4.2 on 2024-06-19 22:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsComment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='评论ID', primary_key=True, serialize=False, verbose_name='评论ID')),
                ('rating', models.IntegerField(choices=[(1, '一星'), (2, '两星'), (3, '三星'), (4, '四星'), (5, '五星')], help_text='评分', verbose_name='评分')),
                ('content', models.CharField(default='', help_text='评论内容', max_length=300, verbose_name='评论内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, help_text='修改时间', verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '商品评论',
                'verbose_name_plural': '商品评论',
                'db_table': 'goods_comment',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.CharField(help_text='订单号', max_length=30, primary_key=True, serialize=False, unique=True, verbose_name='订单号')),
                ('order_amount', models.FloatField(default=0.0, help_text='订单金额', verbose_name='订单金额')),
                ('is_sign', models.BooleanField(default=False, help_text='是否签收', verbose_name='是否签收')),
                ('address', models.CharField(help_text='收货地址', max_length=100, verbose_name='收货地址')),
                ('signer_name', models.CharField(default='匿名', help_text='签收人姓名', max_length=20, verbose_name='签收人')),
                ('signer_mobile', models.CharField(help_text='联系电话', max_length=11, verbose_name='联系电话')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
                ('sign_time', models.DateTimeField(blank=True, help_text='签收时间', null=True, verbose_name='签收时间')),
                ('good', models.ForeignKey(help_text='商品名称', on_delete=django.db.models.deletion.CASCADE, related_name='good_order', to='goods.goodsinfo', verbose_name='商品名称')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
                'db_table': 'order_info',
            },
        ),
    ]