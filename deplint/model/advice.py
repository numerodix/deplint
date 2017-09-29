class Advice(object):
    '''
    Represents an advice message reported by an analyzer.
    '''

    VALID_SEVERITIES = frozenset((
        'debug',
        'info',
        'warn',
        'error',
    ))

    def __init__(self, analyzer, severity, message):
        if severity not in self.VALID_SEVERITIES:
            raise ValueError("Invalid severity: %s" % severity)

        self.analyzer = analyzer
        self.severity = severity
        self.message = message

    def __repr__(self):
        return '<%s analyzer=%r, severity=%r, message=%r>' % (
            self.__class__.__name__,
            self.analyzer.__class__.__name__,
            self.severity,
            self.message,
        )

    def __eq__(self, other):
        if not type(other) == self.__class__:
            return False

        return all((
            self.analyzer == other.analyzer,
            self.severity == other.severity,
            self.message == other.message,
        ))

    def __ne__(self, other):
        return not self.__eq__(other)

    def format_display_line(self):
        return '[%s] %s: %s' % (
            self.analyzer.__class__.__name__.replace('Analyzer', ''),
            self.severity,
            self.message,
        )
