from flask import Flask, render_template, request
import numpy as np
from statistics import mode, median
import matplotlib.pyplot as plt
import re
import os

app = Flask(__name__)

def extract_numbers(text):
    numbers = re.findall(r'-?\d+\.?\d*', text)
    return list(map(float, numbers))

def calculate_stats(numbers):
    return {
        "Mean": np.mean(numbers),
        "Median": median(numbers),
        "Mode": mode(numbers),
        "Count": len(numbers),
        "Min": min(numbers),
        "Max": max(numbers),
    }

import os  # Make sure this import is at the top of your app.py file

def save_plot(numbers):
    # Create the 'static' directory if it doesn't exist
    os.makedirs("static", exist_ok=True)

    plt.figure(figsize=(8, 4))
    plt.hist(numbers, bins=10, color='skyblue', edgecolor='black')
    plt.title("Number Distribution")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.grid(True)

    plot_path = os.path.join("static", "plot.png")
    plt.savefig(plot_path)
    plt.close()

    return plot_path


@app.route('/', methods=['GET', 'POST'])
def index():
    stats = {}
    numbers = []
    plot_path = None
    if request.method == 'POST':
        input_text = request.form['inputText']
        numbers = extract_numbers(input_text)
        if numbers:
            stats = calculate_stats(numbers)
            plot_path = save_plot(numbers)
    return render_template('index.html', stats=stats, plot_path=plot_path, numbers=numbers)

if __name__ == '__main__':
    app.run(debug=True)
