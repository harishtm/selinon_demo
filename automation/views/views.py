import logging
import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from json.decoder import JSONDecodeError
from django.core import serializers
from django.shortcuts import render

from login.decorators import user_is_admin_user, breadcrumb

from ..models import NodeRegister, AutomationWorkflow
from settings.models import ErrorCodes
from store.models import Store
from digitmarketadmin.loading import get_class

logger = logging.getLogger('AM')

@csrf_exempt
def save_automation(request):
    try:
        jsonData = json.loads(request.body.decode('utf-8'))
        flowdata = jsonData['flow']
        workflow = None
        if flowdata['flowId']:
            if (flowdata['flowId'] == str(0)) or (flowdata['flowId'] == ''):
                workflow = AutomationWorkflow.create_workflow()
            else:
                workflow = AutomationWorkflow.objects.get(pk=flowdata['flowId'])
        else:
            workflow = AutomationWorkflow.create_workflow()
            
        if workflow:
            jsonData['flow']['flowId'] = workflow.pk
            thumbnailData = jsonData['flow'].pop('flowThumbnail', None)
            
            return JsonResponse(data={
                'flowId': workflow.save_or_update_workflow(flowdata=jsonData['flow'],
                    workflow=jsonData, thumbnail=thumbnailData,
                        store=Store.objects.get(pk=request.session['storeId']))}, 
                            safe=False)
        
    except JSONDecodeError:
        pass
    return JsonResponse(data={})
    
            


@login_required(login_url='/login/')
@user_is_admin_user
def get_automation(request):

    # get the flow identifier from the request
    try:
        flowId = request.GET['flowId']
    except KeyError:
        flowId = '0'

    # flow identifier is 0, which is newly created case
    if flowId == '0':
        # retrun empty placeholder data model for editor to update
         node_to_return = '{"flow":{"flowId": "0", "flowName": "", "flowThumbnail": "", "flowDescription" : "", "createdDate": ""}, "connections": [], "nodes":[]}'
    else:
        # fetch the flow based on identifier
        workflow = AutomationWorkflow.objects.get(pk = flowId)
        if workflow:
             # get the flow specification
             node_to_return = json.dumps(workflow.workflowSpec)
        else:
            node_to_return = '{"flow":{"flowId": "0", "flowName": "", "flowThumbnail": "", "flowDescription" : "", "createdDate": ""}, "connections": [], "nodes":[]}'
    return JsonResponse(json.loads(node_to_return), safe=False)

@breadcrumb(view_name='Automation List')
@login_required(login_url='/login/')
@user_is_admin_user
def atomation(request):
    return render(request, 'automation_list.html')

@breadcrumb(view_name='Create Automation')
@login_required(login_url='/login/')
@user_is_admin_user    
def automation_editor(request, pk):
    return render(request, 'automation_editor.html', { 'flowId' : pk})
    
def list_automation(request):
    logger.info('Automation Listing Page | Creating JSON for Automation Listing')
    
    """
    ---------------------------------------------------------------------------
    Function to return list of automation associated to the marketplace
    :param request: HTTP to render the list of automation
    :return:
    ---------------------------------------------------------------------------
    """
    # Get the list of automation from the database
    automations = AutomationWorkflow.objects.filter(
        store=Store.objects.get(pk=request.session['storeId']))
    automationsSize = len(automations)
    automationsList = { "data" : [] }
    if automationsSize:
        # Convert the object list into JSON serialize
        automations_serialize = serializers.serialize('json', automations)
        automation_json = json.loads(automations_serialize)
        automation_array = []
        iValP= 0
        # Construct the JSON response
        while iValP < len(automation_json):
            automation_json[iValP]["fields"]["id"] = automation_json[iValP]["pk"]
            automation_json[iValP]["fields"]["button"] = ""
            automation_array.append(automation_json[iValP]["fields"])
            iValP += 1
        
        automationsList["data"] = automation_array
        return JsonResponse(automationsList, status=200, safe=False)
    else:
        try:
            errorCodes = ErrorCodes.objects.filter(errorCode='ADM:0003', 
                errorLocale=settings.LANGUAGE_CODE)
            logger.error(errorCodes[0].errorDesc)
            return JsonResponse(automationsList, status=200, safe=False)
        except:
            return JsonResponse(automationsList, status=200, safe=False)
        
def delete_automation(request):
    try:
        jsonData = json.loads(request.body.decode('utf-8'))        
        
    except JSONDecodeError:
        logger.debug('No attribute selected')
        pass
    
    if (jsonData['list'])  != "":
        for iDel in range(len(jsonData['list'])):
            
            if(jsonData['list'][iDel]):                
                AutomationWorkflow.objects.filter(id = jsonData['list'][iDel]).delete()
            else:
                logger.error('Automation has not been saved in DB to delete it')
                
    else:
        logger.debug('No attribute selected')
        
    return HttpResponse("deleted", status=200)

def check_node_registration(class_name, package_name, store):
    try:
        node = NodeRegister.objects.get(store = store,
            python_class = class_name, python_package = package_name)
        if node:
            return (True, node)
        else:
            return (False, None)
    except NodeRegister.DoesNotExist:
        return (False, None)
        
def register_all_internal_nodes(store):
    # action nodes
    action_nodes = ['CheckForMessage', 'MessageLength', 'SuccessAction', 'FailureAction']
    action_node_packages = 'automation.selinon_node.default_action_nodes'
    # check Sink nodes
    sink_nodes = ['AWSS3SinkNode', 'MongoDBSinkNode', 'RedisSinkNode']
    sink_node_package = 'automation.selinon_node.default_sinknodes'

    condition_nodes = ['MessageCondition']
    condition_node_package = 'automation.selinon_node.default_condition_nodes'

    node_registry(store, sink_nodes, sink_node_package, 'Sink')
    node_registry(store, action_nodes, action_node_packages, 'Action')
    node_registry(store, condition_nodes, condition_node_package, 'Condition')


def node_registry(store='', nodes=[], node_package='automation.nodes', node_type=''):

    for node_name in nodes:
        status, node =  check_node_registration(node_name, node_package, store)
        if not status:
            try:
                store_instance = Store.objects.get(storeId = store)
                nodeobject = NodeRegister(store = store_instance, python_class = node_name, 
                    python_package = node_package, node_type = node_type)
                nodeobject.save()
            except Store.DoesNotExist:
                pass

    
def get_all_nodes(request):
    """
    Returns the nodes list in below format 
    {
        "nodes" : [{
            "name": "string",
            "description" : "string",
            "vesion": "string",
            "class": "string",
            "package": "string",
            "type" : "string",
            "configuration" : [{
                "name": "string",
                "value": "string",
                "type": "int/long/string/strings"
            }]
        }]
    }
    """
    register_all_internal_nodes(request.session.get('storeId'))
    
    nodes_to_return = {}

    nodes_to_return["nodes"] = []
    try:
        try:
            nodeType = request.GET['type']
        except KeyError:
            nodeType = 'Source'
            
        # get all registerd nodes and convert into the objects  based on nodeType
        nodes = NodeRegister.objects.filter(store = request.session.get('storeId'), 
            node_type=nodeType)
    
        # iterate through the nodes
        if nodes:
            for node in nodes:
                nodeObject = get_class(node.python_package, node.python_class, module_prefix='')
                nodes_to_return["nodes"].append(nodeObject.dump_json())
    except KeyError:
        pass
        
    return JsonResponse(nodes_to_return)
    
