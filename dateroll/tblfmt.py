def pretty_table(ld, col_widths=None):
    if len(ld)==0:
        return ""
    headers = list(ld[0].keys())
    data = [headers] + [list(d.values()) for d in ld]

    if col_widths is None:
        col_widths = [max(max([len(str(d[h])) for d in ld]),len(h))+2 for h in headers]

    x = ""
    
    # Print the top border
    x += '┌'
    for i, width in enumerate(col_widths):
        end = ('┬' if i < len(col_widths)-1 else '┐\n')
        x+= '─' * (width + 2) + end
    
    # Print the header row
    for i, width in enumerate(col_widths):
        end = ('  ' if i < len(col_widths)-1 else '  │\n')
        x += '│' + f'{data[0][i]:^{width}}'+ end

    # Print the middle border
    x += '├'
    
    for i, width in enumerate(col_widths):
        end = ('┼' if i < len(col_widths)-1 else  '┤\n')
        x += '─' * (width + 2) + end

    # Print the table data
    for row in data[1:]:
        for i, width in enumerate(col_widths):
            end = ('  ' if i < len(col_widths)-1 else '  │\n' )
            x += '│' + f'{row[i]:<{width}}' + end
    
    # Print the bottom border
    x += '└'
    for i, width in enumerate(col_widths):
        end = ('┴' if i < len(col_widths)-1 else '┘\n')
        x += '─' * (width + 2)+end

    return x

if __name__ == '__main__':  # pragma:no cover
    from dateroll import cals
    data = cals._calsdata
    s = pretty_table(data)
    print(s)
