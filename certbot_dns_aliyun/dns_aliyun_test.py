"""Tests for certbot_dns_aliyun.dns_aliyun."""

import os
import unittest

import mock
from requests.exceptions import HTTPError, RequestException

from certbot.plugins import dns_test_common
from certbot.plugins import dns_test_common_lexicon
from certbot.tests import util as test_util

DOMAIN_NOT_FOUND = Exception('No domain found')
GENERIC_ERROR = RequestException
LOGIN_ERROR = HTTPError('400 Client Error: ...')

ACCESS_KEY = '123'
ACCESS_KEY_SECRET = 'bar'


class AuthenticatorTest(test_util.TempDirTestCase,
                        dns_test_common_lexicon.BaseLexiconAuthenticatorTest):

    def setUp(self):
        super(AuthenticatorTest, self).setUp()

        from certbot_dns_aliyun.dns_aliyun import Authenticator

        path = os.path.join(self.tempdir, 'file.ini')
        dns_test_common.write({
            "aliyun_access_key": ACCESS_KEY,
            "aliyun_access_key_secret": ACCESS_KEY_SECRET
        }, path)

        self.config = mock.MagicMock(
            aliyun_credentials=path,
            aliyun_propagation_seconds=0
        )

        self.auth = Authenticator(self.config, "aliyun")
        
        self.auth._configure_credentials(
            'credentials',
            'Aliyun DNS credentials INI file',
            {
                'access-key': 'AccessKey for Aliyun DNS, obtained from Aliyun RAM',
                'access-key-secret': 'AccessKeySecret for Aliyun DNS, obtained from Aliyun RAM'
            }
        )
        
        self.mock_client = mock.MagicMock()
        self.auth._get_alidns_client = mock.MagicMock(return_value=self.mock_client)

    @test_util.patch_display_util()
    def test_perform(self, mock_get_utility):
        self.auth.perform([self.achall])
        self.mock_client.add_txt_record.assert_called_once()

    @test_util.patch_display_util()
    def test_cleanup(self, mock_get_utility):
        self.auth._attempt_cleanup = True
        self.auth.cleanup([self.achall])
        self.mock_client.del_txt_record.assert_called_once()


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
