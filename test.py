import boto3
import mimetypes
import uuid
import os


def uuid_file_path(filename):
    if filename:
        ext = filename.split('.')[-1]
    else:
        ext = "png"

    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(filename)

path = "/home/ts/Documents/projects/python-base/codes/faceswap/media/result1.mp4"
s3_client = boto3.client(
            's3', aws_access_key_id="AKIAYMPAXPYXGBUSLCO6", aws_secret_access_key="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")
s3_key = 'video/upload/{0}'.format(uuid_file_path(path))
content_type, _ = mimetypes.guess_type(s3_key)

s3_client.upload_file(path, "sfappv2", s3_key,
                             ExtraArgs={'ACL': 'public-read', 'ContentType': content_type})

print(f'https://s3.amazonaws.com/sfappv2/{s3_key}')