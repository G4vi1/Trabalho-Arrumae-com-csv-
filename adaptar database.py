import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# Caminho do arquivo
csv_path = r"C:\Users\gabri\PycharmProjects\IA_final\sistema_completo.csv"

# Tenta ler com utf-8; se falhar, usa latin1
try:
    df = pd.read_csv(csv_path, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(csv_path, encoding='latin1')  # ou encoding='cp1252'

# ---------- 1️⃣ Converter datas ----------
for col in df.columns:
    if "data" in col.lower():  # identifica colunas de data
        df[col] = pd.to_datetime(df[col], errors='coerce')
        df[col + "_dias"] = (df[col] - pd.Timestamp('2020-01-01')).dt.days
        df.drop(col, axis=1, inplace=True)

# ---------- 2️⃣ Converter IDs / strings ----------
label_encoders = {}
for col in df.columns:
    if df[col].dtype == "object":
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

# ---------- 3️⃣ Normalizar valores numéricos ----------
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# ---------- 4️⃣ Separar features e target ----------
if 'preco_final' in df.columns:
    X = df.drop('preco_final', axis=1)
    y = df['preco_final']
else:
    X = df
    y = None

# ---------- 5️⃣ Dividir em treino/teste ----------
if y is not None:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
else:
    X_train, X_test = X, None
    y_train, y_test = None, None

print("Pré-processamento concluído!")
print("Shape X_train:", X_train.shape)
if y is not None:
    print("Shape y_train:", y_train.shape)
