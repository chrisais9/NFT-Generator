from PIL import Image
from image4layer import Image4Layer
import matplotlib.pyplot as plt
import yaml
import random
import json


class Generator:

    def __init__(self, config):
        self.traits = []
        self.config = config
        self.width = config["size"]["width"]
        self.height = config["size"]["height"]

        random.seed(config["seed"])

    def generate(self):

        self.traits = self.generate_traits()

        if self.is_all_trait_unique(self.traits):
            print("Confirmed that every single trait is unique")
        else:
            print("Error! There are duplicated trait")
            return

        self.generate_all_trait_metadata()


        # token_id = self.config["start"]
        #
        # for trait in self.traits:
        #     image = self.generate_image(trait)
        #     image.save(f'./images/{token_id}.jpeg')
        #
        #     token_metadata = self.generate_token_metadata(trait, token_id)
        #     with open(f'./metadata/{token_id}', 'w') as outfile:
        #         json.dump(token_metadata, outfile, indent=4)
        #
        #     token_id += 1

        traits_config = self.config["traits"]
        for attribute in traits_config:
            counts_dict = {k: 0 for k in traits_config[attribute].keys()}
            for trait in self.traits:
                counts_dict[trait[attribute]] = counts_dict.get(trait[attribute], 0) + 1

            labels, counts = zip(*sorted(counts_dict.items(), key=lambda x: x[1]))

            fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(aspect="equal"))
            ax.pie(counts, autopct='%.1f%%', labels=labels, startangle=90, radius=1.1)

            ax.set_title(attribute)

            plt.savefig(f"plot_{attribute}.png")

    def generate_traits(self):
        traits = []
        for i in range(self.config["number"]):
            new_trait = self.new_random_unique_trait()
            traits.append(new_trait)
        return traits

    def new_random_unique_trait(self):
        trait = {}

        traits = self.config["traits"]
        categories = list(traits.keys())
        for category in categories:
            trait[category] = random.choices(
                [k for k in traits[category].keys()],
                [v["prob"] for v in traits[category].values()]
            )[0]

        if trait in self.traits:
            return self.new_random_unique_trait()
        else:
            return trait

    def is_all_trait_unique(self, traits):
        seen = list()
        return not any(i in seen or seen.append(i) for i in traits)

    def generate_all_trait_metadata(self):
        METADATA_FILE_NAME = './metadata/all-traits.json'
        with open(METADATA_FILE_NAME, 'w') as outfile:
            json.dump(self.traits, outfile, indent=4)

    def generate_image(self, trait):
        stack = Image.new('RGBA', (self.width, self.height))

        for category, name in trait.items():
            image_layer = Image.open(f'{self.config["traits"][category]["values"][name]["src"]}').convert('RGBA')
            stack = Image.alpha_composite(stack, image_layer)

        filter = Image.open("layer/filter.png").convert("RGBA")
        filter.putalpha(int(256 * 0.3))
        stack = Image4Layer.pin_light(stack, filter)

        stack = stack.convert('RGB')
        return stack

    def generate_token_metadata(self, trait, token_id):
        return {
            "name": f'{self.config["name"]} #{token_id}',
            "image": f'{self.config["base_uri"]}/{token_id}',
            "attributes": [{"trait_type": trait_type, "value": value} for trait_type, value in trait.items()]
        }


def main():
    with open('config.yaml') as config:
        config = yaml.load(config, Loader=yaml.FullLoader)

    generator = Generator(config)
    generator.generate()


if __name__ == '__main__':
    main()
