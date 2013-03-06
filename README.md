s3-content-type-fixer
==
A script for detecting and updating the Content-Type metadata on Keys within an AWS S3 Bucket. Preserves any other metadata set on the Key.

Requires **boto** and **python-magic**.

Usage:
>  update-content-type.py `<s3 access key`> `<s3 secret key`> `<bucket name`> [--set-extensions]
  
--set-extensions - optional argument which will also rename files with the appropriate
  extension based on MIME type.
