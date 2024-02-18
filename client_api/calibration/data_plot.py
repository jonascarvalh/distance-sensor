from ..utils.calibration import Calibration as calib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

PATH_DATA = os.path.join('calibration', 'measures.csv')
df = pd.read_csv(PATH_DATA)

time    = np.array(df['time'])
measure = np.array(df['measure'])
alpha, p = calib.minimos_quadrados(time, measure)

print(f"Coeficiente angular (a): {alpha}")
print(f"Termo independente (p): {p}")

plt.scatter(df['time'], df['measure'], label='Medida', color='red')
plt.plot(df['time'], alpha*df['time'] + p, 'r', label='Linha ajustada', color='blue')
plt.xlabel('Tempo (us)')
plt.ylabel('Distância Real (cm)')
plt.title('Curva de Calibração HC-SR04')
plt.legend()
plt.show()