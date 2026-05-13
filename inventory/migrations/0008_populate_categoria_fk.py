from django.db import migrations

def convert_categoria(apps, schema_editor):
    ItemEstoque = apps.get_model('inventory', 'ItemEstoque')
    Categoria = apps.get_model('core', 'Categoria')
    mapping = {
        'Rede': 'Redes',
        'Periférico': 'Periféricos',
        'Armazenamento': 'Armazenamento',
        'Computador': 'Computadores',
        'Cabo/Adaptador': 'Cabos/Adaptadores',
        'Impressora': 'Impressoras',
        'Nobreak': 'Nobreaks',
        'OUT': None,
    }
    for item in ItemEstoque.objects.all():
        old_cat = item.categoria  # string
        new_name = mapping.get(old_cat)
        if new_name:
            cat_obj = Categoria.objects.filter(nome=new_name).first()
            if cat_obj:
                item.categoria = cat_obj
            else:
                item.categoria = None
        else:
            item.categoria = None
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_itemestoque_preco_unitario'),
        ('core', '0002_populate_categorias'),
    ]

    operations = [
        migrations.RunPython(convert_categoria),
    ]
