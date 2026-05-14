from django.db import migrations


def add_categorias(apps, schema_editor):
    Categoria = apps.get_model('inventory', 'Categoria')
    novas = ['Outros', 'Cftv']
    for nome in novas:
        Categoria.objects.get_or_create(nome=nome)


def remove_categorias(apps, schema_editor):
    Categoria = apps.get_model('inventory', 'Categoria')
    Categoria.objects.filter(nome__in=['Outros', 'Cftv']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_populate_ti_categories'),
    ]

    operations = [
        migrations.RunPython(add_categorias, remove_categorias),
    ]
