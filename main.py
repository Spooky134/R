import csv
import pickle
from ML.Perceptron import Perceptron

FILENAME = "network.dat"


network = Perceptron()
# Обучение
# network.learning('dataset', 85)
# print(network.percentage_of_training)
# распознавание
network.load_network()
network.update_network()



network.recognition('Image/test1.png')
network.recognition('Image/test2.png')
network.recognition('Image/test3.png')
network.recognition('Image/test4.png')
network.recognition('Image/test5.png')
# network.recognition('Image/test6.png')

