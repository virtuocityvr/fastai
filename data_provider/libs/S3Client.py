import boto3
import logging
import os
import sys
from boto3.s3.transfer import S3Transfer

logger = logging.getLogger('S3Client')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s %(name)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(screen_handler)

class S3Client:
    
    def __init__(self, local_s3_root):
        self.s3 = boto3.resource('s3')
        self.s3client = boto3.client('s3')
        self.transfer = S3Transfer(self.s3client)
        self.local_s3_root = local_s3_root
        
    def download_photo(self, photo):
        file = self.local_s3_root + photo["media"]["path"]
        if not os.path.exists(file):
            self.download_file(photo["media"]["bucket"], photo["media"]["path"], file)
        else:
            logger.debug("file already exists: "+ file)
        return file

    def download_file(self, bucket, path, target_file):
        logger.debug("Downloading: "+ path)
        self.s3client.download_file(bucket, path, target_file)
        logger.debug("Downloaded: " + path)
    
    def upload_result(self, file, bucket, path):
        logger.debug("Uploading: " + file)
        self.transfer.upload_file(file, bucket, path)
        logger.debug("Uploaded: " + file)


