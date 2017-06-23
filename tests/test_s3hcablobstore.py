#!/usr/bin/env python
# coding: utf-8

import os
import sys
import unittest

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, pkg_root)

from dss.blobstore import BlobNotFoundError  # noqa
from dss.blobstore.s3 import S3BlobStore  # noqa
from dss.hcablobstore import HCABlobStore  # noqa
from dss.hcablobstore.s3 import S3HCABlobStore  # noqa
from tests import utils  # noqa


class TestS3HCABlobStore(unittest.TestCase):
    def setUp(self):
        self.test_bucket = utils.get_env("DSS_S3_TEST_BUCKET")
        self.test_src_data_bucket = utils.get_env("DSS_S3_TEST_SRC_DATA_BUCKET")
        self.blobhandle = S3BlobStore()
        self.hcahandle = S3HCABlobStore(self.blobhandle)

    def tearDown(self):
        pass

    def test_verify_blob_checksum(self):
        self.assertTrue(
            self.hcahandle.verify_blob_checksum(
                self.test_src_data_bucket, "test_good_source_data/0",
                {
                    HCABlobStore.MANDATORY_METADATA['S3_ETAG']['keyname']: "3b83ef96387f14655fc854ddc3c6bd57",
                }
            )
        )

        self.assertFalse(
            self.hcahandle.verify_blob_checksum(
                self.test_src_data_bucket, "test_good_source_data/1",
                {
                    HCABlobStore.MANDATORY_METADATA['S3_ETAG']['keyname']: "3b83ef96387f14655fc854ddc3c6bd57",
                }
            )
        )

        with self.assertRaises(BlobNotFoundError):
            self.hcahandle.verify_blob_checksum(
                self.test_src_data_bucket, "test_good_source_data/0/DOES_NOT_EXIST",
                {
                    HCABlobStore.MANDATORY_METADATA['S3_ETAG']['keyname']: "3b83ef96387f14655fc854ddc3c6bd57",
                }
            )


if __name__ == '__main__':
    unittest.main()
