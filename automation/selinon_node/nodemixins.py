from selinon import SelinonTask, DataStorage
from random import randint
from enum import Enum


class NodeTypes(Enum):

    """ Set of Node Type"""

    SOURCE = 1
    ACTION = 2
    CONDITION = 3
    SINK = 4


class ActionNodeMixin(SelinonTask):

    """Base class for all automation action to be performed"""

    def __init__(self, name, description, kwlass, package, *args, **kwargs):
        """ Initialize Action Node.
        :param name: name of the flow under which task runs
        :param kwlass: name of the class
        :param package: package name
        :params description: description of the node
        """
        self.name = name + '_' + str(randint(1000, 9999))
        self.type = NodeTypes.ACTION
        self.kwlass = kwlass
        self.package = package
        self.description = description
        self.max_retry = 0
        self.retry_interval = 10
        self.output_schema = ''
        self.sink = ''
        self.storage_readonly = False
        self.throttle = ''
        self.throttle_value = 0

    def set_max_retry(self, max_retry):
        """
            Set default max retry value for the Action node
        """
        self.max_retry = max_retry

    def set_retry_interval(self, retry_interval):
        """
            Set default retry interval window between the execution intervals
        """
        self.retry_interval = retry_interval

    def set_output_schema_validation(self, output_schema):
        """
            Set output schema in the JSON format to validate the execution results
            which determines the Action execution results
        """
        self.output_schema = output_schema

    def set_storage(self, sink):
        """
            Set default sink node to be used to sink the data
        """
        self.sink = sink

    def set_storage_read_only(self, readonly):
        """
            Sets whether to use the storage as readonly
        """
        self.storage_readonly = readonly

    def set_execution_throttling(self, throttle, value):
        """
            Sets the throttling for the action execution with interval type and value
        """
        self.throttle = throttle
        self.throttle_value = value

    def dump_json(self):
        """Converts the action node to JSON for front-end rendering"""
        json_to_return = {}
        json_to_return['name'] = self.name
        json_to_return['type'] = str(self.type)
        json_to_return['description'] = self.description
        json_to_return['kwlass'] = self.__class__.__name__
        json_to_return['package'] = self.__module__
        json_to_return['properties'] = []
        json_to_return['properties'].append(
            {'name': 'max_retry', 'value': self.max_retry, 'type': 'int'})
        json_to_return['properties'].append(
            {'name': 'retry_interval', 'value': self.retry_interval, 'type': 'int'})
        json_to_return['properties'].append(
            {'name': 'output_schema', 'value': self.output_schema, 'type': 'file'})
        json_to_return['properties'].append(
            {'name': 'sink', 'value': self.sink, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'storage_readonly', 'value': self.storage_readonly, 'type': 'boolean'})
        json_to_return['properties'].append(
            {'name': 'throttle', 'value': self.throttle, 'type': 'int'})
        json_to_return['properties'].append(
            {'name': 'throttle_value', 'value': self.throttle_value, 'type': 'int'})

        return json_to_return


class SinkNodeMixin(DataStorage):

    """
        Sink Node mixin to sink the node to specific data storage
    """

    def __init__(self, name, description, kwlass, package, *args, **kwargs):
        """ Initialize Sink Node.
        :param name: name of the flow under which task runs
        :param kwlass: name of the class
        :param package: package name
        :params description: description of the node
        """
        self.name = name + '_' + str(randint(1000, 9999))
        self.type = NodeTypes.SINK
        self.kwlass = kwlass
        self.package = package
        self.description = description
        self.host = 'localhost'
        self.port = '000'

    def is_connected(self):
        raise NotImplementedError()

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()

    def retrieve(self, flow_name, task_name, task_id):
        raise NotImplementedError()

    def store(self, flow_name, task_name, task_id, result):
        raise NotImplementedError()

    def store_error(self, node_args, flow_name, task_name, task_id, exc_info):
        raise NotImplementedError()


class ConitionNodeMixin:

    def __init__(self, name, description, *args, **kwargs):
        self.name = name
        self.type = NodeTypes.CONDITION
        self.description = description

        self.success_node = ''
        self.success_keys = []
        self.success_value = ''

        self.failure_node = ''
        self.failure_keys = []
        self.failure_value = ''

    def add_success_key(self, key):
        self.success_keys.append(key)

    def associate_success_node(self, node):
        self.success_node = node

    def set_success_value(self, value):
        self.success_value = value

    def add_failure_key(self, key):
        self.failure_keys.append(key)

    def associate_failure_node(self, node):
        self.failure_node = node

    def set_failure_value(self, value):
        self.failure_value = value

    def dump_json(self):
        json_to_return = {}
        json_to_return['name'] = self.name
        json_to_return['description'] = self.description

        json_to_return['properties'] = []

        json_to_return['properties'].append(
            {'name': 'success_args_key', 'value': self.success_keys, 'type': 'strings'})
        json_to_return['properties'].append(
            {'name': 'success_args_value', 'value': self.success_value, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'success_node', 'value': self.success_node, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'failure_args_key', 'value': self.failure_keys, 'type': 'strings'})
        json_to_return['properties'].append(
            {'name': 'failure_args_value', 'value': self.failure_value, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'failure_node', 'value': self.failure_node, 'type': 'string'})
        return json_to_return


from .trigger_register import TriggerRegistry

class TriggerMixin:

    def __new__(cls, *args, **kwargs):
        """
         initialization of a new instance to register the trigger class
        """
        trobj = TriggerRegistry(cls, args[0], args[1])
        if cls not in [[*trig.keys()][0] for trig in trobj.trigger_registry.get('trigger')]:
            trobj.update({cls: {'scope': args[0], 'intent': args[1]}})
        return object.__new__(cls)

    def __init__(self, name, description, *args, **kwargs):
        """
        Initialization
        """
        self.name = name
        self.description = description


    def process(self, store_id=None, scope=None, intent=None):
        """
        Default implementation Initiate Identify the store based workflow
        """
        if store_id:
            tr = TriggerRegistry()
            scope_intent_dict = [[*trg.values()][0] for trg in tr.trigger_registry.get('trigger')]
            worflow_list = TriggerWorkflow.objects.filter(store__storeId=store_id)


    def get_initial_node_args(self):
        """
        """
        pass
