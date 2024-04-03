import json
import os
import matplotlib.pyplot as plt
from PIL import Image
import random

def get_image_names(value_list,value_folder):
    filtered_files=[]
    for value in value_list:# Get a list of all files in the folder
        all_files = os.listdir(value_folder)
        filtered_files += [file for file in all_files if file.startswith(value)]
    return [Image.open(os.path.join(value_folder, f"{value}")) for value in filtered_files]

def create_image_grid(json_data, key_image_folder, value_image_folder,max_images_per_row=12):
    sum_=0
    for key, values in json_data.items():
        # Load key image
        key_image_path = os.path.join(key_image_folder, key)
        key_image = Image.open(key_image_path)

        value_images = get_image_names(values,value_image_folder)
        if len(value_images)==0:
            flat_list = [item for sublist in json_data.values() for item in sublist]

            # Get 5 random values
            random_values = random.sample(flat_list, 5) 
            value_images = get_image_names(random_values,value_image_folder)
        try:
            fig, axes = plt.subplots(2, max_images_per_row + 1, figsize=(max_images_per_row, 4), gridspec_kw={'hspace': 0, 'wspace': 0, 'bottom': 0, 'left': 0, 'top': 1})

            axes[0, 0].imshow(key_image)
            # axes[0, 0].axis('off')
            [axes[0, i].axis('off') for i in range(max_images_per_row+1)]
            # axes[0, 0].set_title('Key Image')

            for i, value_image in enumerate(value_images):
                axes[1, i].imshow(value_image)
                [axes[1, i].axis('off') for i in range(max_images_per_row+1)]
                # axes[1, i].set_title(f'Image {i + 1}')
            
            plt.savefig(f'/home/sdavuluri2/workspace/data/layout/layout_{key}')
            plt.close()
            sum_+=1
            print(sum_)    
        except IndexError:
            plt.savefig(f'/home/sdavuluri2/workspace/data/layout/layout_{key}')
            plt.close()
            sum_+=1
            print(sum_)
            # break

with open('/home/sdavuluri2/workspace/code/brandi_app_product_crops_candidates.json', 'r') as file:
        original = json.load(file)

with open('/home/sdavuluri2/workspace/code/brandi_app_product_crops_lbls.json', 'r') as file:
        mapping = json.load(file)       

# Sample JSON data
sample_json = original

# Specify your key and value image folder paths
key_image_folder_path = '/home/sdavuluri2/workspace/data/images'
value_image_folder_path = '/home/sdavuluri2/workspace/data/baby_fact'

# Create the image grid
create_image_grid(sample_json, key_image_folder_path, value_image_folder_path)
