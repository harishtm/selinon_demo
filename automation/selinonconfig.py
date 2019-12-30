node_dict = {
    'tasks': [{'name': 'CheckMessage', 'queue': 'hello_task', 'import': 'tasks',
               'max_retry': 0, 'storage': 'Redis'},
              {'name': 'MessageLength', 'queue': 'hello_task', 'import': 'tasks',
               'max_retry': 0, 'storage': 'Redis'},
              {'name': 'SuccessAction', 'queue': 'hello_task', 'import': 'tasks',
               'max_retry': 0, 'storage': 'Redis'},
              {'name': 'FailureAction', 'queue': 'hello_task', 'import': 'tasks',
               'max_retry': 0, 'storage': 'Redis'}],
    'flows': ['my_new_flow'],
    'storages': [{'name': 'Redis', 'import': 'selinon.storages.redis',
                  'configuration': {'host': 'localhost', 'port': 6379, 'db': 1,
                                    'charset': 'utf-8'}}],
    'global': {'trace': {'json': True}},
    'migration_dir': 'migration_dir'}

flow_definition = [{'flow-definitions': [{'name': 'my_new_flow',
                                          'queue': 'hello_task',
                                          'sampling': {'name': 'constant', 'args': {'retry': 10}},
                                          'edges': [{'from': '', 'to': 'CheckMessage'},
                                                    {'from': 'CheckMessage', 'to': 'MessageLength'},
                                                    {'from': 'MessageLength', 'to': 'SuccessAction',
                                                     'condition': {'name': 'fieldEqual',
                                                                   'args': {'key': 'status',
                                                                            'value': True}}},
                                                    {'from': 'MessageLength', 'to': 'FailureAction',
                                                     'condition': {'name': 'fieldEqual',
                                                                   'args': {'key': 'status',
                                                                            'value': False}}}],
                                          'failures': [{'nodes': 'MessageLength',
                                                        'fallback': 'FailureAction'}]}]}]


