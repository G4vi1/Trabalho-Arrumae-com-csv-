import pandas as pd

# Caminhos dos arquivos CSV
usuarios_csv = r"C:\Users\gabri\PycharmProjects\IA_final\usuarios.csv"
clientes_csv = r"C:\Users\gabri\PycharmProjects\IA_final\clientes.csv"
empregados_csv = r"C:\Users\gabri\PycharmProjects\IA_final\empregados.csv"
ofertas_csv = r"C:\Users\gabri\PycharmProjects\IA_final\ofertas.csv"
contratos_csv = r"C:\Users\gabri\PycharmProjects\IA_final\contratos.csv"

# Ler CSVs
usuarios = pd.read_csv(usuarios_csv)
clientes = pd.read_csv(clientes_csv)
empregados = pd.read_csv(empregados_csv)
ofertas = pd.read_csv(ofertas_csv)
contratos = pd.read_csv(contratos_csv)

# Criar DataFrame para o Sistema com atributos do DER + métricas
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

# Salvar tudo em um Excel com múltiplas abas
excel_path = r"C:\Users\gabri\PycharmProjects\IA_final\sistema.xlsx"
with pd.ExcelWriter(excel_path) as writer:
    sistema_df.to_excel(writer, sheet_name='Sistema', index=False)
    usuarios.to_excel(writer, sheet_name='Usuarios', index=False)
    clientes.to_excel(writer, sheet_name='Clientes', index=False)
    empregados.to_excel(writer, sheet_name='Empregados', index=False)
    ofertas.to_excel(writer, sheet_name='Ofertas', index=False)
    contratos.to_excel(writer, sheet_name='Contratos', index=False)

print(f"Arquivo Excel criado com sucesso em: {excel_path}")
