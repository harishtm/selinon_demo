from selinon import SelinonTask
from selinon.task_envelope import SelinonTaskEnvelope


class FailureAction(SelinonTask):
	def run(self, node_args):
		print("============>>>>> Failure Node ", node_args)
		return {'status': False}
	