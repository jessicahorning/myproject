from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

def benford_law_test(data):
    observed_counts = [0] * 9
    total_count = 0
    for value in data['7_2009']:
        if value != 0:
            first_digit = int(str(value)[0])
            observed_counts[first_digit - 1] += 1
            total_count += 1

    expected_counts = [total_count * np.log10(1 + 1/digit) for digit in range(1, 10)]

    return observed_counts, expected_counts

def plot_distribution(observed, expected):
    digits = range(1, 10)
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(digits, observed, width, label='Observed')
    ax.bar(digits, expected, width, label='Expected')

    ax.set_xlabel('Digits')
    ax.set_ylabel('Counts')
    ax.set_title('Benford\'s Law Distribution')

    ax.legend()
    plt.xticks(digits)
    plt.grid(True)

    return plt

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)

        observed_counts, expected_counts = benford_law_test(df)

        plot = plot_distribution(observed_counts, expected_counts)
        plot_path = 'static/plot.png'
        plot.savefig(plot_path)

        return render_template('index.html', plot_path=plot_path)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
