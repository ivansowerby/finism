def path(d: dict, path: list, filter: dict = None):
    for p in path:
        if p == '[]':
            continue
        if filter != None:
            for k, v in filter.items():
                if p[1:-1] == k and p[0] == '[' and p[-1] == ']':
                    p = v
        if type(d) == list:
            r = [
                i[p] for i in d if p in i.keys() 
            ]
            if len(r) == 1: return r[0]
            return r
        else:
            d = d[p]
    return d