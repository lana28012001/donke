# Generated by Django 3.2 on 2022-09-11 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20220910_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pathological',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bệnh lý'),
        ),
    ]
