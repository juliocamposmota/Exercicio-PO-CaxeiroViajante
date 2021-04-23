from pulp import *
import time, pandas
import more_itertools

#Leitura de dados do excel
dataFrameDistances = pandas.read_excel('Distancias.ods', index_col = 0)
#Transformar os dados em uma Matriz numpy
distancesMatrix = dataFrameDistances.to_numpy()
#Tamanho da matriz
sizeDestinations = len(distancesMatrix)
#Lista com o nome dos locais de destino
destinationsNames = list(dataFrameDistances.columns.values)

#Modelo matemático
problem = pulp.LpProblem("Caixeiro", LpMinimize)

#Declarando variaveis
xMatrix = [[0 for i in range(sizeDestinations)] for j in range(sizeDestinations)] #Matriz de decisão DE PARA
DecisionMatrix = pandas.DataFrame(xMatrix) #Matriz de decisão DE PARA em DataFrame do pandas

#Declaração das variáveis para o pulp
for i in range(sizeDestinations):
  for j in range(sizeDestinations):
    if i != j:
      xMatrix[i][j] = pulp.LpVariable("x"+str(i) + "_" + str(j), cat = "Binary")

#Preparar a expressão da função objetiva para o "problem"
sum = 0
for i in range(sizeDestinations):
  for j in range(sizeDestinations):
    if i != j:
      sum += distancesMatrix[i][j]*xMatrix[i][j]

problem += sum

#Declaração das restrições de saída
departure = 0
for i in range(sizeDestinations):
  departure = 0
  for j in range(sizeDestinations):
    if i != j:
      departure += xMatrix[i][j]
  problem += departure == 1

#Declaracao das restrições de chegada
arrival = 0
for j in range(sizeDestinations):
  arrival = 0
  for i in range(sizeDestinations):
    if i != j:
      arrival += xMatrix[i][j]
  problem += arrival == 1

#Declaração das restrições de eliminação de subrotas
destinationsGroup = range(sizeDestinations)

for subGroup in list(more_itertools.powerset(destinationsGroup)):
  if len(subGroup) >= 2 and len(subGroup) <= sizeDestinations - 1:
    #print("Conjunto: " + str(subGroup))
    restriction = 0
    for i in subGroup:
      # print("Elemento: " + str(i))
      for j in subGroup:
        restriction += xMatrix[i][j]
    problem += restriction <= len(subGroup) - 1

# print(dataFrameDistances)
# print(distancesMatrix)
# print(sizeDestinations)
# print(destinyNames)
# print(xMatrix)
# print(DecisionMatrix)
# print(xMatrix)
# print(problem)

#conta o Tempo Inicial
startTime = time.process_time()
#Função SOLVE
status = problem.solve()
#conta o Tempo Final
finalTime = time.process_time()

totalTime = finalTime - startTime

solution = []
for var in problem.variables():
  if var.varValue != 0:
    solution.append([var.name, var.varValue])
solution.append(['Tempo total do algoritmo: ' + str(totalTime)])

dataFrameSolution = pandas.DataFrame(solution)
# dataFrameSolution.to_excel('Caixeiro Viajante.ods', index = False, header = False)

#Construindo matriz-escolha
choiceMatrix = []
for i in range(sizeDestinations):
  row = []
  for j in range(sizeDestinations):
    if (value(xMatrix[i][j]) != 0):
      row.append(value(xMatrix[i][j]))
    else:
      row.append('')
  choiceMatrix.append(row)
choiceMatrix = pandas.DataFrame(choiceMatrix)

print('\nBREAK POINT\n')
#Caminho ótimo
betterPath = []
for i in range(sizeDestinations):
  path = []
  for j in range(sizeDestinations):
    if (value(xMatrix[i][j]) != 0):
      path = str(xMatrix[i][j]) + "=" + str(value(xMatrix[i][j]))
      print(str(xMatrix[i][j]) + "=" + str(value(xMatrix[i][j])))
    
print('Solução:')
print(solution)

print('\nStatus da solução encontrada: ' + LpStatus[status])

print('\nMatrix Escolha:')
print(choiceMatrix)

print("\nFunção Objetivo: " + str(value(problem.objective)))

print('\nMelhor Caminho:')
# print(betterPath)
