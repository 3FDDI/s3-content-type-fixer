#!/usr/bin/python -tt
"""
A script for detecting and updating the Content-Type metadata
on Keys within an AWS S3 Bucket. Preserves any other metadata set
on the Key.

Requires boto and python-magic.

Usage: update-content-type.py <s3 access key> <s3 secret key> <bucket name> [--set-extensions]
  
--set-extensions - optional argument which will also rename files with the appropriate
  extension based on MIME type.
"""
import sys
import tempfile
import mimetypes
import boto
import magic


def update_content_type(access_key, secret_key, bucket_name, set_extensions=False):
  s3 = boto.connect_s3(access_key, secret_key)
  bucket = s3.lookup(bucket_name)
  keyList = bucket.list()

  for k in keyList:
    # work around for the fact that list() doesn't return metadata
    key = bucket.lookup(k.name)
    #contentType = mimetypes.guess_type(key.name)
    temp_file = tempfile.NamedTemporaryFile()
    key.get_contents_to_file(temp_file)
    contentType = magic.from_file(temp_file.name, mime=True)
    metadata = {'Content-Type': contentType}

    # Preserve any other metadata that will otherwise be wiped out
    if (key.cache_control):
      metadata.update({'Cache-Control': key.cache_control})
    if (key.content_disposition):
      metadata.update({'Content-Disposition': key.content_disposition})
    if (key.content_language):
      metadata.update({'Content-Language': key.content_language})
    if (key.expiry_date):
      metadata.update({'Expires': key.expiry_date})
    if (key.content_encoding):
      metadata.update({'Content-Encoding': key.content_encoding})
    if (key.metadata):
      metadata.update(key.metadata)

    if set_extensions == True and "." not in key.name:
      # This uglyness is due to mimetypes.guess_extension returning '.jpe' for jpegs. Yay sane defaults.
      if 'jpeg' in contentType:
        k_name = key.name + ".jpg"
      else:
        k_name = key.name + mimetypes.guess_extension(contentType)
      bucket.new_key(k_name)
      key.copy(bucket.name, k_name, metadata, preserve_acl=True)
      key.delete()
    else:
      key.copy(bucket.name, key.name, metadata, preserve_acl=True)
    

def main():
  try:
    args = sys.argv[1:]
    if args[3]=='--set-extensions':
      update_content_type(args[0], args[1], args[2], set_extensions = True)
    elif args[2]:
      update_content_type(args[0], args[1], args[2])
    else:
      print 'Usage: update-content-type.py <s3 access key> <s3 secret key> <bucket name> [--set-extensions]'
      print ' --set-extensions - optional argument which will also rename files with the appropriate'
      print '   extension based on MIME type.'
      sys.exit(1)
  except IndexError:
    print 'Usage: update-content-type.py <s3 access key> <s3 secret key> <bucket name> [--set-extensions]'
    print ' --set-extensions - optional argument which will also rename files that do not have extensions with the appropriate extension based on MIME type.'
    sys.exit(1)


if __name__ == '__main__':
  main()