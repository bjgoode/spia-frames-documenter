# Generated by Django 2.2.6 on 2019-10-07 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rate_doc', '0003_auto_20190930_1924'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Doc',
            new_name='Review',
        ),
        migrations.AddField(
            model_name='reportsourceaffiliation',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rate_doc.Review'),
        ),
    ]
