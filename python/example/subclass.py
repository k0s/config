import string
from pprint import pprint

class Foo:
    pass

class Bar(Foo):
    pass

fleem = 1

mystuff = {i:j for i, j in globals().items()}
types = {i:type(j) for i, j in globals().items()}

mynewstuff = {i:j for i, j in mystuff.items()
              if (type(j) == type(Foo)) and issubclass(j, Foo)}

pprint(mynewstuff)
