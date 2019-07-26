from __future__ import absolute_import, unicode_literals
import os
from selinon import Config, run_flow
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selinon_demo.settings')

app = Celery('selinon_demo')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Config.set_pickel_config_object(MyDBConfig())

Config.set_celery_app(app)

app.autodiscover_tasks()

app.conf.task_routes = {'*': {'queue': 'hello_task'}}





# node_dict = {
#     'tasks': [{'name': 'CheckMessage', 'queue': 'hello_task', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'},
#              {'name': 'MessageLength', 'queue': 'hello_task', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'},
#              {'name': 'SuccessAction', 'queue': 'hello_task', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'},
#              {'name': 'FailureAction', 'queue': 'hello_task', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'}],
#      'flows': ['my_new_flow'],
#      'storages': [{'name': 'Redis', 'import': 'selinon.storages.redis', 'configuration': {'host': 'localhost', 'port':6379, 'db':1, 'charset': 'utf-8'}}],
#      'global': {'trace': {'json': True}},
#      'migration_dir': 'migration_dir'}


# flow_definition = [{'flow-definitions': [{'name': 'my_new_flow',
#                                               'queue': 'hello_task',
#                                               'sampling': {'name': 'constant', 'args': {'retry': 10}},
#                                               'edges': [{'from': '', 'to': 'CheckMessage'},
#                                                         {'from': 'CheckMessage', 'to': 'MessageLength'},
#                                                         {'from': 'MessageLength', 'to': 'SuccessAction', 
#                                                          'condition': {'name': 'fieldEqual',
#                                                                        'args': {'key': 'status', 'value': True}}},
#                                                         {'from': 'MessageLength', 'to': 'FailureAction',
#                                                          'condition': {'name': 'fieldEqual',
#                                                                        'args': {'key': 'status', 'value': False}}}],
#                                               'failures': [{'nodes': 'MessageLength', 'fallback': 'FailureAction'}]
#                                             }]
#                                         }]


# flow_defi_revse = [{'flow-definitions': [{'name': 'my_new_flow',
#                                               'queue': 'hello_task',
#                                               'sampling': {'name': 'constant', 'args': {'retry': 10}},
#                                               'edges': [{'from': '', 'to': 'CheckMessage'},
#                                                         {'from': 'CheckMessage', 'to': 'MessageLength'},
#                                                         {'from': 'MessageLength', 'to': 'SuccessAction', 
#                                                          'condition': {'and': [{'name': 'fieldEqual',
#                                                                                'args': {'key': 'status',
#                                                                                         'value': True}},
#                                                                                {'name': 'fieldEqual',
#                                                                                'args': {'key': 'checkvalue',
#                                                                                         'value': True}},
#                                                                                {'name': 'fieldEqual',
#                                                                                 'args': {'key': 'length',
#                                                                                         'value': True}}]}},
#                                                         {'from': 'MessageLength', 'to': 'FailureAction',
#                                                          'condition': {'name': 'fieldEqual',
#                                                                        'args': {'key': 'status', 'value': False}}}]
#                                             }]
#                                             }]





# Config.set_config_dict(node_dict, flow_defi_revse)

# dispatcher_id = run_flow('my_new_flow', {})





