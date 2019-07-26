from selinon import SelinonTask
from selinon.task_envelope import SelinonTaskEnvelope


class CheckMessage(SelinonTask):
    def run(self, node_args):
        """A simple hello world."""
        # import ipdb;ipdb.set_trace()
        print("============>>>>> I have completed Check Message", node_args)
        return "EEEEEEEEEEEEEEEEEEEEEE, {}!".format(node_args.get('name', 'world'))
        # return 'Success Result'


# Works from different file hello2

# class ValidateMessage(SelinonTask):
#     def run(self, node_args):
#         print("============>>>>> TRYYYYYY NEEWWW TASK", node_args)
#         return 'Success'
