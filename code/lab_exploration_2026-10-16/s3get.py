"""Download one S3 object with retries (LAB 18/10/2026): many jobs starting at once on one instance can fail to get
instance-metadata credentials (botocore NoCredentialsError); retry with a random back-off instead of failing.
usage: python s3get.py <bucket> <key> <local file>"""
import random
import sys
import time

import boto3

bucket, key, dst = sys.argv[1], sys.argv[2], sys.argv[3]
for attempt in range(30):
    try:
        boto3.client("s3", region_name="eu-north-1").download_file(bucket, key, dst)
        sys.exit(0)
    except Exception as exc:                       # credentials not yet available, throttling, transient network
        last = exc
        time.sleep(2 + random.random() * 10)
print("s3get failed after 30 attempts:", repr(last), file=sys.stderr)
sys.exit(1)
