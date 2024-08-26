# Data set - Seed: https://archive.ics.uci.edu/ml/datasets/seeds

import pandas as pd
from sklearn import preprocessing

# URL do Dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt"

# nomes
# 1. area A,
# 2. perímetro P,
# 3. compactação C = 4*pi*A/P^2,
# 4. length of kernel,
# 5. width of kernel,
# 6. asymmetry coefficient
# 7. length of kernel groove.
# 8. Classificação da semente
names = [ "1", "2", "3", "4", "5", "6", "7", "8"]

# Leitura do dataset usando pandas
seed = pd.read_csv(
  url
  , names=names
  , sep="\t"
  , on_bad_lines='skip'
)
#print(seed)

# apaga dados inválidos
seed.dropna(inplace=True)

# pegar de 0-7, o ultimo deve ser o resultado
X = seed.iloc[:, 0:7]
Y = seed.iloc[:, 7]
# Decode ascii
#label_encoder = preprocessing.LabelEncoder()
#Y = Y.apply(label_encoder.fit_transform)
#print(Y)
#print(X)

# # definindo a rede neural
from sklearn.neural_network import MLPClassifier
# alpha = taxa de aprendizagem
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(7,), random_state=1, max_iter=2000)

# dividindo o dataset de treinamento e teste
# from sklearn.model_selection import train_test_split
# X_treinamento, X_validacao, Y_treinamento, Y_validacao = train_test_split(X, Y, test_size=0.20)
# fazer o treinando, calculando os pesos
clf.fit(X.values, Y.values)

#predicoes = clf.predict(X_validacao)

# from sklearn.metrics import classification_report
# print(classification_report(Y_validacao,predicoes))

print(clf.predict([
  [11.41,12.95,0.856, 5.09, 2.775,4.957, 4.825], # linha qualquer do dataset 
  [10.93,12.8, 0.839, 5.046,2.717,5.398, 5.045],
  [13.84,13.94,0.8955,5.324,3.379,2.259, 4.805],
  [7,7,7,7,7,7,7]
]))