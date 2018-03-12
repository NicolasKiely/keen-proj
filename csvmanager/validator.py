class Validator(object):
    ''' CSV validator '''
    def __init__(self):
        self.parsed_header = False
        self.row_num = 0
        self.col_num = 0

    def is_valid(self, record):
        ''' Returns flag, error message. Flag is true if valid, false otherwise '''
        if self.parsed_header:
            return self._is_valid_record(record)
        else:
            self.parsed_header = True
            return self._is_valid_header(record)

    def _is_valid_header(self, record):
        cols = record.split(',')
        self.col_num = len(cols)
        self.row_num += 1
        if cols > 0:
            return True, ''
        else:
            return False, 'No column detected'

    def _is_valid_record(self, record):
        self.row_num += 1
        srow = '#'+ str(self.row_num)

        # Split record by commas
        fields = [r.strip() for r in record.split(',')]

        # Check proper number of fields
        if len(fields) != self.col_num:
            return False, 'Invalid number of fields on line '+ srow

        # Valudate numbers for fields
        try:
            vals = [float(x) for x in fields[1:]]
        except ValueError:
            return False, 'Invalid number on line '+ srow

        # Validate non-negative values in non-index fields
        for val in vals:
            if val < 0:
                return False, 'Negative number on line '+ srow

        return True, ''
