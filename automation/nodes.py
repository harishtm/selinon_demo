from selinon import SelinonTask
from selinon import DataStorage
from enum import Enum

import json
from random import randint

class NodeTypes(Enum):
    SOURCE = 1
    ACTION = 2
    CONDITION = 3
    SINK = 4
    
    
class ValidatorNodeThrottle(Enum):
    DAYS = 1,
    SECONDS = 2,
    MICROSECONDS = 3,
    MILLISECONDS = 4,
    MINUTES = 5,
    HOURS = 4,
    WEEKS = 6
    
class SinkNodeOptions(Enum):
    MYSQL_DB = 1,
    CACHE_REDIS = 2,
    MONGO_DB  = 3,
    POSTGRES_DB = 4,
    AWS_S3 = 5,
    MEMORY = 6,
    CUSTOM = 7

class AWSS3SinkNode:
    def __init__(self, *args, **kwargs):
        self.name = 'AWSS3SinkNode'
        self.description = 'Node to sink the data to S3 bucket, configure' \
            'node with access key and key to sink the data into the S3 bucket'
        self.kwlass = 'S3Storage'
        self.package = 'selinon.storages.s3'
        self.type = NodeTypes.SINK
        self.bucket = 'my-bucket-name'
        self.aws_access_key_id = 'AAAAAAAAAAAAAAAAAAAA'
        self.aws_secret_access_key = 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
        self.region_name = 'us-east-1'
        
    def set_bucket_name(self, bucket_name):
        self.bucket = bucket_name
        
    def set_aws_access_key(self, aws_access_key):
        self.aws_access_key_id = aws_access_key
        
    def set_aws_secret_access_key(self, aws_secret_access_key):
        self.aws_secret_access_key = aws_secret_access_key
        
    def set_aws_region(self, region_name):
        self.region_name = region_name

    def dump_json(self):
        json_to_return = {}
        json_to_return['name'] = self.name
        json_to_return['type'] = str(self.type)
        json_to_return['description'] = self.description
        json_to_return['kwlass'] = self.kwlass
        json_to_return['package'] = self.package
        
        json_to_return['properties'] = []
        json_to_return['properties'].append(
            {'name':'bucket', 'value':self.bucket, 'type':'string'})
        json_to_return['properties'].append(
            {'name':'aws_access_key_id', 'value':self.aws_access_key_id, 'type':'string'})
        json_to_return['properties'].append(
            {'name':'aws_secret_access_key', 'value':self.aws_secret_access_key, 'type':'string'})
        json_to_return['properties'].append(
            {'name':'region_name', 'value':self.region_name, 'type':'string'})

        return json_to_return

class MongoDBSinkNode:
    def __init__(self, *args, **kwargs):
        self.name = 'MongoDBSinkNodengoDBSkink'
        self.description = 'Node to sink the data to mongodb, configure' \
            'node with database connection string to sink the data into the mongodb'
        self.kwlass = 'MongoDB'
        self.package = 'selinon.storages.mongodb'
        self.type = NodeTypes.SINK
        self.db_name = 'database_name'
        self.collection_name = 'collection_name'
        self.host = 'localhost'
        self.port = '27017'
        
    def set_db_name(self, db_name):
        self.db_name = db_name
        
    def set_collection_name(self, collection_name):
        self.collection_name = collection_name
        
    def set_host(self, host):
        self.host = host
        
    def set_port(self, port):
        self.port = port

    def dump_json(self):
        json_to_return = {}
        json_to_return['name'] = self.name
        json_to_return['type'] = str(self.type)
        json_to_return['description'] = self.description        
        json_to_return['kwlass'] = self.kwlass
        json_to_return['package'] = self.package
        json_to_return['properties'] = []
        json_to_return['properties'].append(
            {'name':'db_name', 'value':self.db_name, 'type':'string'})
        json_to_return['properties'].append(
            {'name':'collection_name', 'value':self.collection_name, 'type':'string'})
        json_to_return['properties'].append({'name':'host', 'value':self.host, 'type':'string'})
        json_to_return['properties'].append({'name':'port', 'value':self.port, 'type':'int'})
        
        return json_to_return
        
