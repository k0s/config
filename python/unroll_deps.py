#!/usr/bin/env python 

def cycle_check(order, dependencies):
    """ensure no cyclic dependencies"""
    order_dict = dict([(j, i) for i, j in enumerate(order)])
    for package, deps in dependencies.items():
        index = order_dict[package]
        for d in deps:
            assert index > order_dict[d], "Cyclic dependencies detected"


def unroll_dependencies(dependencies):
    """unroll dependencies"""
    order = []

    # unroll the dependencies
    for package, deps in dependencies.items():
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

    cycle_check(order, dependencies)
    return order

def unroll_dependencies2(dependencies):
    """a variation"""
    order = []

    # flatten all
    packages = set(dependencies.keys())
    for deps in dependencies.values():
        packages.update(deps)

    while len(order) != len(packages):

        for package in packages.difference(order):
            if dependencies.get(package, set()).issubset(order):
                order.append(package)
                break
        else:
            raise AssertionError("Cyclic dependencies detected")

    cycle_check(order, dependencies)
    
    return order

if __name__ == '__main__':
    deps = {'packageA': set(['packageB', 'packageC', 'packageF']),
            'packageB': set(['packageC', 'packageD', 'packageE', 'packageG']),
            'packageC': set(['packageE']),
            'packageE': set(['packageF', 'packageG']),
            'packageF': set(['packageG']),
            'packageX': set(['packageA', 'packageG'])}
    unrolled = unroll_dependencies(deps)
    print unrolled

    unrolled = unroll_dependencies2(deps)
    print unrolled

    # ensure cycle check works
    deps['packageD'] = set(['packageX'])
    try:
        unroll_dependencies(deps)
        raise AssertionError("Missed a cyclic dependency!")
    except AssertionError:
        pass
        
    try:
        unroll_dependencies2(deps)
        raise AssertionError("Missed a cyclic dependency!")
    except AssertionError:
        pass
