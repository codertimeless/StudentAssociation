# Generated by Django 2.2.8 on 2020-05-22 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentClubUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(max_length=15, unique=True, verbose_name='手机号码')),
                ('username', models.CharField(blank=True, default='TestUser', max_length=15, null=True)),
                ('gender', models.CharField(choices=[('female', '女'), ('male', '男')], max_length=6, verbose_name='性别')),
                ('avatar', models.ImageField(default='/avatar/default_avatar.jpg', upload_to='avatar', verbose_name='头像')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClubUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_name', models.CharField(max_length=10, verbose_name='真实姓名')),
                ('phone_number', models.CharField(max_length=11, verbose_name='手机')),
                ('gender', models.CharField(choices=[('female', '女'), ('male', '男'), ('unknown', '未知')], max_length=7)),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('job', models.CharField(choices=[('指导老师', '指导老师'), ('会长', '会长'), ('副会长', '副会长'), ('成员', '成员'), ('匿名', '匿名'), ('活动管理', '活动管理'), ('论坛管理', '论坛管理'), ('学工处老师', '学工处老师')], default='匿名', max_length=12)),
                ('is_manager', models.BooleanField(default=False)),
                ('student_number', models.CharField(blank=True, max_length=10, null=True, verbose_name='学号')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100, verbose_name='消息内容')),
                ('next_url', models.CharField(max_length=120, verbose_name='详情页面')),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('is_read', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('社联消息', '社联消息'), ('活动消息', '活动消息'), ('论坛消息', '论坛消息')], max_length=4, verbose_name='消息类型')),
                ('from_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='message_from', to=settings.AUTH_USER_MODEL, verbose_name='发送人')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='message_to', to='accounts.ClubUserProfile', verbose_name='接受人')),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
    ]