class AutomationConfig(object):
    """ Construct selinon config """

    def __init__(self, automation_workflow_obj=None):
        """ Initialize the AutomationConfig
            :params: automationworkflow object
            :type Query Object:
        """
        if automation_workflow_obj:
            self.workflowspec = automation_workflow_obj.workflowSpec

    def find_task_storage(self, target_id=''):
        """ Finds the storage class for the specifed target node
            params: targetId
            returns: Boolean(whether storage exists)
                     if exists returns the storage class
        """
        for node in self.workflowspec.get('nodes', []):
            if node.get('config', {}).get('type') == 'sink' and node.get('id') == target_id:
                return (True, node.get('kwlass'), )
        return (False, node.get('kwlass'))

    def construct_task(self):
        """ Construct task
            :params: AutomationWorkflow
                    Get the workflow spec from DB
            returns: list of dictionary containg tasks
        """
        task_list = []
        for conn in self.workflowspec.get('connections', []):
            source_node = [node
                           for node in self.workflowspec.get('nodes')
                           if node.get('id') == conn.get('sourceId')][0]
            if source_node.get('config', {}).get('type', '') == 'action':
                task = {}
                task['name'] = source_node.get('kwlass')
                task['queue'] = source_node.get('name')
                task['import'] = source_node.get('package')
                task['max_retry'] = [np.get('value')
                                     for np in source_node.get('properties')
                                     if np.get('name') == 'max_retry'][0]
                task_storage, storage_class = self.find_task_storage(conn.get('targetId'))
                if task_storage:
                    task['storage'] = storage_class
                task_list.append(task)
        return task_list

    def construct_storages(self):
        """ Construct storage
            :params: AutomationWorkflow
                    Get the workflow spec from DB
            returns: list of dictionary containg storages
        """
        storage_list = []
        sink_nodes = [node
                      for node in self.workflowspec.get('nodes', [])
                      if node.get('config', {}).get('type', '') == 'sink']
        sink_nodes = self.remove_duplicate_sink_nodes(sink_nodes)
        for node in sink_nodes:
            storage, configuration = {}, {}
            storage['name'] = node.get('kwlass')
            storage['import'] = node.get('package')
            configuration = {prop.get('name'): (int(prop.get('value'))
                             if prop.get('value').isdigit() else prop.get('value'))
                             for prop in node.get('properties', [])}
            storage['configuration'] = configuration
            storage_list.append(storage)
        return storage_list

    def remove_duplicate_sink_nodes(self, sink_nodes=[]):
        """
            Removes duplicate sink nodes
        """
        unique_storage_list, storagename = [], set()
        for sn in sink_nodes:
            if sn['name'] not in storagename:
                unique_storage_list.append(sn)
                storagename.add(sn['name'])
        return unique_storage_list

    def construct_node(self):
        """ Construct a node to selinon """
        node_dict = dict()
        node_dict['tasks'] = self.construct_task()
        node_dict['flows'] = [self.workflowspec.get('flow', {}).get('flowName')]
        node_dict['storages'] = self.construct_storages()
        node_dict['global'] = {'trace': {'json': True}}
        node_dict['migration_dir'] = 'migration_dir'
        return node_dict

    def construct_flow_definition(self):
        """ Constructs a flow defintion """
        flow_list, edges, flow, single_flow = [], [], {}, {}

        for indx, conn in enumerate(self.workflowspec.get('connections', [])):
            # edges are constructed
            single_edge = {}
            if indx == 0:
                single_edge['from'] = ''
                single_edge['to'] = self.find_source_edge_from(conn.get('sourceId'))
                edges.append(single_edge)
                to = self.find_source_edge_to(conn.get('targetId'))
                if to:
                    single_edge = {}
                    single_edge['from'] = self.find_source_edge_from(conn.get('sourceId'))
                    single_edge['to'] = to
                    edge_condition = self.get_edge_condtion(conn.get('sourceId'),
                                                            conn.get('data', {}).get('condition'),
                                                            [])
                    if edge_condition:
                        single_edge['condition'] = edge_condition
                    edges.append(single_edge)
            else:
                if (self.is_condition_node(conn.get('sourceId')) and
                        not self.is_condition_node(conn.get('targetId'))):
                    single_edge['from'] = self.find_reverse_source_node(conn.get('sourceId'))
                    single_edge['to'] = self.find_kwlass_name(conn.get('targetId'))

                    condition_list = self.get_edge_condtion(conn.get('sourceId'),
                                                            conn.get('data', {}).get('condition'),
                                                            [])
                    if condition_list:
                        if len(condition_list) > 1:
                            single_edge['condition'] = {'and': condition_list}
                        else:
                            single_edge['condition'] = condition_list[0]
                    edges.append(single_edge)

        # flow is constructed a single flow
        flow['name'] = self.workflowspec.get('flow', {}).get('flowName')
        # TODO find queue
        flow['queue'] = 'task_queue'
        flow['sampling'] = {'name': 'constant', 'args': {'retry': 20}}
        flow['edges'] = edges

        # Flow list (containing list of dictionary)
        flow_list.append(flow)
        single_flow['flow-definitions'] = flow_list

        return single_flow

    def get_edge_condtion(self, source_id, boolval, condition_list=[]):
        """ Construct condition for edges """
        for conn in self.workflowspec.get('connections', []):
            if conn.get('sourceId') == source_id and self.is_condition_node(conn.get('sourceId')):
                condition = self.get_condtion(conn, boolval)
                if condition:
                    condition_list.append(condition)
                    for revcon in self.workflowspec.get('connections', []):
                        if (revcon.get('targetId') == conn.get('sourceId') and
                                self.is_condition_node(revcon.get('sourceId'))):
                            return self.get_edge_condtion(revcon.get('sourceId'),
                                                          revcon.get('data', {}).get('condition'),
                                                          condition_list)
        return condition_list

    @staticmethod
    def get_condtion(conn, boolval):
        """ Check the connection and set the condition if exists any """
        condition = {}
        if conn.get('data', {}).get('condition') == boolval:
            condition = {'name': 'fieldEqual',
                         'args': {'key': 'status',
                                  'value': conn.get('data', {}).get('condition')}}
        return condition

    def find_source_edge_from(self, source_id=''):
        """ Find the from edge for flow definition"""
        for node in self.workflowspec.get('nodes', []):
            if node.get('id') == source_id and node.get('config', {}).get('type') == 'action':
                return node.get('kwlass', '')
            elif node.get('id') == source_id and node.get('config', {}).get('type') == 'condition':
                return self.get_condition_source_edge(source_id)
        return ''

    def find_source_edge_to(self, target_id=''):
        """ Find the to edge for flow definition """
        for node in self.workflowspec.get('nodes', []):
            if node.get('id') == target_id and node.get('config', {}).get('type') == 'action':
                return node.get('kwlass', '')
            elif node.get('id') == target_id and node.get('config', {}).get('type') == 'condition':
                return self.find_next_action_node(target_id)
        return ''

    def get_condition_source_edge(self, source_id=''):
        """ Find the source edge for condition node """
        edgename = ''
        for conn in self.workflowspec.get('connections', []):
            if conn.get('targetId') == source_id:
                reverse_source_id = conn.get('sourceId')
                edgename = [node.get('kwlass', '')
                            for node in self.workflowspec.get('nodes', [])
                            if node.get('id') == reverse_source_id][0]
        return edgename

    def find_kwlass_name(self, id):
        """ Finds the class name for the given source / target id"""
        for node in self.workflowspec.get('nodes', []):
            if node.get('id') == id and node.get('config', {}).get('type') == 'action':
                return node.get('kwlass', '')
        return ''

    def find_next_action_node(self, target_id):
        """ Recursive method to find the next action node """
        action_node_id = None
        kwlass = ''
        for indx, conn in enumerate(self.workflowspec.get('connections', [])):
            if conn.get('sourceId') == target_id:
                if self.is_condition_node(conn.get('targetId')):
                    self.find_next_action_node(conn.get('targetId'))
                else:
                    action_node_id = conn.get('targetId')
        if action_node_id:
            for node in self.workflowspec.get('nodes'):
                if node.get('id') == action_node_id:
                    kwlass = node.get('kwlass')
        return kwlass

    def find_reverse_source_node(self, dstid):
        """ Reverse recurssive method to find the source class name """
        # import ipdb;ipdb.set_trace()
        kwlass = ''
        for conn in self.workflowspec.get('connections', []):
            if conn.get('targetId') == dstid:
                source_id = conn.get('sourceId')
                if self.is_condition_node(source_id):
                    for cn in self.workflowspec.get('connections', []):
                        if cn.get('targetId') == source_id:
                            return self.find_reverse_source_node(cn.get('sourceId'))
                else:
                    kwlass = self.find_kwlass_name(source_id)
            elif (conn.get('sourceId') == dstid and
                  self.is_action_node(conn.get('sourceId'),
                  self.workflowspec.get('nodes', []))):
                kwlass = self.find_kwlass_name(conn.get('sourceId'))
        return kwlass

    @staticmethod
    def is_action_node(source_id, nodes):
        """ Check whether the node is action node or not
            params: sourceId/targetId
            return Boolean True/False
        """
        for node in nodes:
            if node.get('id') == source_id and node.get('config', {}).get('type') == 'action':
                return True
        return False

    def is_condition_node(self, target_id):
        """ Check whether the node is condition node or not
            params: sourceId/targetId
            return Boolean True/False
        """
        for node in self.workflowspec.get('nodes', []):
            if node.get('id') == target_id and node.get('config', {}).get('type') == 'condition':
                return True
        return False
