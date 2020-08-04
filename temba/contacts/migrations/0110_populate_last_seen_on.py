# Generated by Django 2.2.10 on 2020-08-04 15:27

from django.db import migrations, transaction


def last_seen_from_msgs(apps, org):
    Msg = apps.get_model("msgs", "Msg")

    last_seen_by_id = {}

    for msg in Msg.objects.filter(org=org, direction="I").only("contact_id", "created_on"):
        current_last_seen = last_seen_by_id.get(msg.contact_id)
        if not current_last_seen or msg.created_on > current_last_seen:
            last_seen_by_id[msg.contact_id] = msg.created_on

    return last_seen_by_id


def populate_last_seen_on_for_org(apps, org):
    Contact = apps.get_model("contacts", "Contact")

    last_seen_by_id = last_seen_from_msgs(apps, org)

    print(f"   - Calculated {len(last_seen_by_id)} last seen values from messages")

    while last_seen_by_id:
        batch = []
        while len(batch) < 5000:
            try:
                batch.append(last_seen_by_id.popitem())
            except KeyError:
                break

        with transaction.atomic():
            for contact_id, last_seen_on in batch:
                Contact.objects.filter(id=contact_id, last_seen_on=None).update(last_seen_on=last_seen_on)

        print(f"   - Updated {len(batch)} contacts with new last seen values")


def populate_last_seen_on(apps, schema_editor):
    Org = apps.get_model("orgs", "Org")
    num_orgs = Org.objects.filter(is_active=True).count()

    for o, org in enumerate(Org.objects.filter(is_active=True)):
        populate_last_seen_on_for_org(apps, org)

        print(f" > Updated last_seen_on for org '{org.name}' ({o + 1} / {num_orgs})")


def reverse(apps, schema_editor):
    pass


def apply_manual():  # pragma: no cover
    from django.apps import apps

    populate_last_seen_on(apps, None)


class Migration(migrations.Migration):

    dependencies = [
        ("contacts", "0109_contact_last_seen_on"),
    ]

    operations = [migrations.RunPython(populate_last_seen_on, reverse)]
