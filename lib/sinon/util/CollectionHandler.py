def partialTupleInTupleList(main, sub):
    """
    >>> main = [('a', 'b', 'c'), ('c', 'd')] 
    >>> partialTupleInTupleList(main, ('a',))
    True
    >>> partialTupleInTupleList(main, ('b','d'))
    False
    >>> partialTupleInTupleList(main, ('a','b','c'))
    True
    >>> partialTupleInTupleList(main, ('z',))
    False
    >>> partialTupleInTupleList(main, ((),))
    False
    """
    return True if [item for item in main if set(sub)&set(item)==set(sub)] else False

def partialDictInDictList(main, sub):
    """
    # Note: The last one is special case
    >>> main = [{'c': 'c', 'a': 'a', 'b': 'b'}, {'c': 'c', 'd': 'd'}]
    >>> partialDictInDictList(main, {'c': 'c'})
    True
    >>> partialDictInDictList(main, {'b': 'b', 'd': 'd'})
    False
    >>> partialDictInDictList(main, {'c': 'c', 'a': 'a', 'b': 'b'})
    True
    >>> partialDictInDictList(main, {'z': 'z'})
    False
    >>> partialDictInDictList(main, {})
    True
    """
    return True if [item for item in main if set(sub.items()).issubset(set(item.items()))] else False

def itemInList(main, sub):
    return True if sub in main else False

def tupleInTupleList(main, sub):
    """
    >>> main = [('a', 'b', 'c'), ('c', 'd')] 
    >>> tupleInTupleList(main, ('a',))
    False
    >>> tupleInTupleList(main, ('b','d'))
    False
    >>> tupleInTupleList(main, ('a','b','c'))
    True
    >>> tupleInTupleList(main, ('c','d'))
    True
    >>> tupleInTupleList(main, ('z',))
    False
    >>> tupleInTupleList(main, ((),))
    False
    """
    return itemInList(main, sub)

def dictInDictList(main, sub):
    """
    >>> main = [{'c': 'c', 'a': 'a', 'b': 'b'}, {'c': 'c', 'd': 'd'}]
    >>> dictInDictList(main, {'c': 'c'})
    False
    >>> dictInDictList(main, {'b': 'b', 'd': 'd'})
    False
    >>> dictInDictList(main, {'c': 'c', 'a': 'a', 'b': 'b'})
    True
    >>> dictInDictList(main, {'c': 'c', 'd': 'd'})
    True
    >>> dictInDictList(main, {'z': 'z'})
    False
    >>> dictInDictList(main, {})
    False
    """
    return itemInList(main, sub)

def tupleInTupleListAlways(main, sub):
    """
    >>> main = [('a', 'b', 'c'), ('c', 'd')] 
    >>> tupleInTupleListAlways(main, ('a' ,'b', 'c'))
    False
    >>> tupleInTupleListAlways(main, ('c', 'd'))
    False
    >>> tupleInTupleListAlways(main, ('a', 'c'))
    False
    >>> tupleInTupleListAlways(main, ('a'))
    False
    >>> tupleInTupleListAlways(main, ((),))
    False
    >>> main = [('a', 'b', 'c'), ('a', 'b', 'c')]
    >>> tupleInTupleListAlways(main, ('a' ,'b', 'c'))
    True
    >>> main = [('a', 'b', 'c')]
    >>> tupleInTupleListAlways(main, ('a' ,'b', 'c'))
    True
    """
    return True if sub in set(main) and len(set(main)) == 1 else False

def dictInDictListAlways(main, sub):
    """
    >>> main = [{'c': 'c', 'a': 'a', 'b': 'b'}, {'c': 'c', 'd': 'd'}]
    >>> dictInDictListAlways(main, {'a': 'a', 'b': 'b', 'c': 'c'})
    False
    >>> dictInDictListAlways(main, {'c': 'c', 'd': 'd'})
    False
    >>> dictInDictListAlways(main, {'a': 'a', 'c': 'c'})
    False
    >>> dictInDictListAlways(main, {'a': 'a'})
    False
    >>> dictInDictListAlways(main, {})
    False
    >>> main = [{'c': 'c', 'a': 'a', 'b': 'b'}, {'c': 'c', 'a': 'a', 'b': 'b'}]
    >>> dictInDictListAlways(main, {'c': 'c', 'a': 'a', 'b': 'b'})
    True
    >>> main = [{'c': 'c', 'a': 'a', 'b': 'b'}]
    >>> dictInDictListAlways(main, {'c': 'c', 'a': 'a', 'b': 'b'})
    True
    """
    for item in main:
        if sub != item:
            return False
    return True

def partialTupleInTupleListAlways(main, sub):
    """
    >>> main = [('a', 'b', 'c'), ('c', 'd')] 
    >>> partialTupleInTupleListAlways(main, ('a' ,'b', 'c'))
    False
    >>> partialTupleInTupleListAlways(main, ('c', 'd'))
    False
    >>> partialTupleInTupleListAlways(main, ('a', 'c'))
    False
    >>> partialTupleInTupleListAlways(main, ('a'))
    False
    >>> partialTupleInTupleListAlways(main, ((),))
    False
    >>> main = [('a', 'b', 'c'), ('a', 'b', 'c')]
    >>> partialTupleInTupleListAlways(main, ('a', 'b'))
    True
    >>> partialTupleInTupleListAlways(main, ('a', 'c'))
    True
    >>> partialTupleInTupleListAlways(main, ('b' ,'c'))
    True
    >>> partialTupleInTupleListAlways(main, ('a'))
    True
    """
    for item in main:
        if not set(sub)&set(item)==set(sub):
            return False
    return True 

def partialDictInDictListAlways(main, sub):
    """
    >>> main = [{'c': 'c', 'a': 'a', 'b': 'b'}, {'c': 'c', 'd': 'd'}]
    >>> partialDictInDictListAlways(main, {'a': 'a', 'b': 'b', 'c': 'c'})
    False
    >>> partialDictInDictListAlways(main, {'c': 'c', 'd': 'd'})
    False
    >>> partialDictInDictListAlways(main, {'a': 'a', 'c': 'c'})
    False
    >>> partialDictInDictListAlways(main, {'a': 'a'})
    False
    >>> partialDictInDictListAlways(main, {})
    False
    >>> main = [{'c': 'c', 'a': 'a', 'b': 'b'}, {'c': 'c', 'a': 'a', 'b': 'b'}]
    >>> partialDictInDictListAlways(main, {'c': 'c', 'a': 'a', 'b': 'b'})
    True
    >>> partialDictInDictListAlways(main, {'c': 'c', 'a': 'a'})
    True
    >>> partialDictInDictListAlways(main, {'c': 'c'})
    True
    """
    if not sub:
        return False
    for item in main:
        if not set(sub.items()).issubset(set(item.items())):
            return False
    return True
