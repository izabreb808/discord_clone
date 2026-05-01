from django.db import migrations


def create_default_channels(apps, schema_editor):
    Channel = apps.get_model('chat', 'Channel')
    for name in ['ogolny', 'prywatny']:
        Channel.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message_image_alter_message_content'),
    ]

    operations = [
        migrations.RunPython(create_default_channels, migrations.RunPython.noop),
    ]
