class Advice(object):
    VALID_SEVERITIES = frozenset((
        'error',
    ))

    def __init__(self, analyzer, severity, message):
        # XXX validate severity

        self.analyzer = analyzer
        self.severity = severity
        self.message = message

    def format_display_line(self):
        return '%s: %s' % (self.severity, self.message)
