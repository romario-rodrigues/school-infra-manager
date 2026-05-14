from django.db import migrations

def popular_categorias(apps, schema_editor):
    Categoria = apps.get_model('inventory', 'Categoria')
    itens = ['Hardware', 'Redes', 'Periféricos', 'Armazenamento', 'Impressoras', 'Nobreaks', 'Cabos', 'Outros', 'Cftv']
    for nome in itens:
        Categoria.objects.get_or_create(nome=nome)

class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0007_itemestoque_preco_unitario'), # Certifique-se que o nome aqui é o da última migração na pasta
    ]

    operations = [
        migrations.RunPython(popular_categorias),
    ]