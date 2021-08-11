__all__ = ["NumeralExpression"]

from typing import Optional

from regex.regex import Match

from ..interfaces import Expression, ExpressionResult
from .utils import get_matched_numeral, get_value


class NumeralExpression(Expression):
    def parse(self, match: Match, text: Optional[str]) -> "ExpressionResult":

        start, end = match.span()
        groups = match.capturesdict()

        values = groups.get("value")
        units = groups.get("unit")

        # if not units, then it's ones or tens
        if not units:
            return ExpressionResult(start, end, get_value(values[0]), self)

        output = 0
        for value, unit in zip(values, units):
            if not value:
                output += get_matched_numeral(unit)
                continue

            value = get_value(value)

            if not unit:
                output += value
            else:
                output += value * get_matched_numeral(unit)

        return ExpressionResult(start, end, output, self)
