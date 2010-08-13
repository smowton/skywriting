# Copyright (c) 2010 Derek Murray <derek.murray@cl.cam.ac.uk>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
import uuid

'''
Created on 20 Apr 2010

@author: dgm36
'''

class SWRealReference:
    
    def as_tuple(self):
        pass

class SWErrorReference(SWRealReference):
    
    def __init__(self, reason, details):
        self.reason = reason
        self.details = details

    def as_tuple(self):
        return ('err', self.reason, self.details)

class SWNullReference(SWRealReference):
    
    def __init__(self):
        pass
    
    def as_tuple(self):
        return ('null',)
    
class SWFutureReference(SWRealReference):
    pass

class SWProvenance:
    
    def as_tuple(self):
        pass
    
class SWNoProvenance(SWProvenance):
    
    def as_tuple(self):
        return ('na', )
    
class SWTaskOutputProvenance(SWProvenance):
    
    def __init__(self, task_id, index):
        self.task_id = task_id
        self.index = index
    
    def as_tuple(self):
        return ('out', str(self.task_id), self.index)

class SWSpawnedTaskProvenance(SWProvenance):
    
    def __init__(self, task_id, spawn_list_index):
        self.task_id = task_id
        self.index = spawn_list_index

    def as_tuple(self):
        return ('spawn', str(self.task_id), self.index)

class SWTaskContinuationProvenance(SWProvenance):
    
    def __init__(self, task_id):
        self.task_id = task_id
        
    def as_tuple(self):
        return ('cont', str(self.task_id))

class SW2_FutureReference(SWFutureReference):
    """
    Used as a reference to a task that hasn't completed yet. The identifier is in a
    system-global namespace, and may be passed to other tasks or returned from
    tasks.
    """
        
    def __init__(self, id, provenance=SWNoProvenance()):
        self.id = id
        self.provenance = provenance
    
    def as_tuple(self):
        return ('f2', str(self.id), self.provenance.as_tuple())

    def __repr__(self):
        return 'SW2_FutureReference(%s, %s)' % (repr(self.id), repr(self.provenance))
                
class SW2_ConcreteReference(SWRealReference):
        
    def __init__(self, id, provenance, location_hints):
        self.id = id
        self.provenance = provenance
        self.location_hints = location_hints
        
    def as_tuple(self):
        return('c2', str(self.id), self.provenance.as_tuple(), self.location_hints)
        
    def __repr__(self):
        return 'SW2_ConcreteReference(%s, %s, %s)' % (repr(self.id), repr(self.provenance), repr(self.location_hints))
        
class SWURLReference(SWRealReference):
    """
    A reference to one or more URLs representing the same data.
    """
    
    def __init__(self, urls, size_hint=None):
        self.urls = urls
        self.size_hint = size_hint
        
    def as_tuple(self):
        return ('urls', self.urls, self.size_hint)
    
    def __repr__(self):
        return 'SWURLReference(%s, %s)' % (repr(self.urls), repr(self.size_hint))

class SWDataValue(SWRealReference):
    """
    Used to store data that has been dereferenced and loaded into the environment.
    """
    
    def __init__(self, value):
        self.value = value
        
    def as_tuple(self):
        return ('val', self.value)
    
    def __repr__(self):
        return 'SWDataValue(%s)' % (repr(self.value), )

def build_provenance_from_tuple(provenance_tuple):
    p_type = provenance_tuple[0]
    if p_type == 'na':
        return SWNoProvenance()
    elif p_type == 'out':
        return SWTaskOutputProvenance(uuid.UUID(hex=provenance_tuple[1]), provenance_tuple[2])
    elif p_type == 'spawn':
        return SWSpawnedTaskProvenance(uuid.UUID(hex=provenance_tuple[1]), provenance_tuple[2])
    elif p_type == 'cont':
        return SWTaskContinuationProvenance(uuid.UUID(hex=provenance_tuple[1]))
    else:
        raise KeyError(p_type)

def build_reference_from_tuple(reference_tuple):
    ref_type = reference_tuple[0]
    if ref_type == 'urls':
        return SWURLReference(reference_tuple[1], reference_tuple[2])
    elif ref_type == 'val':
        return SWDataValue(reference_tuple[1])
    elif ref_type == 'err':
        return SWErrorReference(reference_tuple[1], reference_tuple[2])
    elif ref_type == 'null':
        return SWNullReference()
    elif ref_type == 'f2':
        return SW2_FutureReference(uuid.UUID(hex=reference_tuple[1]), build_provenance_from_tuple(reference_tuple[2]))
    elif ref_type == 'c2':
        return SW2_ConcreteReference(uuid.UUID(hex=reference_tuple[1]), build_provenance_from_tuple(reference_tuple[2]), reference_tuple[3])
    else:
        raise KeyError(ref_type)