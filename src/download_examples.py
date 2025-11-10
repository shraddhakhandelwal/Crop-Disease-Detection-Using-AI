import os
import urllib.request
import ssl

# Bypass SSL verification (not recommended for production)
ssl._create_default_https_context = ssl._create_unverified_context

def download_example_images():
    """Download example plant disease images from trusted sources."""
    examples_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'examples')
    os.makedirs(examples_dir, exist_ok=True)
    
    # Example image URLs from Plant Village dataset (public domain)
    example_images = {
        'healthy_tomato.jpg': 'https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Tomato___healthy/0a8a68ee-f587-4dea-beec-79d02e7d3fa4___GH_HL_Leaf_Face_251.1.jpg',
        'early_blight.jpg': 'https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Tomato___Early_blight/0a4e2ce6-2445-4c7c-9281-c1e3f0c3f58b___RS_Early.B_8494.JPG',
        'late_blight.jpg': 'https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Tomato___Late_blight/0a5865e0-2727-4114-9dbc-6dbe6d0cc04c___RS_Late.B_5046.JPG'
    }
    
    for filename, url in example_images.items():
        output_path = os.path.join(examples_dir, filename)
        if not os.path.exists(output_path):
            print(f'Downloading {filename}...')
            try:
                urllib.request.urlretrieve(url, output_path)
                print(f'Downloaded {filename}')
            except Exception as e:
                print(f'Error downloading {filename}: {str(e)}')

if __name__ == '__main__':
    download_example_images()