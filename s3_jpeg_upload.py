"""
A script for uploading JPEGs to Amazon S3.
"""
import os
import sys
import argparse

import boto3
import botocore


s3 = boto3.resource('s3')

            
def extract_filenames(rootdir):
    """Return a list of JPEG filenames."""
    paths = []
    for subdir, _dirs, files in os.walk(rootdir):
        for f in files:
            _fn, ext = os.path.splitext(f)
            if ext == ".jpeg":
                path = os.path.join(subdir, f)
                paths.append(path)
    return paths

def create_bucket(bucket_name, region):
    """Create the bucket if it doesn't already exist."""
    try:
        if region:
            config = {'LocationConstraint': region}
            s3.create_bucket(Bucket=bucket_name,
                             CreateBucketConfiguration=config)
        else:
            s3.create_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            return
        raise e

if __name__ == '__main__':
    description = '''Upload JPEGSs to Amazon S3.
    
    The folder structure of the root dir will be recreated in the bucket. If the
    bucket already exists any files it contains will be overwritten with those
    that have the same path.
    
    Installation:

        pip install boto3 awscli
    
    Configuration:
        
        Create an AWS IAM user:
        http://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html
        
        Grant the user programatic access and attatch the AmazonS3FullAccess
        policy, then run:
        
        aws configure
        
        and enter the access and secret keys for the user created above.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('rootdir',
                        help="Path to the directory containing the JPEGs.")
    parser.add_argument('bucket_name', help="The name of the bucket.")
    parser.add_argument('--region', default=None,
                        help="The region for the bucket.")
    args = parser.parse_args()
    jpeg_paths = extract_filenames(args.rootdir)
    create_bucket(args.bucket_name, args.region)
    for path in jpeg_paths:
        fn = path.replace(args.rootdir, '').lstrip('/')
        with open(path, 'rb') as img:
            s3.Object(args.bucket_name, fn).put(Body=img)
            print '{0} uploaded'.format(fn)
    
    
    