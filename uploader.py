import json
from urllib.parse import urlparse, urlunparse
from os import walk, path, sep, getenv
from requests import Session, Request
from dotenv import load_dotenv
import os
import glob


class Uploader:

    def __init__(self):
        load_dotenv(verbose=True)
        self.base_url = "https://api.pinata.cloud/pinning"

    def upload_directory(self, directory):

        files = []
        ipfs_url = f"{self.base_url}/pinFileToIPFS"
        headers = {
            'pinata_api_key': getenv('PINATA_API_KEY'),
            'pinata_secret_api_key': getenv('PINATA_SECRET_KEY')
        }

        files.append(('pinataMetadata', (None, '{"name":"' + directory.split(sep)[-1] + '"}')))

        for root, dirs, files_ in walk(path.abspath(directory)):
            for f in files_:
                complete_path = path.join(root, f)
                files.append(('file', (sep.join(complete_path.split(sep)[-2:]), open(complete_path, 'rb'))))
        request = Request(
            'POST',
            ipfs_url,
            headers=headers,
            files=files
        ).prepare()
        response = Session().send(request)

        return response.json()["IpfsHash"]

    def replace_base_uri(self, cid):
        folder_path = './metadata'
        for filename in glob.glob(os.path.join(folder_path, '*')):
            if filename != "./metadata/all-traits.json":
                with open(filename, 'r') as f:
                    metadata = json.load(f)
                image_url = urlparse(metadata["image"])
                token_id = image_url.path.split("/")[-1]

                metadata["image"] = urlunparse(image_url._replace(path=f"{cid}/{token_id}.jpeg"))
                with open(filename, 'w') as outfile:
                    json.dump(metadata, outfile, indent=4)

    def upload(self):

        print("uploading images from ./images")
        image_cid = self.upload_directory("./images")
        print("image uploaded to:", image_cid)

        print("replacing images from ./images")
        self.replace_base_uri(image_cid)

        print("uploading metadata from ./metadata")
        metadata_cid = self.upload_directory("./metadata")
        print("metadata uploaded to:", metadata_cid)


if __name__ == '__main__':

    uploader = Uploader()
    uploader.upload()
