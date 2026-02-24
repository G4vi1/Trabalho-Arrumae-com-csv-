import pandas as pd

# Caminho do CSV original
csv_path = r"C:\Users\gabri\PycharmProjects\IA_final\sistema_simples_500.csv"

# Ler CSV
df = pd.read_csv(csv_path)

# ---------- Função de cálculo de preço ajustada ----------
def calcular_preco(distancia, tamanho, residentes, tempo):
    preco_base = 50
    preco = preco_base
    preco += 1 * distancia            # Distância menor impacto
    preco += 0.3 * tamanho            # Tamanho menor impacto
    preco += 10 * residentes          # Número de residentes menor impacto
    preco += 15 * tempo                # Tempo menor impacto
    return round(preco, 2)

# Atualizar a coluna preco_final
df['preco_final'] = df.apply(lambda row: calcular_preco(
    row['distancia_km'],
    row['tamanho_imovel_m2'],
    row['numero_residentes'],
    row['tempo_horas']
), axis=1)

# ---------- Salvar no Excel ----------
excel_path = csv_path.replace('.csv', '_ajustado.xlsx')
df.to_excel(excel_path, index=False)

print(f"Excel atualizado com preços menores salvo em: {excel_path}")
print(df.head())
