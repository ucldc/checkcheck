#!/usr/bin/env python3
"""CheckCheck checks repositories where the file name is the checksum"""
import argparse
import hashlib
import os
import logging
import sys
import boto3
from urllib.parse import urlparse


class CheckCheckException(Exception):
    """Raise for checksum errors"""


logger = logging.getLogger(__name__)

ENDPOINT_URL = None
HASHNAME = None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='fixity check for content addressable storage')

    parser.add_argument('store', help='root path or specific file')

    parser.add_argument('--loglevel', default='ERROR', required=False)

    parser.add_argument(
        '--endpoint_url',
        default=None,
        required=False, )

    parser.add_argument(
        '--hashname',
        default='md5',
        choices=hashlib.algorithms_available, )

    if argv is None:
        argv = parser.parse_args()

    # set debugging level
    numeric_level = getattr(logging, argv.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % argv.loglevel)
    logging.basicConfig(level=numeric_level, )

    global HASHNAME
    HASHNAME = argv.hashname

    if os.path.isdir(argv.store):
        return check_path(argv.store)
    elif os.path.isfile(argv.store):
        return check_one(argv.store)
    elif argv.store.startswith('s3://'):
        global ENDPOINT_URL
        ENDPOINT_URL = argv.endpoint_url
        return check_s3(argv.store)
    else:
        parser.print_help()
        return 1


def analyze_file(afile, hashtype):
    """Block through the file"""
    hasher = hashlib.new(hashtype)
    BLOCKSIZE = 1024 * hasher.block_size
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()


def check_one(filename):
    """Check a file or s3.Object hash against the filename"""
    checksum = os.path.basename(filename)
    if filename.startswith('s3://'):  # s3
        parts = urlparse(filename)
        s3 = boto3.resource('s3', endpoint_url=ENDPOINT_URL)
        obj = s3.Object(parts.netloc, parts.path.strip('/'))
        afile = obj.get()['Body']
        seen_checksum = analyze_file(afile, HASHNAME)
    else:  # regular file
        with open(filename, 'rb') as afile:
            seen_checksum = analyze_file(afile, HASHNAME)
    if seen_checksum != checksum:
        raise CheckCheckException('file {} has {} of {}'.format(
            checksum, HASHNAME, seen_checksum))


def try_one(filename):
    """Try a filename, catch any exception"""
    try:
        check_one(filename)
        logger.info('{} checks out'.format(filename))
    except CheckCheckException as e:
        return e


def check_path(path):
    """Check all files in a directory"""
    exit_code = 0
    for root, ____, files, in os.walk(path):
        for name in files:
            error = try_one(os.path.join(root, name))
            if error:
                logger.error(error)
                exit_code = 1
    return exit_code


def check_s3(path):
    """Check s3 path"""
    parts = urlparse(path)
    conn = boto3.client('s3', endpoint_url=ENDPOINT_URL)
    paginator = conn.get_paginator('list_objects_v2')
    response_iterator = paginator.paginate(
        Bucket=parts.netloc,
        Prefix=parts.path.strip('/'), )
    exit_code = 0
    for page in response_iterator:
        for key in page['Contents']:
            url = '/'.join(['s3:/', parts.netloc, key['Key']])
            error = try_one(url)
            if error:
                logger.error(error)
                exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
"""
Copyright © 2016, Regents of the University of California
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the University of California nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
