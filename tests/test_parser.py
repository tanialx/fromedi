from fromedi.parser import Parser


def test_x12_810_0():
    parser = Parser()
    interchange = parser.fromFile('./tests/data/x12_810_0.edi')

    expected = {
        'authorization_qualifier': '01',
        'authorization': '0000000000',
        'security_qualifier': '01',
        'security': '0000000000',
        'sender_qualifier': 'ZZ',
        'sender_id': 'ABCDEFGHIJKLMNO',
        'receiver_qualifier': 'ZZ',
        'receiver_id': '123456789012345',
        'date': '101127',
        'time': '1719',
        'repetition_separator': 'U',
        'control_version': '00400',
        'control_number': '000003438',
        'acknowledgment_requested': '0',
        'usage_indicator': 'P',
        'groups': [
            {
                'functional_id_code': 'IN',
                'sender_id_code': '4405197800',
                'receiver_id_code': '999999999',
                'date': '20101205',
                'time': '1710',
                'control_number': '1320',
                'responsible_agency_code': 'X',
                'version/release/identifier_code': '004010VICS',
                'transactions': [
                    {
                        'identifier_code': '810',
                        'control_number': '1004',
                        'invoice_date': '20101204',
                        'invoice_number': '217224',
                        'order_date': '20101204',
                        'order_number': 'P792940',
                        'department_number': '099',
                        'internal_vendor_number': '99999',
                        'names': [
                            {
                                'entity_id_code': 'ST',
                                'name': '',
                                'id_code_qualifier': '92',
                                'id_code': '123'
                            },
                            {
                                'entity_id_code': 'BT',
                                'name': 'john',
                                'id_code_qualifier': '91',
                                'id_code': 'zz'
                            }
                        ],
                        'IT1s': [
                            {},
                            {},
                            {},
                            {},
                            {},
                            {},
                            {},
                            {}
                        ],
                        'total_amount': '21740'
                    }
                ]
            }
        ]
    }
    assert(interchange == expected)
