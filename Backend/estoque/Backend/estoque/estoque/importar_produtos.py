import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # substitua 'backend' pelo nome do seu projeto
django.setup()

from estoque.models import Produto

# Caminho do Excel
caminho_excel = 'controle epi.xlsx'

# Leitura do Excel
df = pd.read_excel(caminho_excel, sheet_name='produtos')

# Inserção no banco
for _, row in df.iterrows():
    Produto.objects.create(
        nome=row['nome'],
        descricao=row.get('descricao', ''),
        quantidade=row['quantidade'],
        estoque_minimo=row.get('estoque_minimo', 0)
    )

print("Importação concluída com sucesso.")
