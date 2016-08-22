from simplon.plone.currency.currency import Currency
from simplon.plone.currency.manager import CurrencyManager
from simplon.plone.currency.interfaces import ICurrencyManager
from zope.interface.verify import verifyObject
import unittest

class ManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager=CurrencyManager()

    def addCurrencies(self):
        self.manager.currencies.addItem(Currency(code="USD", rate=0.72))
        self.manager.currencies.addItem(Currency(code="NOK", rate=0.12))

    def testInterface(self):
        verifyObject(ICurrencyManager, self.manager)

    def testDefaultCurrencies(self):
        self.assertEqual(self.manager.currencies.keys(), ["EUR"])
        euro=self.manager.currencies["EUR"]
        self.assertEqual(euro.code, "EUR")
        self.assertEqual(euro.rate, 1.0)

    def testDefaultBaseCurrency(self):
        self.assertEqual(self.manager.currency, "EUR")

    def testCurrencySwitch(self):
        self.addCurrencies()
        self.manager.SwitchCurrency("USD")
        self.assertEqual(self.manager.currency, "USD")

    def testCurrencySwitchUpdateRates(self):
        self.addCurrencies()
        self.manager.SwitchCurrency("USD")
        self.assertAlmostEqual(self.manager.currencies["USD"].rate, 1.0, 3)
        self.assertAlmostEqual(self.manager.currencies["EUR"].rate, 1.3888, 3)
        self.assertAlmostEqual(self.manager.currencies["NOK"].rate, 0.1666, 3)


def test_suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ManagerTests))
    return suite
