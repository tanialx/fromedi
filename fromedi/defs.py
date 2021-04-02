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

        'ISA': ['Authorization Information Qualifier', 'Authorization Information',
                'Security Information Qualifier', 'Security Information',
                'Interchange ID Sender Qualifier', 'Interchange Sender ID',
                'Interchange ID Receiver Qualifier', 'Interchange Receiver ID',
                'Date', 'Time', 'Repetition Separator',
                'Interchange Control Version Number', 'Interchange Control Number',
                'Acknowledgment Requested', 'Usage Indicator'],
        'GS': ['Functional ID Code', 'Sender\'s ID Code', 'Receiver\'s ID Code',
               'Date', 'Time', 'Group Control Number', 'Responsible Agency Code',
               'Version/Release/Identifier Code'],
        'ST': ['Transaction Set Identifier Code', 'Transaction Set Control Number'],
        'BIG': ['Invoice Date', 'Invoice Number', 'Order Date', 'Purchase Order Number', 'Release Number', 'Transaction Type'],
        'SE': ['# Segments', 'Transaction Control Number'],
        'GE': ['# Transaction Sets', 'Group Control Number'],
        'IEA': ['# Groups', 'Interchange Control Number']
    }

    rule = {

        # Layout of EDI envenlope
        # - segtype: for handling special segments such as envelope level or Loop
        # - subsegs: child segments

        'ISA': {
            'segtype': SegmentType.REGULAR,
            'subsegs': {
                'GS': {
                    'segtype': SegmentType.REGULAR,
                    'subsegs': {
                        'ST': {
                            'segtype': SegmentType.REGULAR,
                            'subsegs': {
                                # TODO: more segment defs
                                'SE': {
                                    'segtype': SegmentType.CLOSING # End of ST segment
                                }
                            }
                        },
                        'GE': {
                            'segtype': SegmentType.CLOSING # End of GS segment
                        }
                    }
                },
                'IEA': {
                    'segtype': SegmentType.CLOSING # End of ISA segment
                }
            }
        }
    }
