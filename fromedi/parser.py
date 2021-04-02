from fromedi.defs import Token, SegmentType, Defs


class Parser:
    def __init__(self):
        self._out = {} # Final result after parsing

        # Keep track of the outer rules when we process child elements that
        # contains nested rules.We will need to comeback to previous rule later on
        # to finialize the info
        #
        # Example:
        # From rule ISA, we switch to GS then switch to ST, and process some regular segments
        # such as BIG and REF <-- These do not contain nested segment so we do not need to track them
        # --> Stack [ISA, GS, ST]
        # Then we switch to N1-Loop rule which contains nested segments N1, N2, N3, N4
        # --> Stack [ISA, GS, ST, N1Loop].
        # After we've done processing with N1Loop, we remove it from stacked
        # --> [ISA, GS, ST] and continue with remaining elements of ST rule)

        self.rule_stack = [{'subsegs': Defs.rule}]

    def currentRule(self):
        return self.rule_stack[len(self.rule_stack) - 1]

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

    # Each EDI segment is converted to list previously in 'fromFile' func
    # Ex: BIG*20101204*217224*20101204*P792940
    # --> [BIG, 20101204, 217224, 20101204, P792940] (elementArr)
    def parseElement(self, elementArr):

        # Retrieve segment name as first element in list
        seg_name = elementArr[0].upper()

        # Retrieve current rule's child elements from stack
        current_rule = self.currentRule()['subsegs']

        # Case 1: seg_name is defined in rule, that means end-of-rule is not encountered yet
        # Continue parsing using current_rule
        if (seg_name in current_rule):
            seg_rule = current_rule[seg_name]

            # Case 1.1: Regular segment
            if (seg_rule['segtype'] == SegmentType.REGULAR):
                self.parse_regular_segment(seg_name)
                if ('subsegs' in seg_rule):
                    # This means this segment contains child elements of itself
                    # The next element(s) should be parsed using the its nested rule
                    self.rule_stack.append(seg_rule)

            # Case 1.2:
            # End-of-rule encountered now, that means there's no more child element for this rule
            # Remove current_rule from stack so that we can continue parsing its parent rule
            elif (seg_rule['segtype'] == SegmentType.CLOSING):
                self.rule_stack.pop()

            return True

        # Case 2: seg_name is defined in rule
        # Either segment definition is missing (un-implemented case), or
        # an end-of-loop signal
        else:
            # Just skip the segment for now
            # TODO: case 2 implementation
            return True

    def parse_regular_segment(self, segment_name):
        # TODO: Implementation
        pass
