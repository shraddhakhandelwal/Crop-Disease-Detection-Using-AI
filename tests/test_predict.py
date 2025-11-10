import os
from src.utils import preprocess_image


def test_preprocess_shape():
    # create a tiny image to test
    from PIL import Image
    p = 'tests/tmp_test_img.jpg'
    os.makedirs('tests', exist_ok=True)
    Image.new('RGB', (100, 200), color=(255,0,0)).save(p)
    arr = preprocess_image(p, target_size=(224,224))
    assert arr.shape == (1, 224, 224, 3)
    os.remove(p)
