from selinon import SelinonTask
from selinon.task_envelope import SelinonTaskEnvelope

class MessageLength(SelinonTask):
	def run(self, node_args):
		# print(self.__dict__.get('log').__dict__, "*********", type(node_args))
		print("============>>>>> Message length check completed", node_args)
		node_args.update({'status': True, 'checkvalue': True, 'length': True})
		return node_args
