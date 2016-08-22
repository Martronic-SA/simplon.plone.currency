from Products.PloneTestCase import PloneTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.Five.testbrowser import Browser
from simplon.plone.currency.tests import layer
import unittest

PloneTestCase.setupPloneSite()

from zope.testing import doctest
OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

class SimplonPloneCurrencyFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    layer = layer.SimplonPloneCurrency

    def getBrowser(self, loggedIn=False):
        """Utility method to get a, possibly logged-in, test browser."""
        browser = Browser()
        if loggedIn:
            browser.addHeader('Authorization', 'Basic %s:%s' %
                 (PloneTestCase.default_user, PloneTestCase.default_password))

        return browser


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(FunctionalDocFileSuite("UserInterface.txt",
            optionflags=OPTIONFLAGS,
            test_class=SimplonPloneCurrencyFunctionalTestCase))
    return suite

