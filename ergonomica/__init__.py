class ErgonomicaError(Exception):
    pass

def ergo(*argc, **argv):
    from ergonomica.ergo import ergo
    return ergo(*argc, **argv)
    
def ergo_to_string(*argc, **argv):
    from ergonomica.ergo import ergo_to_string
    return ergo_to_string(*argc, **argv)
