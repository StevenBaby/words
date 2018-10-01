# Generated by Django 2.0.2 on 2018-02-07 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Paraphrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Paraphrase',
                'verbose_name_plural': 'Paraphrases',
            },
        ),
        migrations.CreateModel(
            name='ParaType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=16, verbose_name='ParaType')),
            ],
            options={
                'verbose_name': 'ParaType',
                'verbose_name_plural': 'ParaTypes',
            },
        ),
        migrations.CreateModel(
            name='Phonetic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=256, null=True, verbose_name='Phonetic')),
            ],
            options={
                'verbose_name': 'Phonetic',
                'verbose_name_plural': 'Phonetics',
            },
        ),
        migrations.CreateModel(
            name='PhoneticType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='NO', max_length=16, verbose_name='PhoneticType')),
            ],
            options={
                'verbose_name': 'PhoneticType',
                'verbose_name_plural': 'PhoneticTypes',
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=16, verbose_name='Rank')),
            ],
            options={
                'verbose_name': 'Rank',
                'verbose_name_plural': 'Ranks',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='First Time')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Update Time')),
                ('review_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Review Time')),
                ('hard_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Hard Time')),
                ('hard', models.IntegerField(default=0, verbose_name='Hard mark')),
                ('level', models.IntegerField(default=0, verbose_name='Review level')),
                ('times', models.IntegerField(default=0, verbose_name='Review times')),
                ('right', models.IntegerField(default=0, verbose_name='Review right times')),
                ('skip', models.IntegerField(default=0, verbose_name='Review skip times')),
                ('error', models.IntegerField(default=0, verbose_name='Review error times')),
                ('review', models.IntegerField(default=0, verbose_name='Review status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Create Time')),
                ('refresh_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Refresh Time')),
                ('title', models.TextField(unique=True, verbose_name='Title')),
                ('star', models.IntegerField(default=0, verbose_name='Star')),
                ('equals', models.ManyToManyField(related_name='_word_equals_+', to='words.Word', verbose_name='Equal word')),
                ('relateds', models.ManyToManyField(related_name='_word_relateds_+', to='words.Word', verbose_name='Related word')),
                ('similars', models.ManyToManyField(related_name='_word_similars_+', to='words.Word', verbose_name='Similar word')),
            ],
            options={
                'verbose_name': 'Word',
                'verbose_name_plural': 'Words',
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='WordType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=16, verbose_name='WordType')),
            ],
            options={
                'verbose_name': 'WordType',
                'verbose_name_plural': 'WordTypes',
            },
        ),
        migrations.AddField(
            model_name='word',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='words.WordType', verbose_name='WordType'),
        ),
        migrations.AddField(
            model_name='review',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='words.Word', verbose_name='Word'),
        ),
        migrations.AddField(
            model_name='rank',
            name='word',
            field=models.ManyToManyField(related_name='ranks', to='words.Word', verbose_name='Word'),
        ),
        migrations.AddField(
            model_name='phonetic',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='words.PhoneticType', verbose_name='PhoneticType'),
        ),
        migrations.AddField(
            model_name='phonetic',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phonetic', to='words.Word', verbose_name='Word'),
        ),
        migrations.AddField(
            model_name='paraphrase',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='words.ParaType', verbose_name='ParaType'),
        ),
        migrations.AddField(
            model_name='paraphrase',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paraphrase', to='words.Word', verbose_name='Word'),
        ),
        migrations.AddIndex(
            model_name='word',
            index=models.Index(fields=['title'], name='words_word_title_6b3d11_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'word')},
        ),
    ]
