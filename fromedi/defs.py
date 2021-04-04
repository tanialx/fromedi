from enum import Enum


class Token:
    elementSeparator = '*'
    compositeElementSeparator = ':'
    segmentSeparator = '~'


class SegmentType(Enum):

    # REGULAR:  Requires no special processing (all segments except LOOP and CLOSING)
    # LOOP:     Repeated segments that may included child segments
    # CLOSING:  Signal end of current segment (no more child),
    #           ex: SE signals end of transaction data (which starts with ST)
    # KV_PAIR:  Segment contains two elements, but one is the value of the other
    #           ex: REF*BM*00000000 should be translate directly as 'bill_of_lading': '00000000'
    #               instead of {'ref_id_qualifier': 'BM, 'ref_id': '00000000'}

    REGULAR = 1
    LOOP = 2
    CLOSING = 3
    KV_PAIR = 4


class Defs:

    segmentDef = {

        # Name for segment's elements corresponding to position in EDI segment
        # Ex.
        # Transaction set segment SE*18*1004 holds values for
        # (# Segments: 18, Transaction Set Control Number: 1004)
        # and is represented as:
        # SE: ['# Segments', 'Transaction Control Number']

        'ISA': ['authorization_qualifier', 'authorization', 'security_qualifier', 'security',
                'sender_qualifier', 'sender_id', 'receiver_qualifier', 'receiver_id',
                'date', 'time', 'repetition_separator', 'control_version', 'control_number',
                'acknowledgment_requested', 'usage_indicator'],
        'GS': ['functional_id_code', 'sender_id_code', 'receiver_id_code',
               'date', 'time', 'control_number', 'responsible_agency_code',
               'version/release/identifier_code'],
        'ST': ['identifier_code', 'control_number'],
        'BIG': ['invoice_date', 'invoice_number', 'order_date', 'order_number', 'release_number', 'transaction_type'],
        'N1': ['entity_id_code', 'name', 'id_code_qualifier', 'id_code'],
        'SE': ['number_of_segments', 'transaction_control_number'],
        'GE': ['number_of_transaction_sets', 'group_control_number'],
        'IEA': ['number_of_groups', 'interchange_control_number']
    }

    loopName = {
        'N1': 'names',
        'GS': 'groups',
        'ST': 'transactions'
    }

    tranx = {
        # ASC X12 810: Invoice
        '810': {
            'subsegs': {
                'BIG': {},
                'REF': {
                    'segtype': SegmentType.KV_PAIR,
                    'key_idx': 1
                },
                'N1': {
                    'segtype': SegmentType.LOOP,
                    'subsegs': {
                        'N1': {},
                        'N2': {},
                        'N3': {},
                        'N4': {}
                    }
                },
                'ITD': {},
                'IT1': {
                    'segtype': SegmentType.LOOP,
                    'subsegs': {
                        'IT1': {}
                    }
                },
                'TDS': {},
                'CAD': {},
                'CTT': {}
            }
        }
    }

    rule = {

        # Layout of EDI envenlope
        # - segtype: for handling special segments such as envelope level or Loop
        #            If segment type is not set for a segment, it'll be parsed as REGULAR
        # - subsegs: child segments
        # - subsegs_link: link to external dict using
        #                 (key = element value at index 'mapped_by_index')
        #                 of the current segment as in raw EDI (including the segment identifier)
        #                 Ex: 'REF' has index 0 in REF*DP*099
        # Treat repeatable envolope segments (GS, ST) as LOOP for now

        'ISA': {
            'subsegs': {
                'GS': {
                    'segtype': SegmentType.LOOP,
                    'subsegs': {
                        'ST': {
                            'segtype': SegmentType.LOOP,
                            'subsegs_link': {
                                # Example: ST*810*1004
                                # 'mapped_by_index': 1 --> key value: 810
                                # Subsegs of this segment are retrieve from
                                # tranx['810']
                                'mapped_by_index': 1,
                                'mapped_with': tranx
                            },
                            'subsegs': {
                                # TODO: more segment defs
                                'SE': {
                                    'segtype': SegmentType.CLOSING  # End of ST segment
                                }
                            }
                        },
                        'GE': {
                            'segtype': SegmentType.CLOSING  # End of GS segment
                        }
                    }
                },
                'IEA': {
                    'segtype': SegmentType.CLOSING  # End of ISA segment
                }
            }
        }
    }
