# Utilizando .loc e .iloc para seleções
import pandas as pd

import pandas as pd

dados = {
    'Motor': ['Motor 4.0 Turbo', 'Motor Diesel', 'Motor Diesel V8', 'Motor 2.0', 'Motor 1.6'],
    'Ano': [2019, 2003, 1991, 2019, 1990],
    'Quilometragem': [0.0, 5712.0, 37123.0, 0.0, 120000.0],
    'Zero_km': [True, False, False, True, False],
    'Valor': [88000.0, 106000.0, 72000.0, 89000.0, 32000.0]
}

dataset = pd.DataFrame(dados, index = ['Jetta', 'Passat', 'Crossfox', 'DS5', 'Fusca'])

print(dataset.iloc[[1, 3], [0, -1]])
# print(dataset.iloc[['Passat', 'DS5'], ['Motor', 'Valor']]) # Necessita index numéricos
print(dataset.loc[['Passat', 'DS5'], ['Motor', 'Valor']])
# print(dataset.loc[[1, 3], [0, -1]])