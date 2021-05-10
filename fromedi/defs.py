from enum import Enum


class Token:
    elementSeparator = '*'
    compositeElementSeparator = ':'
    segmentSeparator = '~'

# Define types of segments in an EDI
# Change to this class should be reflected in func 'segmentType' of parser.py
class SegmentType(Enum):

    # REGULAR:  Requires no special processing (all segments except LOOP and CLOSING)
    # LOOP:     Repeated segments that may included child segments
    # KV_PAIR:  Segment contains two elements, but one is the value of the other
    #           ex: REF*BM*00000000 should be translate directly as 'bill_of_lading': '00000000'
    #               instead of {'ref_id_qualifier': 'BM, 'ref_id': '00000000'}
    # ENVELOPE_OPENING:  
    #           Repeated segments that may included child segments. This type is similar to LOOP
    #           except that the the sub-segments are wrapped with opening and closing segments;
    #           whereas in LOOP, the first segment of LOOP we encounter is the Loop's sub-segment
    #           ex: - WRAP: ST (BIG REF) SE
    #               - LOOP: (N1 N2 N3 N4)
    # ENVELOPE_CLOSING: 
    #           Signal end of current segment (no more child) which previously starts with ENVELOPE_OPENING,
    #           ex: SE signals end of transaction data (which starts with ST)

    REGULAR = 1
    LOOP = 2
    KV_PAIR = 3
    ENVELOPE_OPENING = 4
    ENVELOPE_CLOSING = 5


class Defs:

    commonSegmentDef = {

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
        'N1': ['entity_id_code', 'name', 'id_code_qualifier', 'id_code'],
        'TDS': ['total_amount'],
        'SE': ['number_of_segments', 'transaction_control_number'],
        'GE': ['number_of_transaction_sets', 'group_control_number'],
        'IEA': ['number_of_groups', 'interchange_control_number']
    }

    loop = {
        'GS': {
            'loop_name': 'groups'
        },
        'ST': {
            'loop_name': 'transactions'
        },
        'N1': {
            'loop_name': 'names',
            'subsegs': [
                {
                    "segname": "N1"
                },
                {
                    "segname": "N2"
                },
                {
                    "segname": "N3"
                },
                {
                    "segname": "N4"
                }
            ]
        }
    }

    rule = [{

        # Layout of EDI envenlope
        # - segtype: for handling special segments such as envelope level or Loop
        #            If segment type is not set for a segment, it'll be parsed as REGULAR
        # - subsegs: child segments
        # - subsegs_link: link to external dict/file using
        #                 (key = element value at index 'mapped_by_index')
        #                 of the current segment as in raw EDI (including the segment identifier)
        #                 Ex: 'REF' has index 0 in REF*DP*099

        'segname': 'ISA',
        'subsegs': [{
            'segname': 'GS',
            'segtype': SegmentType.ENVELOPE_OPENING,
            'subsegs': [{
                    'segname': 'ST',
                    'segtype': SegmentType.ENVELOPE_OPENING,
                    'subsegs_link': {

                        # Example: ST*810*1004, with 'mapped_by_index': 1 --> key value: 810
                        # Subsegs of this segment are retrieve from file 'struct/ST/810.json'
                        'mapped_by_index': 1,

                        # if 'mapped_with' = 'struct', file path is constructed as 
                        # 'fromedi/struct/<this_segment_name>/<value_at_mapped_by_index>.json'
                        # (it's also possible to map with a dict object; in that case, the mapping would be to
                        # obj[<value_at_mapped_by_index>])
                        'mapped_with': 'file:struct'
                    },
                    'subsegs': [
                        {
                            'segname': 'SE',
                            'segtype': SegmentType.ENVELOPE_CLOSING,
                        }
                    ]
                    }, {
                'segname': 'GE',
                'segtype': SegmentType.ENVELOPE_CLOSING,
            }
            ]
        }, {
            'segname': 'IEA',
            'segtype': SegmentType.ENVELOPE_CLOSING,
        }]
    }]
