## 🚀 Setup Instructions

Follow these steps to set up and run the project:

bash

# Navigate to the scripts folder

```
cd scripts
```

# Create a virtual environment

```
python -m venv venv
```

# Activate the virtual environment

```
source venv/bin/activate    # On Windows use: venv\Scripts\activate
```

# Install required dependencies

```
pip install -r requirements.txt
```

# Open the file qr_templateScriptForSingleIssuance.py and specify the folder path

# that contains your SVG files under the **main** section:

if **name** == "**main**":
folder_path = '../IdCard13' # Change this to your SVG folder path

# Once configured, run the script with:

```
python qr_templateScriptForSingleIssuance.py
```
