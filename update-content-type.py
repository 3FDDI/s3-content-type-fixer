import boto
import mimetypes

S3_ACCESS_KEY = 'put your access key here'
S3_SECRET_KEY = 'put your secret key here'
S3_BUCKET_NAME = 'enter the bucket name'

s3 = boto.connect_s3(S3_ACCESS_KEY,S3_SECRET_KEY)
bucket = s3.lookup(S3_BUCKET_NAME)
keyList = bucket.list()

for k in keyList:
  # work around for the fact that list() doesn't return metadata
	key = bucket.lookup(k.name)
	contentType = mimetypes.guess_type(key.name)
	metadata = {'Content-Type': contentType[0]}

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

	key.copy(bucket.name, key.name, metadata, preserve_acl=True)