class RedisSinkNode:
    def __init__(self, *args, **kwargs):
        self.name = 'RedisSinkNode'
        self.description = 'Node to sink the data to Redis cache, configure' \
            'node with redis connectivity details to store the data in Redis store'
        self.kwlass = 'Redis'
        self.package = 'selinon.storages.redis'
        self.type = NodeTypes.SINK
        self.db = '0'
        self.charset = 'utf-8'
        self.host = 'redishost'
        self.port = '6379'
        
    def set_db(self, db):
        self.db = db
        
    def set_charset(self, charset):
        self.charset = charset
        
    def set_host(self, host):
        self.host = host
        
    def set_port(self, port):
        self.port = port

    def dump_json(self):
        json_to_return = {}
        json_to_return['name'] = self.name
        json_to_return['description'] = self.description
        json_to_return['type'] = str(self.type)
        json_to_return['kwlass'] = self.kwlass
        json_to_return['package'] = self.package
        json_to_return['properties'] = []
        json_to_return['properties'].append({'name':'db', 'value':self.db, 'type':'string'})
        json_to_return['properties'].append(
            {'name':'charset', 'value':self.charset, 'type':'string'})
        json_to_return['properties'].append({'name':'host', 'value':self.host, 'type':'string'})
        json_to_return['properties'].append({'name':'port', 'value':self.port, 'type':'int'})

        return json_to_return
        
class SinkNode(DataStorage):

    def __init__(self, name, description, kwlass, package, *args, **kwargs):
        self.name = name + '_' + str(randint(1000, 9999))
        self.type = NodeTypes.SINK
        self.kwlass = kwlass
        self.package = package
        self.description = description
        self.host = 'localhost'
        self.port = '000'
        
    def is_connected():
        raise NotImplementedError()
    
    def connect():
        raise NotImplementedError()
        
    def disconnect():
        raise NotImplementedError()
        
    def retrieve(self, flow_name, task_name, task_id):
        raise NotImplementedError()

    def store(self, flow_name, task_name, task_id, result):
        raise NotImplementedError()

    def store_error(self, node_args, flow_name, task_name, task_id, exc_info):
        raise NotImplementedError() 
    
    def dump_json(self):
        json_to_return = {}
        json_to_return['name'] = self.name
        json_to_return['type'] = str(self.type)
        json_to_return['description'] = self.description
        json_to_return['kwlass'] = self.kwlass
        json_to_return['package'] = self.package
        
        json_to_return['properties'] = []
        json_to_return['properties'].append({'name':'host', 'value':self.host, 'type':'string'})
        json_to_return['properties'].append({'name':'port', 'value':self.port, 'type':'int'})
        return json_to_return
        
class ConditionNode:
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
            {'name': 'success_args_key', 'value':self.success_keys, 'type': 'strings'})
        json_to_return['properties'].append(
            {'name': 'success_args_value', 'value':self.success_value, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'success_node', 'value':self.success_node, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'failure_args_key', 'value':self.failure_keys, 'type': 'strings'})
        json_to_return['properties'].append(
            {'name': 'failure_args_value', 'value':self.failure_value, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'failure_node', 'value':self.failure_node, 'type': 'string'})
        return json_to_return       
 
class ActionNode(SelinonTask):
    
    """
    Set the action node name, to maintain unique, random generated id will be attached
    to the action node for example:
    
    if user sets the node name as 'CommentsAction' then node name will be set as 
    'CommentsAction_98090'
    """
    def __init__(self, name, description, kwlass, package, *args, **kwargs):
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
        
    """
    Set default max retry value for the Action node
    """
    def set_max_retry(self, max_retry):
        self.max_retry = max_retry
    
    """
    Set default retry interval window between the execution intervals
    """
    def set_retry_interval(self, retry_interval):
        self.retry_interval = retry_interval
    
    """
    Set output schema in the JSON format to validate the execution results
    which determines the Action execution results
    """
    def set_output_schema_validation(self, output_schema):
        self.output_schema = output_schema
   
    """
    Set default sink node to be used to sink the data
    """
    def set_storage(self, sink):
        self.sink = sink
    
    """
    Sets whether to use the storage as readonly 
    """
    def set_storage_read_only(self, readonly):
        self.storage_readonly = readonly
    
    """
    Sets the throttling for the action execution with interval type and value
    """
    def set_execution_throttling(self, throttle, value):
        self.throttle = throttle
        self.throttle_value = value
    
    
    """
    Converts the action node to JSON for front-end rendering
    """
    def dump_json(self):
        json_to_return = {}
        json_to_return['name'] = self.name
        json_to_return['type'] = str(self.type)
        json_to_return['description'] = self.description
        json_to_return['kwlass'] = self.kwlass
        json_to_return['package'] = self.package
        json_to_return['properties'] = []
        json_to_return['properties'].append(
            {'name': 'max_retry', 'value':self.max_retry, 'type': 'int'})
        json_to_return['properties'].append(
            {'name': 'retry_interval', 'value':self.retry_interval, 'type': 'int'})
        json_to_return['properties'].append(
            {'name': 'output_schema', 'value':self.output_schema, 'type': 'file'})
        json_to_return['properties'].append(
            {'name': 'sink', 'value':self.sink, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'storage_readonly', 'value':self.storage_readonly, 'type': 'boolean'})
        json_to_return['properties'].append(
            {'name': 'throttle', 'value':self.throttle, 'type': 'int'})
        json_to_return['properties'].append(
            {'name': 'throttle_value', 'value':self.throttle_value, 'type': 'int'})
        
        return json_to_return
        
    """
    Run method from the SelinonTask to be implemented
    by the validator node implementation. 
    """
    def run(self, node_args):
        return NotImplementedError()


