from Persistence import Persistent
from zope.interface import implements
from simplon.plone.currency.interfaces import ICurrencyManager
from simplon.plone.currency.currency import CurrencyStorage
from simplon.plone.currency.currency import Currency

class CurrencyManager(Persistent):
    implements(ICurrencyManager)
    
    def __init__(self):
        self.currencies=CurrencyStorage()
        self.currencies.addItem(Currency(code="EUR", rate=1.0))
        self.currency="EUR"

    def SwitchCurrency(self, code):
        factor=self.currencies[code].rate
        for cur in self.currencies.values():
            cur.rate/=factor
        self.currency=code

    def Convert(from_currency, to_currency, amount):
        return (amount*self.currencies[to_curency].rate) / \
                self.currencies[from_currency].rate

