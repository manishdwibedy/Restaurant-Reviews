
def saveToFile(content, fileName):
    content = content.prettify("utf-8")

    with open(fileName, 'w') as file:
        file.write(str(content))