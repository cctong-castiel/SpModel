import json
from os import getcwd, getenv
from os.path import join
from lib.handler.awshandler import AWSHandler
from lib.handler.ziphandler import ZipHandler

# get config value
config = json.load(open(join(getcwd(), "config/config.json")))
vocab_size, zip_type = config.get("vocab_size"), config.get("zip_type")

# load aws env
accessKey = getenv("AWS_ACCESS")
secretKey = getenv("AWS_SECRET")
region = getenv("AWS_REGION")
bucket = getenv("AWS_BUCKET")

# create ZipHandler and AWSHandler objects
aws_handler = AWSHandler(accessKey, secretKey, region, bucket)