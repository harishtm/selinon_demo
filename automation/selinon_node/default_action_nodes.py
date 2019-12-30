from .nodemixins import ActionNodeMixin
# from servicemarket.models import ServiceComments


class CheckForMessage(ActionNodeMixin):

    """ Check message contents"""

    def __init__(self, *args, **kwargs):
        super(CheckForMessage, self).__init__('checkmessages', 'CheckForMessage',
                                              'automation.nodes',
                                              'Checks for the message contents')

    def run(self, node_args):
        service_comments = ServiceComments.objects.filter(block_status=False)
        print("====>>>", "Message Validated")
        return True


class MessageLength(ActionNodeMixin):

    def __init__(self, *args, **kwargs):
        super(MessageLength, self).__init__('messagelength', 'Message Length',
                                            'automation.nodes',
                                            'Check the message length')

    def run(self, node_args):
        print('=====>>>>', 'MessageLength Succeded')
        return True


class SuccessAction(ActionNodeMixin):

    def __init__(self, *args, **kwargs):
        super(SuccessAction, self).__init__('success', 'Success Action',
                                            'automation.nodes',
                                            'Success action')

    def run(self, node_args):
        print('=====>>>>', 'SuccessAction Succeded')
        return True


class FailureAction(ActionNodeMixin):

    def __init__(self, *args, **kwargs):
        super(FailureAction, self).__init__('failuer', 'Failure Action',
                                            'automation.nodes',
                                            'Failure Action')

    def run(self, node_args):
        print('=====>>>>', 'FailureAction Succeded')
        return True
