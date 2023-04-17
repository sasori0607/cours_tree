# Generated by Django 4.2 on 2023-04-17 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0004_userleaf_unique_user_leaf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourses',
            name='status',
            field=models.CharField(choices=[('ST', 'Начат'), ('CP', 'Закончен'), ('RJ', 'Отказано')], default='ST', max_length=2),
        ),
        migrations.AlterField(
            model_name='userleaf',
            name='status',
            field=models.CharField(choices=[('ST', 'Начат'), ('CP', 'Закончен'), ('RJ', 'Отказано')], default='ST', max_length=2),
        ),
    ]