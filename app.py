from flask import Flask, render_template, request, send_file
import pandas as pd
import numpy as np
import pygal
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return 'No file uploaded', 400

    df = pd.read_excel(file)

    # Split calibration and sample data
    calibration_data = df[['Concentration', 'Intensity', 'Calibration Internal Control']].dropna()
    sample_data = df[['Sample Name', 'Sample Intensity', 'Sample Internal Control']].dropna()

    # Normalize calibration data
    calibration_data['Normalized Intensity'] = calibration_data['Intensity'] / calibration_data['Calibration Internal Control']
    calibration_blank = calibration_data[calibration_data['Concentration'] == 0]['Normalized Intensity'].mean()
    calibration_data['Corrected Intensity'] = calibration_data['Normalized Intensity'] - calibration_blank

    # Linear regression
    X = calibration_data[['Concentration']].values
    y = calibration_data['Corrected Intensity'].values
    model = LinearRegression().fit(X, y)
    slope = model.coef_[0]
    intercept = model.intercept_
    r_squared = model.score(X, y)
    detection_limit = 3 * np.std(calibration_data['Corrected Intensity'])

    # Normalize and calculate sample concentrations
    sample_data['Normalized Intensity'] = sample_data['Sample Intensity'] / sample_data['Sample Internal Control']
    blank_intensity = sample_data[sample_data['Sample Name'].str.lower().str.contains('blank')]['Normalized Intensity'].mean()
    sample_data['Corrected Intensity'] = sample_data['Normalized Intensity'] - blank_intensity
    sample_data['Sample Concentration (ppb)'] = (sample_data['Corrected Intensity'] - intercept) / slope

    # Filter out blank rows from sample table
    sample_data = sample_data[~sample_data['Sample Name'].str.lower().str.contains('blank')]

    # Generate plot using Pygal
    chart = pygal.XY(stroke=True)
    chart.title = 'Calibration Curve'
    chart.x_title = 'Concentration (ppb)'
    chart.y_title = 'Corrected Intensity'
    chart.add('Calibration', [(row['Concentration'], row['Corrected Intensity']) for _, row in calibration_data.iterrows()])
    chart.add('Samples', [(np.nan, np.nan)] + [(row['Sample Concentration (ppb)'], row['Corrected Intensity']) for _, row in sample_data.iterrows()])
    min_y = calibration_data['Corrected Intensity'].min()
    max_y = calibration_data['Corrected Intensity'].max()
    chart.add('Detection Limit', [(detection_limit, min_y), (detection_limit, max_y)], stroke_style={'dasharray': '5, 5'})


    plot_path = os.path.join('static', 'calibration_plot.svg')
    chart.render_to_file(plot_path)

    # Prepare data for rendering
    results = {
        'slope': round(slope, 4),
        'intercept': round(intercept, 4),
        'r_squared': round(r_squared, 4),
        'detection_limit': round(detection_limit, 4),
        'sample_data': sample_data.to_dict(orient='records'),
        'plot_url': 'static/calibration_plot.svg'
    }
    return results

@app.route('/download_template')
def download_template():
    return send_file("template_upload.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

application = app