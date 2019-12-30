from django.dispatch import receiver
from .signals import workflow_changed
from .selinonconfig import AutomationConfig
import json



@receiver(workflow_changed, dispatch_uid="automation_workflow_changed")
def receive_workflow_change(sender, workflowSpec, **kwargs):
    config = AutomationConfig(sender)
    seliconfig = {'node': config.construct_node(),
                  'flowdefinition': config.construct_flow_definition()}
    sender.flowspec = json.dumps(seliconfig)
    sender.save()


# @receiver(scope_intent_recieved, dispatch_uid="on_scope_intent_recieved")
# def scope_intent_receiver(sender, scope, intent, referce_object, **kwargs):
#     if kwargs['scope'] == 'User' and kwargs['intent'] == 'ProductCommentAdded':
#     	pass

