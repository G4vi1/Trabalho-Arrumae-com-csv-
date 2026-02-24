# arquivo: calculadora_preco_fuzzy.py
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ---------- 1️⃣ Definir variáveis fuzzy ----------
distancia = ctrl.Antecedent(np.arange(0, 101, 1), 'distancia')
tamanho = ctrl.Antecedent(np.arange(0, 301, 1), 'tamanho')
residentes = ctrl.Antecedent(np.arange(1, 11, 1), 'residentes')
tempo = ctrl.Antecedent(np.arange(2, 9, 1), 'tempo')
preco = ctrl.Consequent(np.arange(50, 501, 1), 'preco')

# ---------- 2️⃣ Funções de pertinência ----------
distancia['perto'] = fuzz.trimf(distancia.universe, [0, 0, 30])
distancia['moderado'] = fuzz.trimf(distancia.universe, [20, 50, 80])
distancia['longe'] = fuzz.trimf(distancia.universe, [60, 100, 100])

tamanho['pequeno'] = fuzz.trimf(tamanho.universe, [0, 0, 100])
tamanho['medio'] = fuzz.trimf(tamanho.universe, [50, 150, 250])
tamanho['grande'] = fuzz.trimf(tamanho.universe, [200, 300, 300])

residentes['individual'] = fuzz.trimf(residentes.universe, [1, 1, 2])
residentes['casal'] = fuzz.trimf(residentes.universe, [2, 3, 4])
residentes['familia'] = fuzz.trimf(residentes.universe, [4, 5, 6])
residentes['grande_familia'] = fuzz.trimf(residentes.universe, [6, 10, 10])

tempo['rapido'] = fuzz.trimf(tempo.universe, [2, 2, 4])
tempo['medio'] = fuzz.trimf(tempo.universe, [3, 5, 7])
tempo['longo'] = fuzz.trimf(tempo.universe, [6, 8, 8])

preco['baixo'] = fuzz.trimf(preco.universe, [50, 50, 150])
preco['medio'] = fuzz.trimf(preco.universe, [100, 250, 400])
preco['alto'] = fuzz.trimf(preco.universe, [300, 400, 500])
preco['muito_alto'] = fuzz.trimf(preco.universe, [450, 500, 500])

# ---------- 3️⃣ Regras fuzzy ----------
rules = [
    ctrl.Rule(distancia['perto'] & tamanho['pequeno'] & residentes['individual'], preco['baixo']),
    ctrl.Rule(distancia['moderado'] | tamanho['medio'] | residentes['casal'], preco['medio']),
    ctrl.Rule(distancia['longe'] | tamanho['grande'] | residentes['grande_familia'], preco['alto']),
    ctrl.Rule(tempo['longo'], preco['muito_alto'])
]

# ---------- 4️⃣ Controlador ----------
preco_ctrl = ctrl.ControlSystem(rules)
preco_simulador = ctrl.ControlSystemSimulation(preco_ctrl)

# ---------- 5️⃣ Input do usuário ----------
dist = float(input("Distância (km) [0-100]: "))
tam = float(input("Tamanho do imóvel (m²) [0-300]: "))
res = float(input("Número de residentes [1-10]: "))
temp = float(input("Tempo desejado (horas) [2-8]: "))

preco_simulador.input['distancia'] = dist
preco_simulador.input['tamanho'] = tam
preco_simulador.input['residentes'] = res
preco_simulador.input['tempo'] = temp

preco_simulador.compute()
print(f"Preço estimado (fuzzy): R$ {preco_simulador.output['preco']:.2f}")
