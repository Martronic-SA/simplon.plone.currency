from zope.interface import Attribute
from zope.interface import Interface
from zope.schema import Choice
from zope.schema import Container
from zope.schema import Float
from zope.container.interfaces import IContained
from zope.container.interfaces import IContainer
from zope.container.interfaces import IContainerNamesContainer
from zope.container.constraints import contains
from Products.CMFPlone import PloneMessageFactory as _

class ICurrencyInformation(Interface):
    code = Choice(
            title=_(u"label_currency_currency",
                default=u"Currency"),
            description=_(u"help_currency_currency",
                default=u"The base currency is used as the default currency "
                        u"as well as the base for currency rates. If you "
                        u"change the base currency all rates will be "
                        u"recalculated automatically."),
            vocabulary="simplon.plone.currency.currencies",
            required=True)

    rate = Float(
            title=_(u"label_currency_rate",
                default=u"Rate"),
            description=_(u"help_currency_date",
                default=u"This is the conversion rate from this currency to a "
                        u"'system' currency you configure."),
            min=0.0,
            default=1.0,
            required=True)

    symbol = Attribute("symbol",
            u"The symbol used to identify this currency. Since not all"
            u"currencies have a symbol this can be an empty string.")

    description = Attribute("description",
            u"A short description of the currency.")


class ICurrency(IContained, ICurrencyInformation):
    """Currency information."""


class ICurrencyStorage(IContainer, IContainerNamesContainer):
    contains("simplon.plone.currency.interfaces.ICurrency")


class IGlobalCurrencySettings(Interface):
    currency = Choice(
            title=_(u"label_currencymanager_base_currency",
                default=u"Base currency"),
            description=_(u"help_currencymanager_base_currency",
                default=u"The base currency is used as the default currency "
                        u"as well as the base for currency rates."),
            vocabulary="simplon.plone.currency.sitecurrencies",
            default="EUR",
            required=True)

    def SwitchCurrency(code):
        """Switch the base currency.

        This will take care of recalculating all conversion rates.
        """

    def Convert(from_currency, to_currency, amount):
        """Convert from one currency to another currency."""


class ICurrencyManager(IGlobalCurrencySettings):
    currencies = Container(
            title=_(u"label_currencymanager_currencies",
                default=u"Currencies"),
            description=_(u"help_currencymanager_currencies",
                default=u""),
            required=True)

