import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from flask import Flask, render_template, request


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
    digits = list(range(1, 10))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=digits, y=observed, mode='lines+markers', name='Observed'))
    fig.add_trace(go.Scatter(x=digits, y=expected, mode='lines+markers', name='Expected'))

    fig.update_layout(xaxis_title='Digits', yaxis_title='Counts', title="Benford's Law Distribution",
                      template='plotly_white')

    return fig.to_html(full_html=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)

        observed_counts, expected_counts = benford_law_test(df)
        plot_data = plot_distribution(observed_counts, expected_counts)

        return render_template('index.html', plot_data=plot_data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)