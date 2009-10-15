def tablify(table_lines, header=True):
    table = '<table>\n'
    if header:
        tag, invtag = '<th> ', ' </th>'
    else:
        tag, invtag = '<td> ', ' </td>'
    if not hasattr(table_lines, '__iter__'):
        table_lines = ( table_lines, )
    for i in table_lines:
        table += '<tr>'
        if not hasattr(i, '__iter__'):
            i = (i,)
        for j in i:
            table += tag + str(j) + invtag
        table += '</tr>\n'
        tag = '<td> '
        invtag = ' </td>'
    table += '</table>'
    return table
