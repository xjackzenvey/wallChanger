import unittest
from utils import JsonUtils

class TestJsonUtils(unittest.TestCase):
    def test_getValueByPath(self):
        self.assertEqual(
            JsonUtils.getValueByPath(
                '[{"key1":"value1","key2":"value2"},["l1","l2",{"k":"v"}]]',
                '/[1]/[2]/k'
            ),
            "v"
        )

if __name__ == '__main__':
    unittest.main()
