# Generated by Django 3.2 on 2022-08-24 09:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20220824_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailorderproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date created_at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailorderproduct',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date updated_at'),
        ),
        migrations.AddField(
            model_name='detailorderservice',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date created_at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailorderservice',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date updated_at'),
        ),
    ]
