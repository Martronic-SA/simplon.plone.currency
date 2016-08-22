from zope.component import getUtility
from zope.component import queryMultiAdapter
from BTrees.OOBTree import OOBTree
from OFS.SimpleItem import SimpleItem
from zope.interface import implements
from zope.container.ordered import OrderedContainer
from zope.container.contained import Contained
from simplon.plone.currency.interfaces import ICurrency
from simplon.plone.currency.interfaces import ICurrencyStorage
from simplon.plone.currency.currencies import currencies

class Currency(SimpleItem, Contained):
    implements(ICurrency)

    def __init__(self, code="", rate=1.0):
        self.code=code
        self.rate=rate

    @property
    def symbol(self):
        return currencies[self.code][1]


    @property
    def description(self):
        return currencies[self.code][0]


class CurrencyStorage(OrderedContainer):
    implements(ICurrencyStorage)

    def __init__(self):
        OrderedContainer.__init__(self)
        self._data=OOBTree()

    def addItem(self, item):
        self[item.code]=item

