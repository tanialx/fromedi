from fromedi.defs import Token, SegmentType, Defs


class Parser:
    def __init__(self):
        self._out = {}

    def fromFile(self, path):
        with open(path, 'r') as reader:
            line = reader.readline()
            while line != '':  # The EOF char is an empty string
                elementArr = line.rstrip().split(Token.elementSeparator)
                isOk = self.parseElement(elementArr)
                if (isOk == False):
                    print(self.err)
                    break
                line = reader.readline()
        return self._out

    # Each EDI segment is converted to list previously    #
    # Ex: BIG*20101204*217224*20101204*P792940
    # --> [BIG, 20101204, 217224, 20101204, P792940] (elementArr)
    def parseElement(self, elementArr):
        return True
