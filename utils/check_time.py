def time_or_no(time: str) -> bool:
    integ = time.split(':')
    if len(time) == 4 or len(time) == 5:
        if time[-3] == ':':
            if integ[0].isdigit() is True and integ[1].isdigit() is True:
                if int(integ[0]) < 24 and int(integ[1]) < 60:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False