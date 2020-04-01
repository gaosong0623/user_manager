# -*- coding: utf-8 -*-

from __future__ import unicode_literals
"""
在Python中有些库的接口要求参数必须是str类型字符串，有些接口要求参数必须是unicode类型字符串。
对于str类型的字符串，调用len()和遍历时，其实都是以字节为单位的，这个太坑爹了，同一个字符使用不同的编码格式，长度往往是不同的。
对unicode类型的字符串调用len()和遍历才是以字符为单位，这是我们所要的。
另外，Django，Django REST framework的接口都是返回unicode类型的字符串。
为了统一，我个人建议使用from __future__ import unicode_literals，将模块中显式出现的所有字符串转为unicode类型，不过，对于必须使用str字符串的地方要加以注意。
"""

# 引入django必要模块？
from django.db import migrations, models
import django.db.models.deletion

# 创建字段

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('identity',models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('cls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Classes')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('cls', models.ManyToManyField(to='app01.Classes')),
            ],
        ),
    ]
