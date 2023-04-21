# Generated by Django 4.2 on 2023-04-20 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0008_alter_userleaf_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gradation',
            field=models.CharField(choices=[('teacher', 'teacher'), ('student', 'student')], default='student', max_length=20),
        ),
        migrations.AlterField(
            model_name='usercourses',
            name='status',
            field=models.CharField(choices=[('ST', 'STARTED'), ('CP', 'COMPLETED'), ('RJ', 'REJECTED')], default='ST', max_length=2),
        ),
        migrations.CreateModel(
            name='Diplomas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tree.course')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
