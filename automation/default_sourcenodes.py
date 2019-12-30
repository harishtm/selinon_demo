from .abstract_source_node import AbstractSourceNode

class ProductSourceNode(AbstractSourceNode):

    def __init__(self, *args, **kwargs):
        super(ProductSourceNode, self).__init__(
            "on product created", "Node fectes newly added product and pushes to next nodes for"\
                "further validation", "ProductSourceNode", "automation.default_sourcenodes")
    
    """
    Execute method to be implemented by the source node implementation. 
    """
    def execute(self, dataset=None):
        return NotImplementedError



    
