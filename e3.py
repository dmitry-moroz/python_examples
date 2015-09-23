d = {'a': [1, 2, 3],
     'b': {'c': 1,
           'd': {'e': 'f', 'f': [5, 6, 7]},
           'f': [7, [8, [9, 10]]],
           'i': 'hello'
          }
    }

def func1(dct, lst=[]):
     for v in dct.values():
         if isinstance(v, dict):
             func1(v, lst)
         elif isinstance(v, (list, tuple)):
             func2(v, lst)
         else:
             lst.append(v)
     return lst

def func2(lst1, lst2):
     for i in lst1:
         if isinstance(i, (list, tuple)):
             func2(i, lst2)
         else:
             lst2.append(i)

def func3(dct):
    for v in dct.itervalues():
         if isinstance(v, dict):
             for x in func3(v):
                 yield x
         else:
             yield v

def func4(lst):
    for v in lst:
         if isinstance(v, list):
             for x in func4(v):
                 yield x
         else:
             yield v

print func1(d)
print list(func4(func3(d)))
