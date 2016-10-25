
def saveSoupToFile(content, fileName):
    content = content.prettify("utf-8")

    with open(fileName, 'w') as file:
        file.write(str(content))

def saveToFile(content, fileName):
    with open(fileName, 'w') as file:
        file.write(content)

def extractAlt(tag):
    if tag.attrMap:
        return tag.attrMap['alt']
    else:
        for tag, value in tag.attrs:
            if tag == 'alt':
                return value

        return 'N.A.'