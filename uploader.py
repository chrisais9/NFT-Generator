from os import walk, path, sep, getenv
from requests import Session, Request
from dotenv import load_dotenv


class Uploader:

    def __init__(self):
        load_dotenv(verbose=True)
        self.base_url = "https://api.pinata.cloud/pinning"

    def upload_directory(self, directory):

        files = []
        ipfs_url = f"${self.base_url}/pinFileToIPFS"
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

        print(response.json())

        return response


if __name__ == '__main__':
    uploader = Uploader()
    uploader.upload_directory("plot")
