# CheckCheck

Python 3 checksum checker for [content addressable storage](https://en.wikipedia.org/wiki/Content-addressable_storage)
schemes where the checksum is the filename.

Can use any checksum scheme that is available to python hashlib.

```
usage: checkcheck.py [-h] [--loglevel LOGLEVEL] [--endpoint_url ENDPOINT_URL]
                     [--hashname {sha256,SHA,RIPEMD160,sha512,sha1,mdc2,SHA256,SHA224,ripemd160,dsaEncryption,MDC2,SHA1,SHA384,MD4,sha384,DSA,whirlpool,sha224,md4,DSA-SHA,md5,ecdsa-with-SHA1,MD5,sha,SHA512,dsaWithSHA}]
                     store

fixity check for content addressable storage

positional arguments:
  store                 root path or specific file

optional arguments:
  -h, --help            show this help message and exit
  --loglevel LOGLEVEL
  --endpoint_url ENDPOINT_URL
  --hashname {sha256,SHA,RIPEMD160,sha512,sha1,mdc2,SHA256,SHA224,ripemd160,dsaEncryption,MDC2,SHA1,SHA384,MD4,sha384,DSA,whirlpool,sha224,md4,DSA-SHA,md5,ecdsa-with-SHA1,MD5,sha,SHA512,dsaWithSHA}
```

## Testing 

To test with something such as [`minio`](https://minio.io) or other S3 API...

Set up another profile in `~/.aws/` ...

Also, set a `--endpoint_url` command line paramater

```
export AWS_PROFILE=...
./checkcheck/checkcheck.py s3://repo-test/ --endpoint_url http://10.0.1.2:9000 --loglevel info
```


