from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from simplon.plone.currency.interfaces import ICurrencyManager
from Products.CMFPlone import PloneMessageFactory as _
from simplon.plone.currency.currencies import currencies

class CurrencyVocabulary(object):
    """Vocabulary factory for currencies."""
    implements(IVocabularyFactory)

    def __call__(self, context):
        def morph(code, data):
            return (code, SimpleTerm(
                    value=code,
                    token=code,
                    title=_(u"${code} ${description}",
                        mapping=dict(code=code, description=data[0]))))

        items=[morph(*cur) for cur in currencies.items()]
        items.sort()
        return SimpleVocabulary([item[1] for item in items])

CurrencyVocabularyFactory = CurrencyVocabulary()

class SiteCurrencyVocabulary(object):
    """Vocabulary factory for currencies enabled in the site."""
    implements(IVocabularyFactory)

    def __call__(self, context):
        def morph(code):
            return (code, SimpleTerm(
                    value=code,
                    token=code,
                    title=_(u"${code} ${description}",
                        mapping=dict(code=code, description=currencies[code][0]))))

        manager=getUtility(ICurrencyManager)
        items=[morph(cur) for cur in manager.currencies.keys()]
        items.sort()
        return SimpleVocabulary([item[1] for item in items])

SiteCurrencyVocabularyFactory = SiteCurrencyVocabulary()
