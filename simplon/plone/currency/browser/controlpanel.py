import logging
from zope.component import getUtility
import zope.event
from zope.lifecycleevent import ObjectModifiedEvent
try:
    from Products.Five.formlib.formbase import EditForm
except:
    from five.formlib.formbase import EditForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib.form import FormFields
from zope.formlib.form import action
from zope.formlib.form import applyChanges
from zope.formlib.form import haveInputWidgets
from simplon.plone.currency.interfaces import IGlobalCurrencySettings
from Products.CMFPlone.utils import getFSVersionTuple
from plone.z3cform import layout
from z3c.form import form, button
from plone.autoform.form import AutoExtensibleForm
from simplon.plone.currency.interfaces import ICurrencyManager
from Products.CMFPlone import PloneMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
LOG = logging.getLogger(__name__)

def update_only_validator(form):
    """Only validate an action when updating.

    This allows you to create an action without having formlib render a
    button for it.
    """
    return "form_result" not in form.__dict__


def GlobalCurrencySettingsFactory(context=None):
    return getUtility(ICurrencyManager)


class ControlPanelForm(AutoExtensibleForm, form.EditForm):

    schema = IGlobalCurrencySettings
    label = u"Currency management"
    description = u""
    form_name = u"Currency management"

    template = ViewPageTemplateFile("controlpanel.pt")

    def currencies(self):
        config=GlobalCurrencySettingsFactory()

        def morph(cur):
            return dict(
                    code=cur.code,
                    symbol=cur.symbol,
                    rate=cur.rate,
                    description=cur.description,
                    protected=(cur.code==config.currency))

        return [morph(cur) for cur in config.currencies.values()]

    @button.buttonAndHandler(_(u"Apply", default=u"Apply"), name='apply')
    def handle_edit_action(self, action):
        message=IStatusMessage(self.request)
        config=GlobalCurrencySettingsFactory()
        oldcurrency=config.currency
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if self.applyChanges(data):
            newcurrency=config.currency
            if newcurrency!=oldcurrency:
                config.currency=oldcurrency
                config.SwitchCurrency(newcurrency)
            zope.event.notify(ObjectModifiedEvent(self.context))
            message.addStatusMessage(
                _("made_changes",
                    default=u"Changes applied"),
                type="info")

        else:
            message.addStatusMessage(
                _("no_changes",
                    default=u"Nothing changed"),
                type="info")


    @button.buttonAndHandler(_(u"Delete", default=u"Delete"), name='delete', condition=update_only_validator)
    def handle_delete_action(self, action):
        todo=[str(cur) for cur in self.request.form["currencies"]]
        config=GlobalCurrencySettingsFactory()
        message=IStatusMessage(self.request)

        succes=False
        for code in todo:
            if code!=config.currency:
                try:
                    del config.currencies[code]
                    succes=True
                except KeyError:
                    message.addStatusMessage(
                            _("remove_bogus_currency",
                                default=u"Failed to remove currency ${code}",
                                mapping=dict(code=code)),
                            type="error")

        if succes:
            message.addStatusMessage(
                    _("currencies_removed",
                        default=u"Currencies have been removed"),
                    type="info")

            
class ControlPanel(layout.FormWrapper):
    form = ControlPanelForm
