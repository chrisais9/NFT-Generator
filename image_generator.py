import pathlib
from PIL import Image
import multiprocessing
from multiprocessing import Pool
import tqdm
import constant


class ImageGenerator:
    def __init__(self, config):
        self.config = config

        self.width = config["size"]["width"]
        self.height = config["size"]["height"]

    def parse_image_directory(self, trait):

        image_path = dict.fromkeys(self.config["order"])

        full_type = trait[constant.CONFIG_TYPE].lower()
        gender_type = full_type.split(" ", 1)[0]

        for trait_name, value in trait.items():
            if trait_name == "token_id":
                continue
            # parse path by full type (xx_diamond)
            if pathlib.Path(f"layer/{trait_name}/{full_type}/{value}.png").exists():
                image_path[trait_name] = f"layer/{trait_name}/{full_type}/{value}.png"
                if f"h_{trait_name}" in image_path:
                    image_path[f"h_{trait_name}"] = f"layer/h_{trait_name}/{full_type}/{value}.png"
            # parse path by type (xx)
            elif pathlib.Path(f"layer/{trait_name}/{gender_type}/{value}.png").exists():
                image_path[trait_name] = f"layer/{trait_name}/{gender_type}/{value}.png"
                if f"h_{trait_name}" in image_path:
                    image_path[f"h_{trait_name}"] = f"layer/h_{trait_name}/{gender_type}/{value}.png"
            # if type doesn't exist, get path from common
            elif pathlib.Path(
                    f"layer/{trait_name}/common/{value}.png").exists():
                image_path[trait_name] = f"layer/{trait_name}/common/{value}.png"

                if f"h_{trait_name}" in image_path:
                    image_path[f"h_{trait_name}"] = f"layer/h_{trait_name}/common/{value}.png"
            else:  # error
                print(trait_name, full_type, gender_type, value, "error", sep=" - ")
                return None

        return image_path

    def merge_image_layer(self, trait):

        image_layer_path = self.parse_image_directory(trait)
        stack = Image.new('RGBA', (self.width, self.height))

        for layer, path in image_layer_path.items():
            if layer == constant.CONFIG_HAIR or layer == constant.CONFIG_HIDDEN_HAIR:
                if trait[constant.CONFIG_HEADGEAR] == constant.CONFIG_VALUE_NONE:
                    image_layer = Image.open(path).convert('RGBA')
                    stack = Image.alpha_composite(stack, image_layer)
                else:
                    pass
            elif layer == constant.CONFIG_HIDDEN_HEADGEAR_HAIR:
                if trait[constant.CONFIG_HEADGEAR] != constant.CONFIG_VALUE_NONE:
                    image_layer = Image.open(path).convert('RGBA')
                    stack = Image.alpha_composite(stack, image_layer)
                else:
                    pass
            else:
                image_layer = Image.open(path).convert('RGBA')
                stack = Image.alpha_composite(stack, image_layer)

        filter = Image.open(image_layer_path[constant.CONFIG_BACKGROUND]).convert('RGBA')
        filter.putalpha(filter.getchannel('A').point(lambda x: x * 0.1))
        stack = Image.alpha_composite(stack, filter)

        stack = stack.convert('RGB')
        stack.save(f'./images/{trait["token_id"]}.png')

    def generate(self, traits):
        print(f"multi threading with {multiprocessing.cpu_count()} CPUs")

        pool = Pool(processes=multiprocessing.cpu_count())
        for _ in tqdm.tqdm(pool.imap_unordered(self.merge_image_layer, traits), total=len(traits), unit=" image"):
            pass
        pool.close()
        pool.join()
