import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# -------------------- Caminhos dos arquivos --------------------
usuarios_csv = r"C:\Users\gabri\PycharmProjects\IA_final\usuarios.csv"
clientes_csv = r"C:\Users\gabri\PycharmProjects\IA_final\clientes.csv"
empregados_csv = r"C:\Users\gabri\PycharmProjects\IA_final\empregados.csv"
ofertas_csv = r"C:\Users\gabri\PycharmProjects\IA_final\ofertas.csv"
contratos_csv = r"C:\Users\gabri\PycharmProjects\IA_final\contratos.csv"
output_csv = r"C:\Users\gabri\PycharmProjects\IA_final\sistema_completo_ml.csv"

# -------------------- Leitura dos CSVs --------------------
usuarios = pd.read_csv(usuarios_csv)
clientes = pd.read_csv(clientes_csv)
empregados = pd.read_csv(empregados_csv)
ofertas = pd.read_csv(ofertas_csv)
contratos = pd.read_csv(contratos_csv)

# -------------------- Criar a "tabela" Sistema --------------------
sistema_data = {
    'id_sistema': [1],
    'nome': ['Arrumae'],
    'versao': ['1.0'],
    'descricao': ['Sistema de gestão de contratação de serviços domésticos'],
    'total_usuarios': [len(usuarios)],
    'total_clientes': [len(clientes)],
    'total_empregados': [len(empregados)],
    'total_ofertas': [len(ofertas)],
    'total_contratos': [len(contratos)]
}
sistema_df = pd.DataFrame(sistema_data)

# -------------------- Juntar tudo em um DataFrame único --------------------
# Vamos fazer merges com IDs para ter tudo no mesmo DF
clientes_full = pd.merge(clientes, usuarios, left_on='id_usuario', right_on='id_usuario', how='left')
empregados_full = pd.merge(empregados, usuarios, left_on='habilidade_id_usuario', right_on='id_usuario', how='left')
ofertas_full = pd.merge(ofertas, clientes_full, left_on='id_cliente', right_on='id_usuario', how='left')
ofertas_full = pd.merge(ofertas_full, empregados_full, left_on='id_empregado', right_on='habilidade_id_usuario', how='left')
full_df = pd.merge(ofertas_full, contratos, left_on='id_oferta', right_on='id_oferta', how='left')

# -------------------- Pré-processamento --------------------
# 1️⃣ Converter datas
for col in full_df.columns:
    if "data" in col.lower():
        full_df[col] = pd.to_datetime(full_df[col], errors='coerce')
        full_df[col + "_dias"] = (full_df[col] - pd.Timestamp('2020-01-01')).dt.days
        full_df.drop(col, axis=1, inplace=True)

# 2️⃣ Converter strings/categorias para números
label_encoders = {}
for col in full_df.columns:
    if full_df[col].dtype == "object":
        le = LabelEncoder()
        full_df[col] = le.fit_transform(full_df[col].astype(str))
        label_encoders[col] = le

# 3️⃣ Normalizar valores numéricos
numeric_cols = full_df.select_dtypes(include=['int64', 'float64']).columns
scaler = StandardScaler()
full_df[numeric_cols] = scaler.fit_transform(full_df[numeric_cols])

# -------------------- Salvar CSV pronto para ML --------------------
full_df.to_csv(output_csv, index=False)
print(f"Arquivo CSV para ML criado com sucesso: {output_csv}")
print("Shape final:", full_df.shape)
