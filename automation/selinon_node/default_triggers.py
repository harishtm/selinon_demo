from .nodemixins import TriggerMixin

class ProductRatingTrigger(TriggerMixin):

    def __init__(self, scope, intent):
        self.scope = scope
        self.intent = intent

    # def process(self):
    #     print('Processing')


class ProductCommentTrigger(TriggerMixin):

    def __init__(self, scope, intent):
        self.scope = scope
        self.intent = intent




# from django.dispatch import receiver
# from ..signals import workflow_changed
# from django.dispatch.dispatcher import Signal
# from django.db.models.signals import post_save



# class ProductCommentTrigger(TriggerMixin):

#     @classmethod
#     @receiver(workflow_changed, dispatch_uid="ProductCommentTrigger.call_back")
#     def call_back(self, sender, **kwargs):
#         print("====>>>>", **kwargs)
#         if kwargs['scope'] == 'User' and kwargs['intent'] == 'ProductCommentAdded':
#             # kwargs['data']
#             print("====>>>>")

#     def call_back(self, sender, **kwargs):
#         from django.dispatch.dispatcher import Signal
#         Signal.connect(dispatch_uid='automation_workflow_changed')
#         print("====>>>>")

#     def __call__(self, *args, **kwargs):
#         @receiver(workflow_changed, dispatch_uid="automation_workflow_changed")
#         def foo(sender, workflowSpec, **kwargs):
#             print("YOUUUUUUU")