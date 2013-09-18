def environment():
    print 'hi'

class Foo(object):
    environment = environment

foo = Foo()

class Bar(object):
    def __init__(self):
        self.environment = environment
bar = Bar()

import unittest
class TestBinding(unittest.TestCase):
    """weird!"""
    def test_binding(self):
        self.assertEqual(foo.environment, environment)
    def test_class_level(self):
        self.assertEqual(Foo.environment, environment)
    def test_on_init(self):
        self.assertEqual(bar.environment, environment)

if __name__ == '__main__':
    unittest.main()
