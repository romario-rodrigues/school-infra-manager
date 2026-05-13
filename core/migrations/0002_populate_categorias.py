from django.db import migrations

def populate_categorias(apps, schema_editor):
    Categoria = apps.get_model('core', 'Categoria')
    categorias = [
        'Redes',
        'Periféricos',
        'Armazenamento',
        'Computadores',
        'Cabos/Adaptadores',
        'Impressoras',
        'Nobreaks',
    ]
    for nome in categorias:
        Categoria.objects.get_or_create(nome=nome)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_categorias),
    ]
