# Generated by Django 1.11.2 on 2017-07-20 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("msgs", "0100_auto_20170614_0915")]

    operations = [
        migrations.AddField(
            model_name="msg", name="uuid", field=models.UUIDField(help_text="The UUID for this message", null=True)
        )
    ]
