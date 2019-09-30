# Generated by Django 2.2.5 on 2019-09-30 18:56

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
            name='Affiliation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Expertise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='MediaOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MediaType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_desc', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('section', models.CharField(max_length=45)),
                ('page', models.IntegerField()),
                ('report_text_html', models.TextField()),
                ('author', models.ManyToManyField(to='rate_doc.Author')),
                ('media_org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_doc.MediaOrg')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year_born', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ReportSourceAffiliation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('affiliation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_doc.Affiliation')),
                ('expertise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_doc.Expertise')),
            ],
        ),
        migrations.CreateModel(
            name='ReportSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('affiliation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_doc.ReportSourceAffiliation')),
                ('expertise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_doc.Expertise')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_doc.Report')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_doc.Source')),
            ],
        ),
        migrations.AddField(
            model_name='mediaorg',
            name='media_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_doc.MediaType'),
        ),
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rated', models.BooleanField(default=False)),
                ('rated_date', models.DateTimeField()),
                ('assignedTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_user', to=settings.AUTH_USER_MODEL)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_doc.Report')),
            ],
        ),
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('is_explicit', models.BooleanField()),
                ('is_support', models.BooleanField()),
                ('frame', models.ManyToManyField(to='rate_doc.Frame')),
                ('source', models.ManyToManyField(to='rate_doc.Source')),
            ],
        ),
    ]
