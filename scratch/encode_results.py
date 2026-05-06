import base64
import os

def encode_image_to_txt(img_path, txt_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        with open(txt_path, "w") as text_file:
            text_file.write(encoded_string)
        print(f"Encoded {img_path} to {txt_path}")
    else:
        print(f"File {img_path} not found")

os.makedirs('results', exist_ok=True)
encode_image_to_txt('results/opex_var_histogram.png', 'results/opex_var_histogram.txt')
encode_image_to_txt('results/variance_comparison.png', 'results/variance_comparison.txt')
