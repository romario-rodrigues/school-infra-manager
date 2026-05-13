from django.db import migrations

def create_default_categories(apps, schema_editor):
    Categoria = apps.get_model('inventory', 'Categoria')
    # Garante que exista uma categoria padrão "Outros"
    Categoria.objects.get_or_create(nome='Outros')

def convert_categoria(apps, schema_editor):
    ItemEstoque = apps.get_model('inventory', 'ItemEstoque')
    Categoria = apps.get_model('inventory', 'Categoria')
    # Cria a categoria padrão se não existir
    cat_outros, _ = Categoria.objects.get_or_create(nome='Outros')
    # Para itens que não possuem categoria, atribui "Outros"
    for item in ItemEstoque.objects.filter(categoria__isnull=True):
        item.categoria = cat_outros
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_itemestoque_preco_unitario'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
        migrations.RunPython(convert_categoria),
    ]
