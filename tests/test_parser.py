from fromedi.parser import Parser

def test_Parser():
    parser = Parser()
    interchange = parser.fromFile('./tests/data/x12_810_0.edi')
    assert(interchange['authorization_qualifier'] == '01')
    assert(interchange['authorization'] == '0000000000')
    assert(interchange['security_qualifier'] == '01')
    assert(interchange['security'] == '0000000000')
    assert(interchange['sender_qualifier'] == 'ZZ')
    assert(interchange['sender_id'] == 'ABCDEFGHIJKLMNO')
    assert(interchange['receiver_qualifier'] == 'ZZ')
    assert(interchange['receiver_id'] == '123456789012345')
    assert(interchange['date'] == '101127')
    assert(interchange['time'] == '1719')
    assert(interchange['repetition_separator'] == 'U')
    assert(interchange['control_version'] == '00400')
    assert(interchange['control_number'] == '000003438')
    assert(interchange['acknowledgment_requested'] == '0')
    assert(interchange['usage_indicator'] == 'P')

    group0 = interchange['GSs'][0]    
    assert(group0['functional_id_code'] == 'IN')
    assert(group0['sender_id_code'] == '4405197800')
    assert(group0['receiver_id_code'] == '999999999')
    assert(group0['date'] == '20101205')
    assert(group0['time'] == '1710')
    assert(group0['control_number'] == '1320')
    assert(group0['responsible_agency_code'] == 'X')
    assert(group0['version/release/identifier_code'] == '004010VICS')

    tranx0 = group0['STs'][0]
    assert(tranx0['identifier_code'] == '810')
    assert(tranx0['control_number'] == '1004')

