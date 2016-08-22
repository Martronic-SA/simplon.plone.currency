from simplon.plone.currency.currency import Currency
from simplon.plone.currency.interfaces import ICurrency
from zope.interface.verify import verifyObject
import unittest

class CurrencyTests(unittest.TestCase):
    def testInterface(self):
        euro=Currency(code="EUR", rate="1.0")
        verifyObject(ICurrency, euro)

    def testConstruction(self):
        euro=Currency(code="EUR", rate=1.0)
        self.assertEqual(euro.code, "EUR")
        self.assertEqual(euro.rate, 1.0)
        usd=Currency(code="USD", rate=0.72)
        self.assertEqual(usd.code, "USD")
        self.assertEqual(usd.rate, 0.72)

    def testCurrencySymbolKnowledge(self):
        self.assertEqual(Currency("EUR").symbol, u"\u20ac")
        self.assertEqual(Currency("USD").symbol, "$")
        self.assertEqual(Currency("NOK").symbol, "NOK")

    def testCurrencySymbolKnowledge(self):
        self.assertEqual(Currency("EUR").description, u"Euro")
        self.assertEqual(Currency("USD").description, u"US Dollar")
        self.assertEqual(Currency("NOK").description, u"Norwegian Krone")


def test_suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CurrencyTests))
    return suite
