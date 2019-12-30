from .nodemixins import ConitionNodeMixin


class MessageCondition(ConitionNodeMixin):

    def __init__(self, *args, **kwargs):
        super(MessageCondition, self).__init__('messagecondition',
                                               'Message Length Should be less than 100')
