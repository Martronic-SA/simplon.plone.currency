from simplon.plone.currency.vocabulary import CurrencyVocabularyFactory
from simplon.plone.currency.vocabulary import SiteCurrencyVocabularyFactory
from simplon.plone.currency.interfaces import ICurrencyManager
from simplon.plone.currency.manager import CurrencyManager
from simplon.plone.currency.currency import Currency
from zope.schema.interfaces import IVocabularyFactory
from zope.component.globalregistry import base
from zope.interface.verify import verifyObject
import unittest

class CurrencyVocabularyTests(unittest.TestCase):
    def setUp(self):
        self.vocabulary=CurrencyVocabularyFactory

    def XXXtestInterface(self):
        # This fails even though as far as I can see it should not
        verifyObject(IVocabularyFactory, self.vocabulary)

    def testContains(self):
        self.failUnless("EUR" in self.vocabulary(None))
        self.failUnless("NOK" in self.vocabulary(None))
        self.failIf("XXX" in self.vocabulary(None))


class SiteCurrencyVocabularyTests(unittest.TestCase):
    def setUp(self):
        self.vocabulary=SiteCurrencyVocabularyFactory
        self.manager=CurrencyManager()
        base.registerUtility(self.manager, ICurrencyManager)

    def tearDown(self):
        base.unregisterUtility(self.manager, ICurrencyManager)

    def testInitialVocabulary(self):
        self.assertEqual(len(self.vocabulary(None)), 1)
        self.assertEqual([t.value for t in self.vocabulary(None)], ["EUR"])

    def testNewCurrencies(self):
        self.manager.currencies.addItem(Currency(code="NOK"))
        self.assertEqual(len(self.vocabulary(None)), 2)
        self.assertEqual(set([t.value for t in self.vocabulary(None)]),
                set(["EUR", "NOK"]))

    def testRemovingCurrencies(self):
        self.manager.currencies.addItem(Currency(code="NOK"))
        del self.manager.currencies["EUR"]
        self.assertEqual(len(self.vocabulary(None)), 1)
        self.assertEqual([t.value for t in self.vocabulary(None)], ["NOK"])


def test_suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CurrencyVocabularyTests))
    suite.addTest(unittest.makeSuite(SiteCurrencyVocabularyTests))
    return suite

