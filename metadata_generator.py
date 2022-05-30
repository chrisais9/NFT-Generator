import json

import constant


class MetadataGenerator:
    def __init__(self, config):
        self.config = config

    def generate(self, traits):
        for trait in traits:
            token_metadata = self.generate_token_metadata(trait)

            with open(f'./metadata/{trait["token_id"]}', 'w') as outfile:
                json.dump(token_metadata, outfile, indent=4)

    def generate_token_metadata(self, trait):

        attributes = []
        for trait_type, value in trait.items():
            if trait_type == "token_id":
                continue

            if trait_type == constant.CONFIG_HIDDEN_HEADGEAR_HAIR:
                if trait[constant.CONFIG_HEADGEAR] != constant.CONFIG_VALUE_NONE:
                    attributes.append({"trait_type": constant.CONFIG_HAIR, "value": value})
            elif trait_type == constant.CONFIG_HAIR:
                if trait[constant.CONFIG_HEADGEAR] == constant.CONFIG_VALUE_NONE:
                    attributes.append({"trait_type": trait_type, "value": value})
            else:
                attributes.append({"trait_type": trait_type, "value": value})

        return {
            "name": f'{self.config["title"]} #{trait["token_id"]}',
            "description": self.config["description"],
            "image": f'{self.config["base_uri"]}/{trait["token_id"]}',
            "attributes": attributes
        }
