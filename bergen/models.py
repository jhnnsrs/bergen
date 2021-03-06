from bergen.types.model import ArnheimModelManager
from bergen.extenders.user import UserExtender
from bergen.types.node.inputs import Inputs, Outputs
from bergen.managers.model import ModelManager
from bergen.delayed import CREATE_NODE_MUTATION, NODE_FILTER_QUERY, NODE_QUERY
from bergen.extenders.node import NodeExtender
from bergen.managers.node import NodeManager
from bergen.schema import Node as SchemaNode
from bergen.schema import User as SchemaUser
from bergen.schema import *
try:
	# python 3.8
	from typing import ForwardRef, Type
except ImportError:
	# ForwardRef is private in python 3.6 and 3.7
	from typing import _ForwardRef as ForwardRef, Type

Node = ForwardRef('Node')

class NodeManager(ArnheimModelManager[Node]):

    def get_or_create(self, inputs: Type[Inputs] = None, outputs: Type[Outputs] = None , **kwargs) -> Node:
        
        parsed_inputs = inputs.serialized
        parsed_outputs = outputs.serialized
        
        node = CREATE_NODE_MUTATION(self.model).run(variables={
            "inputs" : parsed_inputs,
            "outputs": parsed_outputs,
            **kwargs

        })
        return node


class Node(NodeExtender, SchemaNode):
    __slots__ = ("_pod","_provisionhandler", "_postman")

    objects = NodeManager()

    class Meta:
        overwrite_default = True
        identifier = "node"
        filter = NODE_FILTER_QUERY
        get = NODE_QUERY



class User(UserExtender, SchemaUser):

    class Meta:
        overwrite_default = True
        identifier = "user"
