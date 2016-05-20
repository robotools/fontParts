from fontParts.objects.base.lib import BaseLib


class TestLib(object):

    def test_initializes(arg):
        lib = BaseLib()
        lib.foo = "bar"
        assert lib.foo is "bar"
