# Generated by Django 4.2 on 2023-04-18 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0005_alter_usercourses_status_alter_userleaf_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userleaf',
            name='status',
            field=models.CharField(choices=[('5', 'NOT_INTERESTED'), ('1', 'INTERESTED'), ('2', 'LEARNING'), ('3', 'LEARNED'), ('4', 'VALIDATED')], default='5', max_length=2),
        ),
    ]
