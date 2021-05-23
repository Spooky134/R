import csv
import os
import random
import ML.AElement
from PIL import Image

import ML.RElement


class Perceptron:
    character_dict = {'A': [0, 1], 'B': [1, 0], 'C': [1, 1]}
    A = []
    connectionTable = []
    lamdas = [list([1] * 500)]
    paths = []
    R = []

    percentage_of_training = 0

    sumDict = {'A': 0, 'B': 0}
    answerDict = {'01': 'A', '10': 'B', '11': 'C'}
    letterDict = {'01': 'Я', '10': 'Д', '11': 'Н'}

    def __init__(self):
        self.gen_connection_table()

        for i in range(500):
            self.A.append(ML.AElement.AElement())

        for i in range(2):
            self.R.append(ML.RElement.RElement())

    def gen_connection_table(self):
        for i in range(2500):
            self.connectionTable.append(list([0] * 500))
        # заполнение по диагонали
        j = 0
        for i in range(500-1, -1, -1):
            self.connectionTable[i][j] = random.choice([1, -1])
            j += 1
        for i in range(500, 2500):
            self.connectionTable[i][random.randint(0, 500 - 1)] = random.choice([1, -1])

    def activate_el(self, imag):
        for i in range(500):
            self.A[i].update_status(imag, [r[i] for r in self.connectionTable])

    def sum_el(self):
        self.sumDict['A'] = 0
        self.sumDict['B'] = 0
        for i in range(250):
            self.sumDict['A'] += self.A[i].lamdas * self.A[i].status
        for i in range(250, 500):
            self.sumDict['B'] += self.A[i].lamdas * self.A[i].status

    def save_lambda(self):
        self.lamdas.append([el.lamdas for el in self.A])

    def update_lambda(self, path_picture):
        expected_value = 0
        if 'A' in path_picture:
            expected_value = self.character_dict['A']
        elif 'B' in path_picture:
            expected_value = self.character_dict['B']
        elif 'C' in path_picture:
            expected_value = self.character_dict['C']

        if self.R[0].status != expected_value[0]:
            if self.R[0].status == 0:
                for i in range(250):
                    if self.A[i].status == 1:
                        self.A[i].lamdas += 1
            elif self.R[0].status == 1:
                for i in range(250):
                    if self.A[i].status == 1:
                        self.A[i].lamdas -= 1

        if self.R[1].status != expected_value[1]:
            if self.R[1].status == 0:
                for i in range(250, 500):
                    if self.A[i].status == 1:
                        self.A[i].lamdas += 1
            elif self.R[1].status == 1:
                for i in range(250, 500):
                    if self.A[i].status == 1:
                        self.A[i].lamdas -= 1


    def update_R(self):
        self.R[0].update_status(self.sumDict['A'])
        self.R[1].update_status(self.sumDict['B'])

    def gen_list_paths(self, directory):
        folder = []
        for files in os.walk(directory):
            folder.append(files)

        for path in folder[0][2]:
            if path != '.DS_Store':
                self.paths.append(directory + '/' + path)

    def percentage_recognition(self, correct_answer, number_of_questions):
        self.percentage_of_training = (correct_answer * 100) / number_of_questions

    def learning(self, path_dataset, recognition_percentage):
        correct_answer = 0
        counter = 0
        self.gen_list_paths(path_dataset)

        while 1:
            random.shuffle(self.paths)
            for j in range(len(self.paths)):
                # активация элементов
                self.activate_el(self.load_image(self.paths[j]))
                # сумматор
                self.sum_el()
                # R элемент
                self.update_R()
                # обновление лямд
                self.update_lambda(self.paths[j])
                # сохраниние лямд в массив
                self.save_lambda()
                # максимальная сумма

                print(self.paths[j])
                ind = ''.join(''.join(str(el.status) for el in self.R))
                if ind != '00':
                    answer = self.answerDict[ind]
                    print(ind,'-',answer)
                    if answer in self.paths[j]:
                        correct_answer += 1
                counter += 1

            self.percentage_recognition(correct_answer, counter)
            if self.percentage_of_training >= recognition_percentage:
                break
            print(self.percentage_of_training)
        self.save_network()

    def recognition(self, path_picture):
        # активация элементов
        self.activate_el(self.load_image(path_picture))
        # сумматор
        self.sum_el()
        # R элемент
        self.update_R()
        ind = ''.join(''.join(str(el.status) for el in self.R))
        answer = self.letterDict[ind]
        print(path_picture)
        print(ind, '-', answer)


    @staticmethod
    def load_image(path):
        image = Image.open(path)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()

        table = list()
        min_table = list()
        for i in range(height):
            for j in range(width):
                a = (pix[j, i][0] + pix[j, i][1] + pix[j, i][2]) / 3
                if a > 0:
                    a = 1
                else:
                    a = 0
                min_table.append(a)
            table.append(list(min_table))
            min_table.clear()
        other = []
        for i in range(len(table)):
            other += table[i]
        return other

    def save_network(self):
        # таблица подключений
        with open('TableCSV/baseTable.csv', "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.connectionTable)

        # таблица лямд
        with open('TableCSV/LamdasTable.csv', "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.lamdas)

    def load_network(self):
        self.lamdas.clear()

        self.connectionTable.clear()
        # таблица подключений
        with open('TableCSV/baseTable.csv', "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                self.connectionTable.append([int(el) for el in row])

        # таблица лямд
        with open('TableCSV/LamdasTable.csv', "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                self.lamdas.append([int(el) for el in row])

    def update_network(self):
        for i in range(500):
            self.A[i].lamdas = self.lamdas[-1][i]
