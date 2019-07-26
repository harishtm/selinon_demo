from selinon import SelinonTask
from selinon.task_envelope import SelinonTaskEnvelope


class SuccessAction(SelinonTask):
	def run(self, node_args):
		print("============>>>>> SuccessAction Node ", node_args)
		return {'status': True}
	