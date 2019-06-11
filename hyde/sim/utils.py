"""Hyde: Utility functions

   _______     ___
+ 6 @ |||| # P ||| +

"""

def convertToStrSet(byteSet):
    r"""Converts byteSet into a set of strings
    """
    strSet = set()
    for e in byteSet:
        strSet.add(e.decode('utf-8'))
    return strSet

