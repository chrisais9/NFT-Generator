import yaml

import image_generator
import metadata_generator
import trait_generator


class Generator:

    def __init__(self, config):
        self.config = config

        self.traits = []
        self.traitGenerator = trait_generator.TraitGenerator(config)

        self.metadataGenerator = metadata_generator.MetadataGenerator(config)

        self.imageGenerator = image_generator.ImageGenerator(self.config)

    def generate(self):
        self.traits = self.traitGenerator.generate()
        self.traitGenerator.plot_generated_traits()

        self.metadataGenerator.generate(self.traits)

        self.imageGenerator.generate(self.traits)


def main():
    with open('config.dev.yaml') as config:
        config = yaml.load(config, Loader=yaml.FullLoader)

    generator = Generator(config)
    generator.generate()


if __name__ == '__main__':
    main()
