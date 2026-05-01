from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_create_default_channels'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.RemoveField(
            model_name='message',
            name='image',
        ),
    ]
