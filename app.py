from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Prevent GUI issues
import matplotlib.pyplot as plt
import io
import base64
from sklearn.linear_model import LinearRegression

app = Flask(__name__, template_folder='templates', static_folder='static')

# Function to extract blank control intensity from sample data
def get_blank_control(sample_data):
    blank_rows = sample_data[sample_data['Sample Name'].str.contains('blank', case=False, na=False)]
    if not blank_rows.empty:
        return blank_rows['Normalized Intensity'].mean()  # Use mean if multiple blanks exist
    return 0  # Default to 0 if no blank is found

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        df = pd.read_excel(file, engine='openpyxl')

        # Ensure required columns exist
        required_columns = ['Concentration', 'Intensity', 'Calibration Internal Control', 'Sample Name', 'Sample Intensity', 'Sample Internal Control']
        if not all(col in df.columns for col in required_columns):
            return jsonify({"error": "Invalid file format. Required columns: 'Concentration', 'Intensity', 'Calibration Internal Control', 'Sample Name', 'Sample Intensity', 'Sample Internal Control'"}), 400

        # Extract calibration and sample data
        calibration_data = df[['Concentration', 'Intensity', 'Calibration Internal Control']].dropna()
        sample_data = df[['Sample Name', 'Sample Intensity', 'Sample Internal Control']].dropna()

        # Normalize calibration and sample intensities
        calibration_data['Normalized Intensity'] = calibration_data['Intensity'] / calibration_data['Calibration Internal Control']
        sample_data['Normalized Intensity'] = sample_data['Sample Intensity'] / sample_data['Sample Internal Control']

        # Apply background correction after normalization
        calibration_blank_intensity = calibration_data[calibration_data['Concentration'] == 0]['Normalized Intensity'].mean()
        calibration_data['Corrected Intensity'] = calibration_data['Normalized Intensity'] - calibration_blank_intensity

        # Perform linear regression on normalized calibration data
        X = calibration_data[['Concentration']].values.reshape(-1, 1)
        y = calibration_data[['Corrected Intensity']].values.ravel()
        model = LinearRegression()
        model.fit(X, y)
        slope = model.coef_[0]
        intercept = model.intercept_
        r_squared = model.score(X, y)

        # Apply blank subtraction after normalization
        blank_intensity = get_blank_control(sample_data)
        sample_data['Corrected Intensity'] = sample_data['Normalized Intensity'] - blank_intensity

        # Calculate sample concentrations
        sample_data['Sample Concentration (ppb)'] = (sample_data['Corrected Intensity'] - intercept) / slope
        sample_data = sample_data[~sample_data['Sample Name'].str.contains('blank', case=False, na=False)]
        sample_data = sample_data.drop(columns=['Sample Internal Control'], errors='ignore').to_dict(orient='records')

        # Generate calibration plot
        plt.figure(figsize=(6, 4))
        plt.scatter(X, y, color='blue', label='Calibration Data')
        plt.plot(X, model.predict(X), 'k--', label=f'Fit: y = {slope:.4f}x + {intercept:.4f}, R² = {r_squared:.4f}')
        plt.xlabel('Concentration (ppb)')
        plt.ylabel('Normalized Intensity')
        plt.legend()

        # Save plot as image
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return jsonify({
            "calibration_data": calibration_data.to_dict(orient='records'),
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_squared,
            "plot_url": plot_url,
            "sample_data": sample_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
