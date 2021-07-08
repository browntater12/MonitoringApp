

def orderVersion(versions):
    vers = []
    for x in versions:
        x = x.replace('.', '')
        if len(x) == 2:
            x = int(x) * 10
        elif len(x) == 1:
            x = int(x) * 100
        vers += [str(x)]
    vers.sort(reverse=True)
    orderedList = []
    for y in vers:
        string = ""
        for z in range(len(y)):
            if z == 2:
                string += y[z]
            else:
                string += y[z]
                string += '.'
        string = [string]
        orderedList += string
        
    return orderedList
        
