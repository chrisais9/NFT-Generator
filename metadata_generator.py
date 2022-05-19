import json


class MetadataGenerator:
    def __init__(self, config):
        self.config = config

    def generate(self, traits):
        print("======= Save Token Metadata Start =======")

        token_id = 1
        for trait in traits:
            token_metadata = self.generate_token_metadata(trait, token_id)
            with open(f'./metadata/{token_id}', 'w') as outfile:
                json.dump(token_metadata, outfile, indent=4)
            print(f"saved {token_id}")

            token_id += 1

    def generate_token_metadata(self, trait, token_id):
        return {
            "name": f'{self.config["title"]} #{token_id}',
            "description": self.config["description"],
            "image": f'{self.config["base_uri"]}/{token_id}',
            "attributes": [{"trait_type": trait_type, "value": value} for trait_type, value in trait.items()]
        }
