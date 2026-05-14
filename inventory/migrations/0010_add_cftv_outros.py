from django.db import migrations

def adicionar_novos_itens(apps, schema_editor):
    Categoria = apps.get_model('inventory', 'Categoria')
    # Adicionando apenas o que falta
    novos_itens = ['Outros', 'Cftv']
    for nome in novos_itens:
        Categoria.objects.get_or_create(nome=nome)

class Migration(migrations.Migration):
    dependencies = [
        # Note que aqui apontamos para a 0009 que você já tem
        ('inventory', '0009_populate_ti_categories'),
    ]
    operations = [
        migrations.RunPython(adicionar_novos_itens),
    ]