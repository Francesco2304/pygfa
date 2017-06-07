from parser import line, error, field_validator as fv
import re

def is_segmentv1 (string):
    """Checks wether a given string belongs to the first GFA version.
    @param string A string that is supposed to represent an S line.
    @exceptions Exception Launch a generic exception if the given parameter is
    not a string."""
    if not isinstance (string, str):
        raise Exception ("The given parameter is not a string.")
    try:
        if re.fullmatch (fv.DATASTRING_VALIDATION_REGEXP['seq'], \
                       re.split("\t", string)[2]):
                       return True
    except: pass
    return False

def is_segmentv2 (string):
    """Checks wether a given string belongs to the second GFA version.
    @param string A string that is supposed to represent an S line.
    @exceptions Exception Launch a generic exception if the given parameter is
    not a string."""
    if not isinstance (string, str):
        raise Exception ("The given parameter is not a string.")
    try:
        if re.fullmatch (fv.DATASTRING_VALIDATION_REGEXP['pos'], \
                       re.split("\t", string)[2]):
                       return True
    except: pass
    return False

class SegmentV1 (line.Line):

    def __init__ (self):
        super().__init__ ('S')
    
    REQUIRED_FIELDS = { \
    'name' : 'lbl', \
    'seq' : 'seq' \
    }

    PREDEFINED_OPTFIELDS = { \
    'LN' : 'i', \
    'RC' : 'i', \
    'FC' : 'i', \
    'KC' : 'i', \
    'SH' : 'H', \
    'UR' : 'Z' \
    }

    @classmethod
    def from_string (cls, string):
        """Extract the segment fields from the string.
        The string can contain the S character at the begin or can only contains the fields
        of the segment directly."""
        fields = re.split ('\t', string)
        sfields = []
        if fields[0] == 'S':
            fields = fields[1:]
            
        segment = SegmentV1 ()

        # the required fields are in the first two columns
        name_f = fv.validate (fields[0], cls.REQUIRED_FIELDS['name'])
        sfields.append (line.Field ('name', name_f))

        seq_f = fv.validate (fields[1], cls.REQUIRED_FIELDS['seq'])
        sfields.append (line.Field ('seq', seq_f))

        for field in fields[2:]:
            sfields.append (line.OptField.from_string (field))
            
        for field in sfields:
            segment.add_field (field)

        return segment


class SegmentV2 (line.Line):

    def __init__ (self):
        super().__init__ ('S')
    
    REQUIRED_FIELDS = { \
    'name' : 'lbl', \
    'seq_len' : 'pos', \
    'seq' : 'seq' \
    }

    @classmethod
    def from_string (cls, string):
        """Extract the segment fields from the string.
        The string can contain the S character at the begin or can only contains the fields
        of the segment directly."""
        fields = re.split ('\t', string)
        sfields = []
        if fields[0] == 'S':
            fields = fields[1:]
            
        segment = SegmentV2 ()

        # the required fields are in the first two columns
        name_f = fv.validate (fields[0], cls.REQUIRED_FIELDS['name'])
        sfields.append (line.Field ('name', name_f))

        seq_f = fv.validate (fields[1], cls.REQUIRED_FIELDS['seq'])
        sfields.append (line.Field ('seq', seq_f))

        seq_f = fv.validate (fields[2], cls.REQUIRED_FIELDS['seq_len'])
        sfields.append (line.Field ('seq_len', seq_f))
        
        for field in fields[3:]:
            sfields.append (line.OptField.from_string (field))
            
        for field in sfields:
            segment.add_field (field)

        return segment


