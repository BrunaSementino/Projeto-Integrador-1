import os
import django
import pandas as pd

# Ajusta o caminho base do projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque.settings')
django.setup()

from estoque.models import Produto

# Caminho para o seu arquivo Excel
CAMINHO_EXCEL = 'caminho/para/seu/arquivo.xlsx'

# Lê os dados do Excel
df = pd.read_excel(CAMINHO_EXCEL)

# Laço para salvar os dados no banco
for _, row in df.iterrows():
    Produto.objects.create(
        nome=row['nome'],
        categoria=row['categoria'],
        quantidade=row['quantidade'],
        validade=row['validade'],
        criado_em=row.get('criado_em')  # use .get() se a coluna for opcional
    )

print("Importação finalizada com sucesso!")
