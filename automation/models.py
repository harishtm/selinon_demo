
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile
from django_mysql.models import JSONField
from django.db import models
from django_mysql.models import JSONField
from .signals import workflow_changed
import base64


def validator_image_directory_path(instance, filename):
    return 'validator/{0}/files/{1}'.format(instance.id, filename)


def workflow_file_path(instance, filename):
    return 'workflow/{0}/files/{1}'.format(instance.id, filename)


class AutomationWorkflow(models.Model):

    thumbnail = models.ImageField(
        _("Thumbnail"), upload_to=validator_image_directory_path, max_length=255)

    name = models.CharField(_("Automation Workflow Name"), max_length=30)

    description = models.CharField(_("Automation Workflow Description"), max_length=30)

    totalRunCount = models.IntegerField(_('Total Run Count'), default=0)

    totalFailureCount = models.IntegerField(_('Total Failure Count'), default=0)

    workflowSpec = JSONField()

    created_date = models.DateTimeField(_("Registration Date"), blank=True, null=True,
                                        help_text=_("Date on workflow created"), auto_now_add=True)

    store = models.ForeignKey('store.Store', on_delete=models.CASCADE,
                              verbose_name=_("Store"), blank=True, null=True)

    flowspec = JSONField()

    class Meta:
        app_label = 'automation'

    @staticmethod
    def create_workflow():
        return AutomationWorkflow.objects.create()

    def save_or_update_workflow(self, flowdata=None, workflow=None, thumbnail=None, store=None):

        if flowdata:
            # save basic information about the workflow
            self.name = flowdata['flowName']
            self.description = flowdata['flowDescription']

        if thumbnail:
            # save thumbnail related to the workflow
            ext = 'png'
            format, imgstr = thumbnail.split(';base64,')
            if imgstr:
                data = ContentFile(base64.b64decode(imgstr))
                file_name = self.name + "." + 'png'
                self.thumbnail.delete()
                self.thumbnail.save(file_name, data, save=True)

        if store:
            self.store = store

        if workflow:
            # save workflow specification
            self.workflowSpec = workflow

        self.save()
        workflow_changed.send_robust(sender=self, workflowSpec=self.workflowSpec)

        return self.pk


class NodeRegister(models.Model):

    NodeTypes = (
        ('Source', _('Souorce Node')),
        ('Action', _('Action Execution Node')),
        ('Condition', _('Condition Node To Execute Validation')),
        ('Sink', _('Storage Node To Sink Data'))
    )

    python_class = models.CharField(_('Class Implementation'), max_length=100,
                                    null=False, blank=False)

    python_package = models.CharField(_('Package holds Class'), max_length=100,
                                      null=False, blank=False)

    node_type = models.CharField(_('Node Type'), choices=NodeTypes, max_length=20,
                                 null=False, blank=False, default='Source')

    registered = models.DateTimeField(_("Registration Date"), blank=True, null=True,
                                      help_text=_("Date on which node registered"),
                                      auto_now_add=True)

    version = models.FloatField(_("Node version"), default=1.0)

    store = models.ForeignKey('store.Store', on_delete=models.PROTECT,
                              verbose_name=_("Store"), blank=False, null=False)

    class Meta:
        unique_together = ('python_class', 'python_package',)


class TriggerWorkflow(models.Model):

    trigger = models.CharField(_('Trigger Name'),  max_length=255, blank=False, null=False)

    store = models.ForeignKey('store.Store', on_delete=models.CASCADE,
                              verbose_name=_("Store"), blank=True, null=True)

    workflow = models.ForeignKey('automation.AutomationWorkflow', on_delete=models.CASCADE,
                                 verbose_name=_('Automation Workflow'), blank=False, null=False)
