#!/usr/bin/env python 

def unroll_dependencies(dependencies):
    """unroll dependencies"""
    order = []

    # unroll the dependencies
    for package, deps in dependencies.items():
        print package, order
        try:
            index = order.index(package)
        except ValueError:
            order.append(package)
            index = len(order) - 1
        for dep in deps:
            try:
                dep_index = order.index(dep)
                if dep_index > index:
                    order.insert(dep_index+1, package)
                    order.pop(index)
                    index = dep_index
            except ValueError:
                order.insert(index, dep)
            except AssertionError:
                print reverse_deps
                raise

    # ensure no cyclic dependencies
    # XXX should do this first
    order_dict = dict([(j, i) for i, j in enumerate(order)])
    for package, deps in dependencies.items():
        index = order_dict[package]
        for d in deps:
            assert index > order_dict[d], "Cyclic dependencies detected"

    return order

if __name__ == '__main__':
    deps = {'packageA': set(['packageB', 'packageC', 'packageF']),
            'packageB': set(['packageC', 'packageD', 'packageE', 'packageG']),
            'packageC': set(['packageE']),
            'packageE': set(['packageF', 'packageG']),
            'packageF': set(['packageG']),
            'packageX': set()}
    unrolled = unroll_dependencies(deps)
    print unrolled
