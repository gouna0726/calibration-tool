# Calibration Tool Web App

## Overview
This is a web-based calibration tool designed for analytical chemistry applications. It allows users to:
- Upload an Excel file containing calibration and sample data
- Generate a calibration curve using linear regression
- Perform background correction using blank samples
- Normalize data using internal controls
- Calculate sample concentrations based on the calibration curve
- Visualize the calibration curve with sample data

## Features
✅ Excel file upload for calibration and sample data
✅ Internal control-based normalization
✅ Background correction using blank samples
✅ Automatic sample concentration calculation
✅ Dynamic visualization of calibration data and sample results
✅ One-click downloadable Excel template for easy data entry

## Installation
To run this tool locally, follow these steps:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Flask App
```bash
python app.py
```
✅ The tool will be available at `http://127.0.0.1:5000/`

## Deployment (Render)
To deploy on **Render**, follow these steps:
1. Push all changes to **GitHub**.
2. Connect your repository to **Render**.
3. Set the **Start Command** to:
   ```bash
   gunicorn app:app
   ```
4. Deploy and access your tool online!

## Usage
1️⃣ **Download the Template File** from the web interface.
2️⃣ **Fill in Calibration and Sample Data** in the Excel file.
3️⃣ **Upload the file** to the tool.
4️⃣ **View the calibration curve and calculated sample concentrations**.
5️⃣ **Export results if needed**.

## Technologies Used
- **Python** (Flask, Pandas, NumPy, Scikit-learn)
- **JavaScript** (for dynamic updates)
- **HTML & CSS** (for frontend layout)
- **Matplotlib** (for visualization)
- **Gunicorn** (for deployment)

## Troubleshooting
- **If `gunicorn` is missing on Render**, make sure it's in `requirements.txt` and re-deploy.
- **If the app fails to start**, check `app.py` logs for errors.
- **If you get a 404 error**, confirm `index.html` is in the `templates/` folder.

## Contributors
👤 **Your Name**  Na Gou
📧 Email: gouna0726@gmail.com  
🔗 [GitHub Profile](https://github.com/gouna0726)

## License
📜 MIT License – Free to use and modify!

