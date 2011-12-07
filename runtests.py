import unittest
import tests.test_daemon_context
import tests.test_single_instance

test_modules = [
                tests.test_single_instance,
                tests.test_daemon_context,
               ]

suite = unittest.TestSuite()
for module in test_modules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(module))
unittest.TextTestRunner().run(suite)


