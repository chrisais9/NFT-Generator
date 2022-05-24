import pathlib
from PIL import Image
import multiprocessing
from multiprocessing import Pool

import constant


class ImageGenerator:
    def __init__(self, config):
        self.config = config

        self.width = config["size"]["width"]
        self.height = config["size"]["height"]

    def parse_image_directory(self, trait):

        image_path = dict.fromkeys(self.config["order"])

        full_type = trait["type"]
        gender_type = full_type.split("_", 1)[0]

        for trait_name, value in trait.items():
            # parse path by full type (xx_diamond)
            if pathlib.Path(f"layer/{trait_name}/{full_type}/{value}.png").exists():
                image_path[trait_name] = f"layer/{trait_name}/{full_type}/{value}.png"
            # parse path by type (xx)
            if pathlib.Path(f"layer/{trait_name}/{gender_type}/{value}.png").exists():
                image_path[trait_name] = f"layer/{trait_name}/{gender_type}/{value}.png"
                if f"h_{trait_name}" in image_path:
                    image_path[f"h_{trait_name}"] = f"layer/{trait_name}/{gender_type}/{value}.png"
            # if type doesn't exist, get path from common
            elif pathlib.Path(
                    f"layer/{trait_name}/common/{value}.png").exists():
                image_path[trait_name] = f"layer/{trait_name}/common/{value}.png"

                if f"h_{trait_name}" in image_path:
                    image_path[f"h_{trait_name}"] = f"layer/h_{trait_name}/common/{value}.png"
            else:  # error
                print(trait_name, full_type, gender_type, value, "error")

        return image_path

    def merge_image_layer(self, trait):
        print(f"merge {trait}")
        image_layer_path = self.parse_image_directory(trait)

        stack = Image.new('RGBA', (self.width, self.height))

        for layer, path in image_layer_path.items():
            if layer == constant.CONFIG_HAIR or layer == constant.CONFIG_HIDDEN_HAIR:
                if trait[constant.CONFIG_HEADGEAR] == "none":
                    image_layer = Image.open(path).convert('RGBA')
                    stack = Image.alpha_composite(stack, image_layer)
            elif layer == constant.CONFIG_HIDDEN_HEADGEAR_HAIR:
                if trait[constant.CONFIG_HEADGEAR] != "none":
                    image_layer = Image.open(path).convert('RGBA')
                    stack = Image.alpha_composite(stack, image_layer)
            else:
                image_layer = Image.open(path).convert('RGBA')
                stack = Image.alpha_composite(stack, image_layer)

        filter = Image.open(image_layer_path[constant.CONFIG_BACKGROUND]).convert('RGBA')
        filter.putalpha(filter.getchannel('A').point(lambda x: x * 0.1))
        stack = Image.alpha_composite(stack, filter)

        stack = stack.convert('RGB')
        return stack

    def generate(self, traits):
        print(f"multi threading with {multiprocessing.cpu_count()} CPUs")
        pool = Pool(processes=multiprocessing.cpu_count())
        images = pool.map(self.merge_image_layer, traits)
        pool.close()
        pool.join()

        print("merge images done")

        token_id = 1
        for image in images:
            image.save(f'./images/{token_id}.jpeg')
            print(f"saved {token_id}")

            token_id += 1
