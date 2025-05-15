import pandas as pd
from estoque.models import Produto

def importar_dados():
    df = pd.read_excel('controle epi.xlsx')

    for _, row in df.iterrows():
        Produto.objects.create(
            nome=row['Nome'],
            estoque_fisico=int(row['Estoque']),
            preco_unitario=float(row['Preço'])
        )

if __name__ == '__main__':
    importar_dados()

def importar_planilha():
    df = pd.read_excel('controle epi.xlsx')

    # Substitui NaN por 0 na coluna de estoque
    df['Estoque físico'] = df['Estoque físico'].fillna(0)

    for _, row in df.iterrows():
        Produto.objects.create(
            nome=row['Nome do produto'],
            estoque_fisico=int(row['Estoque físico']),
            estoque_minimo=10,  # valor padrão
            preco_unitario=0.0  # valor padrão
        )

    print("✅ Produtos importados com sucesso!")