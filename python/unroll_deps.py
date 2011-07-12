#!/usr/bin/env python 

def unroll_dependencies(dependencies):
    """unroll dependencies"""
    order = []
    for package, deps in dependencies.items():
        try:
            index = order.index(package)
        except ValueError:
            order.append(package)
            index = len(order) - 1
        for dep in deps:
            try:
                dep_index = order.index(dep)
                assert dep_index < index, "Cyclic dependencies detected"
            except ValueError:
                order.insert(index, dep)
    return order

if __name__ == '__main__':
    deps = {'packageA': set(['packageB', 'packageC']),
            'packageB': set(['packageC', 'packageD']),
            'packageC': set()}
    unrolled = unroll_dependencies(deps)
    print unrolled
