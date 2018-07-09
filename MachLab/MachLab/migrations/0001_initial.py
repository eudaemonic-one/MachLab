# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-07 14:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=256)),
                ('comment_datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=32)),
                ('model_type', models.IntegerField(blank=True, choices=[(0, 'default'), (1, 'tensorflow'), (2, 'keras'), (3, 'pytorch')], default=(0, 'default'))),
                ('description', models.TextField(blank=True, max_length=256, null=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-modified_datetime'],
            },
        ),
        migrations.CreateModel(
            name='ModelCommit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=256, null=True)),
                ('commit_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-commit_datetime'],
            },
        ),
        migrations.CreateModel(
            name='Modelfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=32)),
                ('file', models.FileField(upload_to='models/')),
                ('description', models.TextField(blank=True, max_length=256, null=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-modified_datetime'],
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=32, unique=True)),
                ('username', models.CharField(max_length=16, unique=True)),
                ('password', models.CharField(max_length=16)),
                ('bio', models.CharField(max_length=256)),
                ('url', models.CharField(max_length=256)),
                ('location', models.CharField(max_length=32)),
                ('avatar', models.FileField(upload_to='static/media/avatar/')),
                ('register_datetime', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=256, null=True)),
                ('url', models.URLField(blank=True, max_length=256, null=True)),
                ('location', models.CharField(blank=True, max_length=32, null=True)),
                ('avatar', models.FileField(blank=True, null=True, upload_to='avatar/')),
                ('register_datetime', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ModelDrop',
            fields=[
                ('modelcommit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='MachLab.ModelCommit')),
            ],
            bases=('MachLab.modelcommit',),
        ),
        migrations.CreateModel(
            name='ModelPull',
            fields=[
                ('modelcommit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='MachLab.ModelCommit')),
            ],
            bases=('MachLab.modelcommit',),
        ),
        migrations.CreateModel(
            name='ModelPush',
            fields=[
                ('modelcommit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='MachLab.ModelCommit')),
                ('push_name', models.CharField(max_length=32)),
            ],
            bases=('MachLab.modelcommit',),
        ),
        migrations.CreateModel(
            name='ModelResult',
            fields=[
                ('modelfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='MachLab.Modelfile')),
                ('result_type', models.IntegerField(choices=[(0, 'default'), (1, '.txt'), (2, '.py'), (3, '.r')], default=(0, 'default'))),
            ],
            bases=('MachLab.modelfile',),
        ),
        migrations.AddField(
            model_name='modelfile',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MachLab.Model'),
        ),
        migrations.AddField(
            model_name='modelcommit',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MachLab.Model'),
        ),
        migrations.AddField(
            model_name='modelcommit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MachLab.Model'),
        ),
        migrations.AddField(
            model_name='comment',
            name='target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MachLab.Comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
