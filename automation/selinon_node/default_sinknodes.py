from enum import Enum
from .nodemixins import SinkNodeMixin


class NodeTypes(Enum):
    SOURCE = 1
    ACTION = 2
    CONDITION = 3
    SINK = 4


class BaseConnection(object):

    def is_connected(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def retrieve(self, flow_name, task_name, task_id):
        pass

    def store(self, flow_name, task_name, task_id, result):
        pass

    def store_error(self, node_args, flow_name, task_name, task_id, exc_info):
        pass


class AWSS3SinkNode(BaseConnection, SinkNodeMixin):
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
            {'name': 'bucket', 'value': self.bucket, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'aws_access_key_id', 'value': self.aws_access_key_id, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'aws_secret_access_key', 'value': self.aws_secret_access_key,
             'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'region_name', 'value': self.region_name, 'type': 'string'})

        return json_to_return


class MongoDBSinkNode(BaseConnection, SinkNodeMixin):
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
            {'name': 'db_name', 'value': self.db_name, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'collection_name', 'value': self.collection_name, 'type': 'string'})
        json_to_return['properties'].append({'name': 'host', 'value': self.host, 'type': 'string'})
        json_to_return['properties'].append({'name': 'port', 'value': self.port, 'type': 'int'})

        return json_to_return


class RedisSinkNode(BaseConnection, SinkNodeMixin):

    """ Sink Node for Redis """

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
        json_to_return['properties'].append({'name': 'db', 'value': self.db, 'type': 'string'})
        json_to_return['properties'].append(
            {'name': 'charset', 'value': self.charset, 'type': 'string'})
        json_to_return['properties'].append({'name': 'host', 'value': self.host, 'type': 'string'})
        json_to_return['properties'].append({'name': 'port', 'value': self.port, 'type': 'int'})

        return json_to_return
