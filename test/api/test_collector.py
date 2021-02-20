import os
import unittest

from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json

AKI = os.environ.get('ALI_ACCESS_KEY_ID', None)
AKS = os.environ.get('ALI_ACCESS_KEY_SECRET', None)

if AKI == None or AKS == None:
    print("""
##################################################
# ERROR 
#
# Configure your Alibaba Cloud credential first for test
##################################################
example)

export ALI_ACCESS_KEY_ID=<YOUR_ALI_ACCESS_KEY_ID>
export ALI_ACCESS_KEY_SECRET=<YOUR_ALI_ACCESS_KEY_SECRET>

""")
    exit


class TestCollector(TestCase):

    def test_init(self):
        v_info = self.inventory.Collector.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {
        }
        secret_data = {
            'ali_access_key_id': AKI,
            'ali_access_key_secret': AKS
        }
        v_info = self.inventory.Collector.verify({'options': options, 'secret_data': secret_data})
        print_json(v_info)

    def test_collect(self):
        options = {}
        secret_data = {
            'ali_access_key_id': AKI,
            'ali_access_key_secret': AKS,
        }
        filter = {}
        resource_stream = self.inventory.Collector.collect({'options': options, 'secret_data': secret_data,
                                                            'filter': filter})
        for res in resource_stream:
            print_json(res)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
