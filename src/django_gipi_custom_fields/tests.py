from django.test import TestCase

from . import DatiBancari

# http://bitkickers.blogspot.com/2009/10/unit-testing-django-with-doctest.html
__test__ = {
        "dati_bancari": DatiBancari
}

class ShortURLTests(TestCase):
    def test_environment(self):
        """Just make sure everything is set up correctly."""
        self.assert_(True)
