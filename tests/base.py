'''
这段代码负责单元测试：
1. 单元测试的主要目的是测试代码是否正确，避免手动检查。
2. 在修改代码之后，会不会破坏原有的功能
3. 发现bug，并为debug提供线索

'''
from todo import create_app
import unittest

class TodoTest(unittest.TestCase):
    def setUp(self):
        # 传入一个测试实例，使用内存数据库模式(数据不会保存到文件，每次测试全是全新的数据库)
        self.app = create_app(config_overrides={
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'TESTING': True
        })
        
        self.client = self.app.test_client()

    # 这个方法用于 检查 whole 字典是否包含 expected_subset 的键值对
    def assertDictSubset(self, expected_subset: dict, whole: dict):
        for key, value in expected_subset.items():
            self.assertEqual(whole[key],value)