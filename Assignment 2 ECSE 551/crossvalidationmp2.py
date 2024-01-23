# -*- coding: utf-8 -*-
"""CrossValidationMP2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rImTNhLAS3CWDIvhV5o_FY9I39FeHw8P
"""

# ECSE 551 - Mini-Project 2
# Aymen Boustani 260916311, Hamza Chikhaoui 260912960

import numpy as np
import pandas as pd
from collections import Counter

class CrossValidation:

  # Initializes a CrossValidation instance
  def __init__(self, k):
    self.k = k # Number of folds

  # Defines the Accuracy function
  def Accueval(self, compare):
    right = Counter(output[0] == output[1]  for output in compare)[1]
    wrong = Counter(output[0] != output[1]  for output in compare)[1]
    return right / (right + wrong)

  # Defines the validate() function that computes accuracy for each fold among k folds
  def validate(self, model, X, Y, status, labels, nested = False):
      folds = np.array_split(X, self.k, axis = 0)
      classes = np.array_split(Y, self.k)
      assert len(folds) == len(classes)
      l = len(folds)
      avg = 0
      accuracies = {}
      for i in range(l):
        index = l - i - 1
        X_test, Y_test= folds[index], classes[index]
        if not nested:
          X_train, Y_train = np.concatenate(folds[:index] + folds[index + 1:]), np.concatenate(classes[:index] + classes[index + 1:])
          model.fit(X_train, Y_train)
          predicted = model.predict(X_test)
          compare = np.stack((Y_test, predicted), axis = - 1)
          accuracy = self.Accueval(compare)
          avg += accuracy
          if status:
            print(f'Iteration {i + 1} of {self.k} - cross fold on the {model}: Accuracy obtained is {round(accuracy * 100,2)} %')
        if nested:
          avg_n = 0
          for j in range(l - 1):
            index_inner = l - j - 1
            X_test_inner, Y_test_inner= folds[index_inner], classes[index_inner]
            X_train, Y_train = np.concatenate(folds[:index_inner] + folds[index_inner + 1:]), np.concatenate(classes[:index_inner] + classes[index_inner + 1:])
            model.fit(X_train, Y_train)
            predicted = model.predict(X_test_inner)
            compare = np.stack((Y_test_inner, predicted), axis = - 1)
            u = self.Accueval(compare)
            avg_n += u
            if status:
              print(f'Iteration {j + 1} over the {i + 1} subfold of {self.k} - nested cross fold on the {model}: Accuracy obtained is {round(u * 100,2)} %')
          accuracies[index] = avg_n / (l - 1)
      if nested:
        best_k = max(accuracies, key = accuracies.get)
        X_test, Y_test= folds[best_k], classes[best_k]
        X_train, Y_train = np.concatenate(folds[:best_k] + folds[best_k + 1:]), np.concatenate(classes[:best_k] + classes[best_k + 1:])
        model.fit(X_train, Y_train)
        predicted = model.predict(X_test)
        compare = np.stack((Y_test, predicted), axis = - 1)
        avg = self.Accueval(compare)
        print(f'Best accuracy of {model} is : {round(avg * 100,2)} %')
      else:
        avg /= l
        print(f'Averrage accuracy of {model} is : {round(avg * 100,2)} %')
      return avg

# @title Give me a name {display-mode: "form"}

# This code will be hidden when the notebook is loaded.
