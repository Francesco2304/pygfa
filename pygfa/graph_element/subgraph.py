from parser.lines import path, group
from parser import line
import copy

class InvalidSubgraphError (Exception): pass

class Subgraph:

    def __init__ (self, graph_id, elements, opt_fields={}):
        if not isinstance (graph_id, str):
            raise InvalidSubgraphError ("A  has always an id of type string, " + \
                                 "given {0} of type {1}".format (node_id, type (node_id)))

        if not isinstance (elements, list):
            raise InvalidSubgraphError ("A list of elements is required.")

        self._sub_id = graph_id
        self._elements = elements
        self._opt_fields = {}
        for key, field in opt_fields.items ():
            if line.is_field (field):
                self._opt_fields[key] = copy.deepcopy (field)


    @property
    def sub_id (self):
        return self._sub_id

    @property
    def elements (self):
        return self._elements

    @property
    def opt_fields (self):
        return self._opt_fields

    @classmethod
    def from_line (cls, line):

        if not line.is_valid ():
            raise InvalidSubgraphError ("The line to be added must have all the required fields. Line type: '{0}'".format (line.type))

        try:
            fields = copy.deepcopy (line.fields)

            if line.type == 'P':
                fields.pop ('path_name')
                fields.pop ('seqs_names')

                return Subgraph ( \
                                line.fields['path_name'].value, \
                                line.fields['seqs_names'].value, \
                                fields)

            if line.type == 'O':
                fields.pop ('oid')
                fields.pop ('references')

                return Subgraph ( \
                                line.fields['oid'].value, \
                                line.fields['references'].value, \
                                fields)

            if line.type == 'U':
                fields.pop ('uid')
                fields.pop ('references')

                return Subgraph ( \
                                line.fields['uid'].value, \
                                line.fields['references'].value, \
                                fields)
                            
                
        except Exception as e:
            raise e
