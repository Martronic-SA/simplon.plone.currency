from Acquisition import aq_parent, aq_inner
import zope.event
from zope.lifecycleevent import ObjectModifiedEvent
from zope.interface import implements
try:
    from Products.Five.formlib.formbase import EditFormBase, AddFormBase
except:
    from five.formlib.formbase import EditFormBase, AddFormBase
from simplon.plone.currency.browser.interfaces import ICurrencyAdding
from simplon.plone.currency.interfaces import ICurrencyInformation
from simplon.plone.currency.currency import Currency
from OFS.SimpleItem import SimpleItem
from Acquisition import Implicit
from Products.Five import BrowserView
from Products.CMFPlone import PloneMessageFactory as _
from zope.formlib.form import FormFields
#from zope.formlib.form import applyChanges
from z3c.form.form import applyChanges
from zope.formlib.form import action
from zope.formlib.form import haveInputWidgets
from zope.traversing.interfaces import ITraversable
from zope.component import adapts
from zope.component import getUtility
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from zope.publisher.interfaces.browser import IBrowserRequest
from simplon.plone.currency.interfaces import ICurrencyManager
from plone.app.form.validators import null_validator
from z3c.form import form, button
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.z3cform import layout
from plone.autoform.form import AutoExtensibleForm
from z3c.form.i18n import MessageFactory as _z3c


class CurrencyAdding(SimpleItem, BrowserView):
    implements(ICurrencyAdding)

    contentName = _(u"Currency")
    request = None
    context = None
    id = '+currencies'
    
    __allow_access_to_unprotected_subobjects__ = True

    def add(self, content):
        """Add the currency to the schema
        """
        currencies=getUtility(ICurrencyManager).currencies
        currencies.addItem(content)

    def nextURL(self):
        parent = aq_parent(aq_inner(self.context))
        url = str(getMultiAdapter((parent, self.request), name=u"absolute_url"))
        return url + "/@@currency-controlpanel"

    def namesAccepted(self):
        return False

    def nameAllowed(self):
        return False

    def addingInfo(self):
        return ()

    def isSingleMenuItem(self):
        return False

    def hasCustomAddView(self):
        return False


class CurrencyAddFormBase(AutoExtensibleForm, form.AddForm):
    """An add form for currencies.
    """
    ignoreContext = True
    schema = ICurrencyInformation
    label = _(u"Add Currency")
    description = _(u"Register a new currency in your site")

    def create(self, data):
        currency = Currency(data["code"])
        del data["code"]
        applyChanges(self, currency, data)
        return currency

    def add(self, content):
        self.context.add(content)

    def nextURL(self):
        parent = aq_parent(aq_inner(self.context))
        url = str(getMultiAdapter((parent, self.request), name=u"absolute_url"))
        return url + "/@@currency-controlpanel"

    @button.buttonAndHandler(_z3c('Add'), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"), name='cancel')
    def handle_cancel_action(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''


class CurrencyAddForm(layout.FormWrapper):
    form = CurrencyAddFormBase


class CurrencyEditForm(AutoExtensibleForm, form.EditForm):
    """An edit form for LDAP properties.
    """
    schema = ICurrencyInformation
    label = _(u"Edit Currency")
    description = _(u"Edit a currency.")
    form_name = _(u"Configure currency")
    fieldset = "schema"

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='save')
    def handle_save_action(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        manager=getUtility(ICurrencyManager)

        if manager.currency==self.context.code:
            message.addStatusMessage(
                _("can_not_edit_base_currency",
                    default=u"You can not edit the base currency"),
                type="error")
        if self.applyChanges(data):
            zope.event.notify(ObjectModifiedEvent(self.context))
            message.addStatusMessage(
                    _("currency_updated",
                        default=u"Currency ${code} modified.",
                        mapping=dict(code=self.context.code)),
                    type="info")
        else:
            message.addStatusMessage(
                _("no_changes",
                    default=u"Nothing changed"),
                type="info")
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"), name='cancel')
    def handle_cancel_action(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''


    def nextURL(self):
        parent = aq_parent(aq_inner(self.context))
        url = str(getMultiAdapter((parent, self.request), name=u"absolute_url"))
        return url + "/@@currency-controlpanel"


class CurrencyNamespace(object):
    """Currencies traversing.
    """
    implements(ITraversable)
    adapts(ISiteRoot, IBrowserRequest)

    def __init__(self, context, request=None):
        self.context=context
        self.request=request


    def traverse(self, name, ignore):
        currencies = getUtility(ICurrencyManager).currencies
        return currencies[name].__of__(self.context)

