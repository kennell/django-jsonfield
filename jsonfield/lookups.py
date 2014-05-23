from django.db.models import Lookup

class HasKey(Lookup):
    """
    If our connection is able to handle proper json (and our field is indeed
    an actual json object), then we can use the json_object_keys function,
    or equivalent.
    
    Otherwise, we'll need to be a bit tricky, and look for a string of the format:
    
    "keyname":
    
    (including the quotes).
    
    We probably won't get too many false positives. I hope.
    """
    lookup_name = 'has_key'
    
    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        
        return 'count(*) > 0 FROM json_object_keys(%s) WHERE json_object_keys = %s' % (
            rhs, lhs
        ), params


