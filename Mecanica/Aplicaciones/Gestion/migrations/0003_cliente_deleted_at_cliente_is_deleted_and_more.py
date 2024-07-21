# Generated by Django 5.0.6 on 2024-07-19 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0002_alter_ordenservicio_servicio_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inspeccion',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inspeccion',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orden',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='servicio',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='servicio',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usuario',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]