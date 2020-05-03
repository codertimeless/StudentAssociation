# Generated by Django 2.2.8 on 2020-05-02 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20200502_2016'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_date', models.DateTimeField(auto_created=True)),
                ('real_name', models.CharField(max_length=10, verbose_name='真实姓名')),
                ('phone_number', models.CharField(max_length=11, verbose_name='手机')),
                ('gender', models.CharField(choices=[('female', '女'), ('male', '男')], max_length=6)),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('job', models.CharField(choices=[('teacher', '指导老师'), ('manager', '会长'), ('vicemanager', '副会长'), ('member', '成员'), ('anonymous', '匿名')], max_length=12)),
                ('is_manager', models.BooleanField(default=False)),
                ('student_number', models.CharField(blank=True, max_length=10, null=True, verbose_name='学号')),
                ('club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='management.Club', verbose_name='社团')),
                ('student_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='management.StudentClass', verbose_name='职务')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='management.Unit', verbose_name='单位')),
            ],
        ),
    ]