class SourceNode(SelinonTask):
    
    """
    Set the source node name, to maintain unique, random generated id will be attached
    to the source node
    """
    def __init__(self, name, description, kwlass, package, *args, **kwargs):
        self.name = name + '_' + str(randint(1000, 9999))
        self.type = NodeTypes.SOURCE
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
        
    """
    Set default max retry value for the validator node
    """
    def set_max_retry(self, max_retry):
        self.max_retry = max_retry
    
    """
    Set default retry interval window between the execution intervals
    """
    def set_retry_interval(self, retry_interval):
        self.retry_interval = retry_interval
    
    """
    Set output schema in the JSON format to validate the execution results
    which determines the validator execution results
    """
    def set_output_schema_validation(self, output_schema):
        self.output_schema = output_schema
   
    """
    Set default sink node to be used to sink the data
    """
    def set_storage(self, sink):
        self.sink = sink
    
    """
    Sets whether to use the storage as readonly 
    """
    def set_storage_read_only(self, readonly):
        self.storage_readonly = readonly
    
    """
    Sets the throttling for the validator execution with interval type and value
    """
    def set_execution_throttling(self, throttle, value):
        self.throttle = throttle
        self.throttle_value = value
    
    
    """
    Converts the validator node to JSON for front-end rendering
    """
    def dump_json(self):
        json_to_return = {}
        json_to_return['name'] = self.name
        json_to_return['type'] = str(self.type)
        json_to_return['description'] = self.description
        json_to_return['kwlass'] = self.kwlass
        json_to_return['package'] = self.package
        json_to_return['properties'] = []
        json_to_return['properties'].append(
            {'name': 'max_retry', 'value':self.max_retry, 'type': 'int'})
        json_to_return['properties'].append(
            {'name': 'retry_interval', 'value':self.retry_interval, 'type': 'int'})
        json_to_return['properties'].append(
            {'name': 'output_schema', 'value':self.output_schema, 'type': 'file'})
        json_to_return['properties'].append(
            {'name': 'sink', 'value':self.sink, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'storage_readonly', 'value':self.storage_readonly, 'type': 'boolean'})
        json_to_return['properties'].append(
            {'name': 'throttle', 'value':self.throttle, 'type': 'int'})
        json_to_return['properties'].append(
            {'name': 'throttle_value', 'value':self.throttle_value, 'type': 'int'})
        
        return json_to_return
        
    """
    Run method from the SelinonTask to be implemented
    by the validator node implementation. 
    """
    def run(self, node_args):
        return NotImplementedError()
        
        
        
class CheckForMessage(ActionNode):
    def __init__(self):
        super(CheckForMessage, self).__init__(
            "checkformessages", "asdadasdasd", "CheckForMessage", "automation.selinon")
    def run(self, node_arg):
        pass
        
class DefaultCondition(ConditionNode):
    
    def __init__(self):
        super(DefaultCondition, self).__init__(
            "default_condition", "default condition to make true or false decision")
        self.add_success_key('status')
        self.add_failure_key('status')
        self.set_success_value('True')
        self.set_success_value('False')
        
       