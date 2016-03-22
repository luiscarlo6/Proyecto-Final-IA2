import sys, getopt, json, os
from red import ejecutar_red

def is_rest(filename):
    return 1 if "rest" in filename else 0

def which_pitch(filename):
  if "a-" in filename: return 0
  elif "h-" in filename: return 1
  elif "c1-" in filename: return 2
  elif "d1-" in filename: return 3
  elif "e1-" in filename: return 4
  elif "f1-" in filename: return 5
  elif "g1-" in filename: return 6
  elif "a1-" in filename: return 7
  elif "h1-" in filename: return 8
  elif "c2-" in filename: return 9
  elif "d2-" in filename: return 10
  elif "e2-" in filename: return 11
  elif "f2-" in filename: return 12
  elif "g2-" in filename: return 13
  elif "a2-" in filename: return 14
  elif "h2-" in filename: return 15
  elif "c3-" in filename: return 16

def which_duration(filename):
  if "whole" in filename: return 0
  elif "half" in filename: return 1
  elif "quarter" in filename: return 2
  elif "eighth" in filename: return 3
  elif "sixteenth" in filename: return 4
  

if len(sys.argv) != 5:
  print('Uso: ')
  print('python main.py <carpeta_imagenes> <nro_uni_capa_intermedia> <max_iter> <entrenamiento>')
  print('entrenamiento:')
  print('\tsymbol: para clasificar entre notes y rest')
  print('\tnote_duration: para clasificar entre distintas duraciones de notas: whole, half, quarter, eighth y sixteenth ')
  print('\trest_duration: para clasificar entre distintas duraciones de rest: whole, half, quarter, eighth y sixteenth ')
  print('\tpitch: para clasificar los pitch de las notas: a, h, c1, d1, e1, f1, g1, a1, h1, c2, d2, e2, f2, g2, a2, h2, c3, other')
  sys.exit()

carpeta_imagenes = sys.argv[1]
nro_uni_capa_intermedia = int(sys.argv[2])
max_iter = int(sys.argv[3])
entrenamiento = str(sys.argv[4])

if entrenamiento == "symbol":
  nombres_imagenes = [f for f in os.listdir('./' + carpeta_imagenes)]
  class_fun = is_rest
  nro_salida = 2
elif entrenamiento == "pitch":
  nombres_imagenes = [f for f in os.listdir('./' + carpeta_imagenes) if ("note" in f) and ("other" not in f)]
  class_fun = which_pitch
  nro_salida = 17
elif entrenamiento == "note_duration":
  nombres_imagenes = [f for f in os.listdir('./' + carpeta_imagenes) if ("note" in f) and ("other" not in f)]
  class_fun = which_duration
  nro_salida = 5
elif entrenamiento == "rest_duration":
  nombres_imagenes = [f for f in os.listdir('./' + carpeta_imagenes) if "rest" in f]
  class_fun = which_duration
  nro_salida = 5
else:
  print("Argumento incorrecto en <entrenamiento>.")

ejecutar_red(carpeta_imagenes, nombres_imagenes, class_fun, nro_salida, nro_uni_capa_intermedia, max_iter, entrenamiento)
