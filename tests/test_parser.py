from fromedi.parser import Parser

def test_Parser():
    parser = Parser()
    _inv = parser.fromFile('./tests/data/x12_810_0.edi')
    assert(_inv != None)
