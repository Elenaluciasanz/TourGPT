# Generated by Django 4.2.10 on 2024-03-10 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_pog'),
        ('planner', '0006_remove_route_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteDayActivityGastronomy',
            fields=[
                ('routedayactivity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='planner.routedayactivity')),
                ('point', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.pog', verbose_name='Point of Gastronomy')),
            ],
            options={
                'verbose_name': 'Gastronomic Activity',
                'verbose_name_plural': 'Gastronomic Activities',
            },
            bases=('planner.routedayactivity',),
        ),
    ]
