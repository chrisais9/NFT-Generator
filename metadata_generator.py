import json


class MetadataGenerator:
    def __init__(self, config):
        self.config = config
        self.token_id = self.config["start"]

    def generate(self, traits):
        print("======= Save Token Metadata Start =======")
        for trait in traits:
            token_metadata = self.generate_token_metadata(trait, self.token_id)
            with open(f'./metadata/{self.token_id}', 'w') as outfile:
                json.dump(token_metadata, outfile, indent=4)
            print(f"saved {self.token_id}")

            self.token_id += 1

    def generate_token_metadata(self, trait, token_id):
        return {
            "name": f'{self.config["title"]} #{token_id}',
            "description": self.config["description"],
            "image": f'{self.config["base_uri"]}/{token_id}',
            "attributes": [{"trait_type": trait_type, "value": value} for trait_type, value in trait.items()]
        }
