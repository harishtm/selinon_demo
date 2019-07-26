from django.shortcuts import render
from django.http import JsonResponse
from selinon import Config, run_flow
from selinon import Dispatcher
from selinon_demo import settings
from celery.decorators import task
from celery import Celery



import copy




# @task(name='workflowselinon')
def send_selinon(request):


    node_dict = {
    'tasks': [{'name': 'CheckMessage', 'queue': 'hello_task', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'},
             {'name': 'MessageLength', 'queue': 'hello_task', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'},
             {'name': 'SuccessAction', 'queue': 'hello_task', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'},
             {'name': 'FailureAction', 'queue': 'hello_task', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'}],
     'flows': ['my_new_flow'],
     'storages': [{'name': 'Redis', 'import': 'selinon.storages.redis', 'configuration': {'host': 'localhost', 'port':6379, 'db':1, 'charset': 'utf-8'}}],
     'global': {'trace': {'json': True}},
     'migration_dir': 'migration_dir'}


    flow_definition = [{'flow-definitions': [{'name': 'my_new_flow',
                                              'queue': 'hello_task',
                                              'sampling': {'name': 'constant', 'args': {'retry': 10}},
                                              'edges': [{'from': '', 'to': 'CheckMessage'},
                                                        {'from': 'CheckMessage', 'to': 'MessageLength'},
                                                        {'from': 'MessageLength', 'to': 'SuccessAction', 
                                                         'condition': {'name': 'fieldEqual',
                                                                       'args': {'key': 'status', 'value': True}}},
                                                        {'from': 'MessageLength', 'to': 'FailureAction',
                                                         'condition': {'name': 'fieldEqual',
                                                                       'args': {'key': 'status', 'value': False}}}],
                                              'failures': [{'nodes': 'MessageLength', 'fallback': 'FailureAction'}]
                                            }]
                                        }]


    flow_defi_revse = [{'flow-definitions': [{'name': 'my_new_flow',
                                              'queue': 'hello_task',
                                              'sampling': {'name': 'constant', 'args': {'retry': 10}},
                                              'edges': [{'from': '', 'to': 'CheckMessage'},
                                                        {'from': 'CheckMessage', 'to': 'MessageLength'},
                                                        {'from': 'MessageLength', 'to': 'SuccessAction', 
                                                         'condition': {'and': [{'name': 'fieldEqual',
                                                                               'args': {'key': 'status',
                                                                                        'value': True}},
                                                                               {'name': 'fieldEqual',
                                                                               'args': {'key': 'checkvalue',
                                                                                        'value': True}},
                                                                               {'name': 'fieldEqual',
                                                                                'args': {'key': 'length',
                                                                                        'value': True}}]}},
                                                        {'from': 'MessageLength', 'to': 'FailureAction',
                                                         'condition': {'name': 'fieldEqual',
                                                                       'args': {'key': 'status', 'value': False}}}]
                                            }]
                                            }]




    


   
    node_dict1 = copy.deepcopy(node_dict)
    flow_defi_revse1 = copy.deepcopy(flow_defi_revse)

    Config.set_config_dict(node_dict, flow_defi_revse)

    # print(Config.__dict__)

    # from selinon_demo import celery_config

    # Config.set_celery_app(celery_config.app)

    # celery_config.app.tasks.register(Dispatcher())
    
    # celery_config.app.autodiscover_tasks()
    # import ipdb;ipdb.set_trace()

    dispatcher_id = run_flow('my_new_flow', {}, node_dict1, flow_defi_revse1)

    dispatcher_id1 = run_flow('my_new_flow', {}, node_dict1, flow_definition)

    return JsonResponse({'status': 'success'})
    
