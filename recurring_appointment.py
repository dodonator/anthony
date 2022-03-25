from datetime import datetime

import dateutil.relativedelta as drel
import dateutil.rrule as dr


class RecurringAppointment:
    title: str
    content: str
    start: datetime
    rule: dr.rrule

    def __init__(self, title, content, start, rule):
        self.title = title
        self.content = content
        self.start = start
        self.rule = rule
        self._rule_it = iter(self.rule)

    def next_datetime(self):
        return self.rule.after(self.start)


start = datetime(2022, 1, 7, 18, 0)
rule = dr.rrule(dr.WEEKLY, dtstart=start, byweekday=drel.FR)

freitagsfoo = RecurringAppointment(
    title="Freitagsfoo",
    content="Freitagsfoo im chaosdorf",
    start=start,
    rule=rule,
)
