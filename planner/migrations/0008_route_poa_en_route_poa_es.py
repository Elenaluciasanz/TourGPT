# Generated by Django 4.2.10 on 2024-03-18 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_pog'),
        ('planner', '0007_routedayactivitygastronomy'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='poa_en',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='poa_en', to='services.poa', verbose_name='Accommodation Point EN'),
        ),
        migrations.AddField(
            model_name='route',
            name='poa_es',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='poa_es', to='services.poa', verbose_name='Accommodation Point ES'),
        ),
    ]
