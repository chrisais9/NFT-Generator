from PIL import Image
from image4layer import Image4Layer
import yaml

import metadata_generator
import trait_generator


class Generator:

    def __init__(self, config):
        self.config = config
        self.width = config["size"]["width"]
        self.height = config["size"]["height"]

        self.traits = []
        self.traitGenerator = trait_generator.TraitGenerator(config)

        self.metadataGenerator = metadata_generator.MetadataGenerator(config)

    def generate(self):
        self.traits = self.traitGenerator.generate()
        self.traitGenerator.plot_generated_traits()

        self.metadataGenerator.generate(self.traits)

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


def main():
    with open('config.yaml') as config:
        config = yaml.load(config, Loader=yaml.FullLoader)

    generator = Generator(config)
    generator.generate()


if __name__ == '__main__':
    main()
