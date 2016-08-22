from Products.PloneTestCase.layer import PloneSite
from Testing import ZopeTestCase
from Products.Five import fiveconfigure
from Products.Five import zcml
from OFS.Application import install_package
import simplon.plone.currency

class SimplonPloneCurrency(PloneSite):
    @classmethod
    def setUp(cls):
        # starting with 2.10.4 product initialization gets delayed for
        # instance startup and is never called when running tests;  hence
        # we have to initialize the package method manually...
        app = ZopeTestCase.app()
        install_package(app, simplon.plone.currency, None)
        ZopeTestCase.close(app)

        fiveconfigure.debug_mode = True
        zcml.load_config('configure.zcml',
                         simplon.plone.currency)
        fiveconfigure.debug_mode = False

    @classmethod
    def tearDown(cls):
        pass
