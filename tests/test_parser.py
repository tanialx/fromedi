from fromedi.parser import Parser

def test_Parser():
    parser = Parser()
    interchange = parser.fromFile('./tests/data/x12_810_0.edi')
    assert(interchange['Authorization Qualifier'] == '01')
    assert(interchange['Authorization'] == '0000000000')
    assert(interchange['Security Qualifier'] == '01')
    assert(interchange['Security'] == '0000000000')
    assert(interchange['Sender Qualifier'] == 'ZZ')
    assert(interchange['Sender ID'] == 'ABCDEFGHIJKLMNO')
    assert(interchange['Receiver Qualifier'] == 'ZZ')
    assert(interchange['Receiver ID'] == '123456789012345')
    assert(interchange['Date'] == '101127')
    assert(interchange['Time'] == '1719')
    assert(interchange['Repetition Separator'] == 'U')
    assert(interchange['Control Version Number'] == '00400')
    assert(interchange['Control Number'] == '000003438')
    assert(interchange['Acknowledgment Requested'] == '0')
    assert(interchange['Usage Indicator'] == 'P')

    group0 = interchange['GSs'][0]    
    assert(group0['Functional ID Code'] == 'IN')
    assert(group0['Sender\'s ID Code'] == '4405197800')
    assert(group0['Receiver\'s ID Code'] == '999999999')
    assert(group0['Date'] == '20101205')
    assert(group0['Time'] == '1710')
    assert(group0['Control Number'] == '1320')
    assert(group0['Responsible Agency Code'] == 'X')
    assert(group0['Version/Release/Identifier Code'] == '004010VICS')

    tranx0 = group0['STs'][0]
    assert(tranx0['Identifier Code'] == '810')
    assert(tranx0['Control Number'] == '1004')

