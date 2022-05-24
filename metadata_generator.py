import json


class MetadataGenerator:
    def __init__(self, config):
        self.config = config

    def generate(self, traits):

        for trait in traits:
            token_metadata = self.generate_token_metadata(trait)
            with open(f'./metadata/{trait["token_id"]}', 'w') as outfile:
                json.dump(token_metadata, outfile, indent=4)
            print(f'saved {trait["token_id"]}')

    def generate_token_metadata(self, trait):
        return {
            "name": f'{self.config["title"]} #{trait["token_id"]}',
            "description": self.config["description"],
            "image": f'{self.config["base_uri"]}/{trait["token_id"]}',
            "attributes": [
                {
                    "trait_type": trait_type,
                    "value": value
                } for trait_type, value in trait.items() if trait_type != "token_id"
            ]
        }
