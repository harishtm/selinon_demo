from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from celery.decorators import task
from selinon_demo.celery_config import get_selinon_config

# Create your views here.


from selinon.task_envelope import SelinonTaskEnvelope

@task(name="test")
def test():

    from selinon import run_flow, run_flow_selective

    
    print("===================================================")

    node_dict = {
        'tasks': [{'name': 'CheckMessage', 'queue': 'my_new_flow', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'},
                 {'name': 'MessageLength', 'queue': 'my_new_flow', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'},
                 {'name': 'SuccessAction', 'queue': 'my_new_flow', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'},
                 {'name': 'FailureAction', 'queue': 'my_new_flow', 'import': 'tasks', 'max_retry':0, 'storage': 'Redis'}],
         'flows': ['my_new_flow'],
         'storages': [{'name': 'Redis', 'import': 'selinon.storages.redis', 'configuration': {'host': 'localhost', 'port':6379, 'db':1, 'charset': 'utf-8'}}],
         'global': {'trace': {'json': True}},
         'migration_dir': 'migration_dir'}


    flow_definition = [{'flow-definitions': [{'name': 'my_new_flow',
                                              'queue': 'my_new_flow',
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
                                              'queue': 'my_new_flow',
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
    
    print(get_selinon_config().dispatcher_queues)

    get_selinon_config().set_config_dict(node_dict, flow_defi_revse)
    
    print("===================================================")

    dispatcher_id = run_flow('my_new_flow')

    print("===================================================")



def send_selinon(request):

    # import ipdb;ipdb.set_trace()

    
    # app.autodiscover_tasks()

    # subprocess.call('selinon-cli execute --nodes-definition ' + node_dict + '--flow-definitions ' + flow_definition + ', shell=True')
    test.apply_async()

    # run_flow_selective(dispatcher_id)
    # from celery import Task
    # Task
    return JsonResponse({'status': 'success'})