

def ddh(some_string):
    parts = some_string.split(',')
    num_parts = len(parts)

    match num_parts:
        case 0:
            ...
        case 1:
            ...
        case 2:
            # can be 2 date or 2 period, need to test for homogeneity
            raise Exception('[dateroll] 1 part for non-schedules, 3 part for schedule generation, or n parts for homogeneous schedules')
        case 3:
            ...
        case _:
            # Must 
            raise Exception('[dateroll] for n>3 parts, all parts mustr be Date')
