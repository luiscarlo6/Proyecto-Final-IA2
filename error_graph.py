import numpy as np
import sys, getopt, json
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
# Legend code
#line1, = plt.plot([3,2,1], marker='o', label='Line 1')
#line2, = plt.plot([1,2,3], marker='o', label='Line 2')

#plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})

# Se pasan los archivos con los errores, hasta 6 archivos
options = getopt.getopt(sys.argv[1:], "f1:f2:f3:f4:f5:f6:")
errors = []
files = []
tam = []
# Distintos valores para la el dibujo de la grafica
var = ['ro', 'gs', 'bs', 'y--', 'b^']
n = 0
for opt in options:
    for x, y in opt:
        if y != "":
        	files.append(y)

for file in files :
	with open(file,"r") as f:
		x = json.load(f)
		errors.append(x)

# Se crea el vector de puntos a graficar
n = len(errors[0])
i = 0 

while(i != n):
	tam.append(i)
	i += 1
count = 0
# Se agrega el valor de los errores a la grafica
for error in errors:

	plt.plot(tam, error, var[count])
	count += 1

# Se grafica.
plt.axis([0.0, float(len(tam)), 0.0, 0.002])
plt.savefig(f[0] + ".png")