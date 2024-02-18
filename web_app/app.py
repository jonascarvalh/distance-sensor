from flask import Flask, render_template, redirect, send_file
import matplotlib.pyplot as plt
from matplotlib import use
from io import BytesIO
import numpy as np
import requests

use('agg')
app = Flask(__name__)
estimativas = [0]
incertezas  = [0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot.png')
def plot_png():
    img_buffer = generate_plot()
    return send_file(img_buffer, mimetype='image/png')

def generate_plot():
    plt.clf()

    ROUTE_API = 'http://127.0.0.1:5000/measure'

    data      = requests.get(ROUTE_API).json()
    medida    = float(data['measure'])
    incerteza = float(data['uncertainty'])

    estimativas.append(medida)
    incertezas.append(incerteza)
    y_err = incertezas
    x = np.arange(len(estimativas))

    # Plot expanded uncertainty
    plt.plot(x, estimativas, label='Estimativa do Mensurando')
    plt.fill_between(x, np.array(estimativas) - np.array(y_err), np.array(estimativas) + np.array(y_err), alpha=0.3, label='Incerteza Expandida')
    plt.xlabel('Medições')
    plt.ylabel('Distância')
    plt.title('Estimativa do Mensurando com Incerteza Expandida')
    plt.legend()

    # Save image
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    return img_buffer

if __name__ == '__main__':
    app.run(port=5001)