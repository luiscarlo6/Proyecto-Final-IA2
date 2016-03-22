import os 
import cv2
import numpy as np
from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.tools.validation    import CrossValidator, ModuleValidator
from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from numpy.random import multivariate_normal


def ejecutar_red(carpeta_imagenes, nombres_imagenes, class_fun, nro_salida, nro_uni_capa_intermedia, max_iter, entrenamiento):
  n = len(nombres_imagenes)
  m = 1500#porque cada imagen ahora eses un arreglo de 1500
  X = np.zeros(shape = (n, m))
  y = np.zeros(shape = (n, 1))

  for (i, nombre) in enumerate(nombres_imagenes):
    imagen = cv2.imread(carpeta_imagenes+'/' + nombre, cv2.IMREAD_GRAYSCALE)
    klass = class_fun(nombre)
    X[i] = np.ravel(imagen / 255) #se divide entre 255 porque es un pixel cuyos valores son 0 y 255 unicamente.
    y[i] = klass

  all_set = ClassificationDataSet(X.shape[1], nb_classes = nro_salida)

  for i in range(len(X)):
    all_set.addSample(X[i], y[i])
  test_set, train_set = all_set.splitWithProportion( 0.3 )
  train_set._convertToOneOfMany()
  test_set._convertToOneOfMany()

  print("Tipo de entrenamiento: '{}'".format(entrenamiento))
  print("Numero de iteraciones", max_iter)
  print("Numero de imagenes en conjunto de entrenamiento", len(train_set))
  print("Numero de imagenes en conjunto de prueba", len(test_set))
  print("Nro de dimensiones de entrada y salida:", train_set.indim, train_set.outdim)
  print("Neuronas de capa intermedia:", nro_uni_capa_intermedia)

  net = buildNetwork(train_set.indim, nro_uni_capa_intermedia, train_set.outdim, outclass=SoftmaxLayer)
  trainer = BackpropTrainer(net, dataset = train_set)
  # # Crossvalidate de data sets
  # cv = CrossValidator(trainer=trainer, dataset=train_set, n_folds=5) #creates a crossvalidator instance
  # cv.validate() #calls the validate()
  errores_entrenamiento = []
  errores_pruebas = []
  errores = []
  for i in range(max_iter):
      error = trainer.train()
      training_result = percentError(trainer.testOnClassData(dataset = train_set), train_set['class']) / 100
      test_result     = percentError(trainer.testOnClassData(dataset = test_set), test_set['class']) / 100
      print("iteracion: {0:4d}   error_entrenamiento: {1:10.8f}   error_prueba: {2:10.8f}   error: {3:10.8f}"
          .format(trainer.totalepochs, training_result, test_result, error))
      errores_entrenamiento.append(training_result)
      errores_pruebas.append(test_result)
      errores.append(error)

  exitos = [0] * train_set.outdim
  totales = [0] * train_set.outdim
  for i in range(len(test_set['input'])):
    probs = net.activate(test_set['input'][i])
    #prediction = probs.index(max(probs))
    prediction = np.where(probs==max(probs))[0]
    klass = int(test_set['class'][i])
    if prediction == klass:
      exitos[prediction] += 1
    totales[klass] += 1
  for i in range(len(totales)):
    print("Clase: {0:4d}   Totales: {1:4d}   Exitos: {2:4d}   Porcentaje: {3:10.8f}"
          .format(i, totales[i], exitos[i], float(exitos[i])/float(totales[i]) if totales[i]!=0 else 0.0))
  return errores_entrenamiento, errores_pruebas, errores