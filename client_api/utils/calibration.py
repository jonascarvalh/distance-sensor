import numpy as np
import matplotlib.pyplot as plt

class Calibration:
    # Probabilidade t de student para 95% e n graus de liberdade 
    t_student_13graus = 2.160
    t_student_14graus = 2.145

    def __init__(self, entradas, saidas, alpha, p):
        self.entradas = entradas
        self.saidas   = saidas
        self.alpha    = alpha
        self.p        = p
        self.N = len(saidas)

    @staticmethod
    def minimos_quadrados(x, y):
        # Construir a matriz de projeto (design matrix)
        X = np.vstack([x, np.ones_like(x)]).T

        # Calcular os mínimos quadrados
        alpha, p = np.linalg.lstsq(X, y, rcond=None)[0]

        # Retornando coeficiente angular e termo independente
        return alpha, p
    
    # Desvio padrão do erro de ajuste
    def dp_erro_ajuste(self):
        somatorio = 0
        for i in range(self.N):
            somatorio += (self.saidas[i] - self.p - self.alpha*self.entradas[i])**2
        return np.sqrt(1 / (self.N-2) * somatorio)
    
    def variancia_alpha(self, dp_erro):
        somatorio1 = 0
        for i in range(self.N):
            somatorio1 += self.entradas[i]

        somatorio2 = 0
        for i in range(self.N):
            somatorio2 += self.entradas[i]**2

        return (self.N*dp_erro**2) / (self.N * somatorio2 - somatorio1**2)

    def desvio_alpha(self, variancia):
        return np.sqrt(variancia)
    
    def variancia_p(self, dp_erro):
        somatorio1 = 0
        for i in range(self.N):
            somatorio1 += self.entradas[i]

        somatorio2 = 0
        for i in range(self.N):
            somatorio2 += self.entradas[i]**2
        
        return (dp_erro**2 * somatorio2) / (self.N * somatorio2 - somatorio1**2)

    def desvio_p(self, variancia):
        return np.sqrt(variancia)

    def intervalo_confianca(self, t_student, dp_erro):
        return t_student * (dp_erro / np.sqrt(self.N))
    
    def estimativa_mensurando(self, medida):
        return self.alpha*medida + self.p
    
    def incerteza_combinada(self, medida, intervalo_conf, desv_a, desv_p):
        return np.sqrt(
            (self.alpha * intervalo_conf)**2 +
            (medida*desv_a)**2 +
            (1*desv_p)**2
        )
    
    def incerteza_expandida(self, incerteza_comb, t_student):
        return incerteza_comb * t_student