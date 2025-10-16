import os
import asyncio
import base64
from io import BytesIO
from PIL import Image
from playwright.async_api import async_playwright

class ChromiumClient:
    @classmethod
    def svg_to_webp(cls, svg_content: bytes, dest_path: str, webp_quality: int = 80) -> str:
        try:
            screenshot_content = asyncio.run(cls.convert_svg_to_png(svg_content))
            
            # Compress the PNG
            compressed_png = cls.compress_png(screenshot_content)
            
            # Save the compressed PNG
            with open(dest_path, 'wb') as f:
                f.write(compressed_png)
            
            # Convert the PNG to WebP
            webp_dest_path, webp_size = cls.png_to_webp(compressed_png, os.path.splitext(dest_path)[0] + '.webp', webp_quality)
            
            # Return the size of the compressed PNG, WebP path, and WebP size
            return len(compressed_png), webp_dest_path, webp_size
        except Exception as error:
            raise Exception(f"Conversion failed: {error}")

    @staticmethod
    async def convert_svg_to_png(svg_content: bytes) -> bytes:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={'width': 1920, 'height': 1080, 'device_scale_factor': 2})

            data_uri = 'data:image/svg+xml;base64,' + base64.b64encode(svg_content).decode('utf-8')
            await page.set_content(f'<img src="{data_uri}" />', wait_until='networkidle')

            screenshot_content = await page.screenshot(type='png', full_page=True)

            await browser.close()
            return screenshot_content

    @staticmethod
    def compress_png(png_content: bytes) -> bytes:
        # Open the PNG image from the byte content
        with Image.open(BytesIO(png_content)) as img:
            # Save the image with optimized settings
            buffer = BytesIO()
            img.save(buffer, format='PNG', optimize=True)
            return buffer.getvalue()

    @staticmethod
    def png_to_webp(png_content: bytes, webp_dest_path: str, quality: int = 80) -> tuple:
        # Open the PNG image from the byte content
        with Image.open(BytesIO(png_content)) as img:
            # Save as WebP with the specified quality
            img.save(webp_dest_path, format='WEBP', quality=quality, method=6)  # method=6 for best compression

        # Get the size of the WebP file
        webp_size = os.path.getsize(webp_dest_path)
        return webp_dest_path, webp_size

def process_directory(directory):
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.svg') and file.startswith('preview'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")

                with open(file_path, 'rb') as svg_file:
                    svg_content = svg_file.read()

                # Get the size of the source SVG file
                svg_size = len(svg_content)

                png_dest_path = os.path.splitext(file_path)[0] + '.png'
                png_size, webp_dest_path, webp_size = ChromiumClient.svg_to_webp(svg_content, png_dest_path)

                # Print the sizes and quality
                print(f"Source SVG size: {svg_size / 1024:.2f} KB")
                print(f"Compressed PNG size: {png_size / 1024:.2f} KB")
                print(f"WebP size: {webp_size / 1024:.2f} KB")
                # print(f"WebP quality setting: {80}")  # Adjusted the quality to your requirement

                # Remove the PNG file after conversion to WebP
                try:
                    os.remove(png_dest_path)
                    print(f"Removed temporary PNG file: {png_dest_path}")
                except Exception as e:
                    print(f"Failed to remove PNG file {png_dest_path}: {e}")

if __name__ == "__main__":
    directory = '/Users/subhrajeetpradhan/Documents/GitHub/credissuer-certificates/degreeTranscript11'
    process_directory(directory)
