from selinon import SelinonTask
from selinon import DataStorage
from enum import Enum

from product import signals

import json
from random import randint

class NodeTypes(Enum):
    SOURCE = 1
    source = 2
    CONDITION = 3
    SINK = 4
    
    
class AbstractSourceNode(SelinonTask):
    
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
    Set  kwlass for the source node
    """
    def set_kwlass(self, kwlass):
        self.kwlass = kwlass
        
    """
    Set package for the source node
    """
    def set_python_package(self, package):
        self.package = package
    
    """
    Set node description
    """
    def set_description(self, description):
        self.description = description
                
    """
    Set default max retry value for the source node
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
    which determines the source execution results
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
    Sets the throttling for the source execution with interval type and value
    """
    def set_execution_throttling(self, throttle, value):
        self.throttle = throttle
        self.throttle_value = value
        
    """
    Converts the source node to JSON for front-end rendering
    """
    def dump_json(self):
        json_to_return = {}
        json_to_return['name'] = self.name
        json_to_return['type'] = str(self.type)
        json_to_return['description'] = self.description
        json_to_return['kwlass'] = self.kwlass
        json_to_return['package'] = self.package
        json_to_return['configuration'] = []
        json_to_return['configuration'].append(
            {'name': 'max_retry', 'value':self.max_retry, 'type': 'int'})
        json_to_return['configuration'].append(
            {'name': 'retry_interval', 'value':self.retry_interval, 'type': 'int'})
        json_to_return['configuration'].append(
            {'name': 'output_schema', 'value':self.output_schema, 'type': 'file'})
        json_to_return['configuration'].append(
            {'name': 'sink', 'value':self.sink, 'type': 'string'})
        json_to_return['configuration'].append(
            {'name': 'storage_readonly', 'value':self.storage_readonly, 'type': 'boolean'})
        json_to_return['configuration'].append(
            {'name': 'throttle', 'value':self.throttle, 'type': 'int'})
        json_to_return['configuration'].append(
            {'name': 'throttle_value', 'value':self.throttle_value, 'type': 'int'})
        
        return json_to_return
    
    """
    Configure method will be invoked to configure the node
    """
    def configure(self, name, value, type):
        setattr(self, name, value)
    
    def trigger(self, signal_event=[]):
    
        for event in signal_event:
            method_to_call = getattr(signals, event)
    
    """
    Execute method to be implemented by the source node implementation. 
    """
    def execute(self, dataset=None):
        return NotImplementedError

    """
    Run method from the SelinonTask  
    """
    def run(self, node_args):
        return {'dataset' : self.execute(node_args['dataset'])}
