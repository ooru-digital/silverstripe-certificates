# SVG to WebP Converter

This project converts SVG files to PNG and then compresses them to WebP format. It uses Playwright to render SVG files and PIL (Pillow) to handle image compression.

## Requirements

Before running the script, you need to install the required dependencies. You can find the list of dependencies in the `requirements.txt` file.

## Setup

1. **Move to directory:**

    ```bash
    cd <directory>
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install Playwright dependencies:**

    Playwright requires additional browser binaries to be installed. Run the following command to install them:

    ```bash
    playwright install
    ```

## Usage

1. **Update the path in `convert.py`:**

    Open the `convert.py` file and update the `directory` variable to point to the directory containing your SVG files.

    ```python
    if __name__ == "__main__":
        directory = '/path/to/your/svg/files'  # Update this path
        process_directory(directory)
    ```

2. **Run the script:**

    Execute the script to convert SVG files to PNG and then to WebP format:

    ```bash
    python convert.py
    ```

## Notes

- Ensure that the SVG files are named with the prefix `preview` and have the `.svg` extension.
- The script will process all matching SVG files in the specified directory and its subdirectories.

## Troubleshooting

- If you encounter issues with Playwright, ensure that you have all necessary system dependencies installed and that you have run `playwright install` to set up the browsers.
- For issues related to image conversion or file handling, verify that the paths are correctly specified and that you have the required permissions to read and write files.

