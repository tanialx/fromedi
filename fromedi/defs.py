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

    REGULAR = 1
    LOOP = 2
    CLOSING = 3


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
        'BIG': ['invoice_date', 'invoice_number', 'order_date', 'purchase_order_number', 'release_number', 'transaction_type'],
        'SE': ['number_of_segments', 'transaction_control_number'],
        'GE': ['number_of_transaction_sets', 'group_control_number'],
        'IEA': ['number_of_groups', 'interchange_control_number']
    }

    rule = {

        # Layout of EDI envenlope
        # - segtype: for handling special segments such as envelope level or Loop
        # - subsegs: child segments
        # Treat repeatable envolope segments (GS, ST) as LOOP for now

        'ISA': {
            'segtype': SegmentType.REGULAR,
            'subsegs': {
                'GS': {
                    'segtype': SegmentType.LOOP,
                    'subsegs': {
                        'ST': {
                            'segtype': SegmentType.LOOP,
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
