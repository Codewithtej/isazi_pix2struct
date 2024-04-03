import json
import os
import torch
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from PIL import Image
import random
from concurrent.futures import ProcessPoolExecutor

def get_image_names(value_list, value_folder):
    filtered_files = []
    for value in value_list:
        all_files = os.listdir(value_folder)
        filtered_files += [file for file in all_files if file.startswith(value)]
    return [os.path.join(value_folder, f"{value}") for value in filtered_files]

def generate_image(args):
    key, values, key_image_folder, value_image_folder, max_images_per_row = args

    key_image_path = os.path.join(key_image_folder, key)
    key_image = Image.open(key_image_path)

    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Resize images to a fixed size
        transforms.ToTensor(),           # Convert images to PyTorch tensors
    ])

    key_image = transform(key_image).unsqueeze(0)  # Add batch dimension

    value_images = get_image_names(values, value_image_folder)
    if len(value_images) == 0:
        print(f"No images found for values: {values}")
        return

    try:
        fig, axes = plt.subplots(2, min(max_images_per_row, len(value_images)) + 1, figsize=(max_images_per_row, 4), gridspec_kw={'hspace': 0, 'wspace': 0, 'bottom': 0, 'left': 0, 'top': 1})
        axes[0, 0].imshow(key_image.squeeze(0).permute(1, 2, 0))
        [axes[0, i].axis('off') for i in range(min(max_images_per_row, len(value_images)) + 1)]

        for i, value_image_path in enumerate(value_images[:min(max_images_per_row, len(value_images))]):
            value_image = Image.open(value_image_path)
            value_image = transform(value_image).unsqueeze(0)  # Add batch dimension
            axes[1, i].imshow(value_image.squeeze(0).permute(1, 2, 0))
            [axes[1, i].axis('off') for i in range(min(max_images_per_row, len(value_images)) + 1)]

        plt.savefig(f'/home/sdavuluri2/workspace/data/layout/layout_{key}')
        plt.close()
        print(f"Generated layout for {key}")
    except Exception as e:
        print(f"Error generating layout for {key}: {e}")

def create_image_grid(json_data, key_image_folder, value_image_folder, max_images_per_row=12):
    args_list = [(key, values, key_image_folder, value_image_folder, max_images_per_row) for key, values in json_data.items()]

    with ProcessPoolExecutor(max_workers=torch.cuda.device_count()) as executor:
        executor.map(generate_image, args_list)

with open('/home/sdavuluri2/workspace/code/brandi_app_product_crops_candidates.json', 'r') as file:
    original = json.load(file)

with open('/home/sdavuluri2/workspace/code/brandi_app_product_crops_lbls.json', 'r') as file:
    mapping = json.load(file)

sample_json = original
key_image_folder_path = '/home/sdavuluri2/workspace/data/images'
value_image_folder_path = '/home/sdavuluri2/workspace/data/baby_fact'

create_image_grid(sample_json, key_image_folder_path, value_image_folder_path)
