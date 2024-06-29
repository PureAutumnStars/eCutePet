# Generated by Django 4.2 on 2024-06-19 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsfavor',
            name='user',
            field=models.ForeignKey(help_text='用户', on_delete=django.db.models.deletion.CASCADE, related_name='good_favor', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='goodscategory',
            name='parent_category',
            field=models.ForeignKey(blank=True, help_text='父类别目录', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_category', to='goods.goodscategory', verbose_name='父类目级别'),
        ),
        migrations.AddConstraint(
            model_name='goodsfavor',
            constraint=models.UniqueConstraint(fields=('good', 'user'), name='unique_favor_good_user'),
        ),
    ]
