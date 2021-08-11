__all__ = ["Expression"]

from dataclasses import dataclass
from typing import Iterable, Optional

import regex as re
from regex.regex import Match

import maha.parsers.interfaces as interfaces
from maha.parsers.utils import convert_to_number_if_possible


@dataclass
class Expression:
    """Regex pattern holder.

    Parameters
    ----------
    pattern : str
        Regular expression pattern.
    """

    __slots__ = ["pattern", "_compiled_pattern"]

    pattern: str
    """Regular expersion(s) to match"""

    def __init__(
        self,
        pattern: str,
    ):
        self.pattern = pattern
        self._compiled_pattern = None

    def compile(self):
        """Compile the regular expersion."""
        if self._compiled_pattern is None:
            self._compiled_pattern = re.compile(self.pattern, re.MULTILINE)

    def search(self, text: str):
        """Search for the pattern in the input ``text``.

        Parameters
        ----------
        text : str
            Text to search in.

        Returns
        -------
        :class:`regex.Match`
            Matched object.
        """
        self.compile()
        return self._compiled_pattern.search(text)

    def match(self, text: str) -> Optional[Match]:
        """Match the pattern in the input ``text``.

        Parameters
        ----------
        text : str
            Text to match in.

        Returns
        -------
        :class:`regex.Match`
            Matched object.
        """
        self.compile()
        return self._compiled_pattern.match(text)

    def __call__(self, text: str) -> Iterable["interfaces.ExpressionResult"]:
        """
        Extract values from the input ``text``.

        Parameters
        ----------
        text : str
            Text to extract the value from.

        Yields
        -------
        :class:`ExpressionResult`
            Extracted value.
        """
        self.compile()

        for m in re.finditer(self._compiled_pattern, text):
            yield self.parse(m, text)

    def parse(self, match: Match, text: Optional[str]) -> "interfaces.ExpressionResult":
        """Extract the value from the input ``text`` and return it.

        .. note::
            This is a simple implementation that needs a group to match.

        .. warning::
            This method is called by :meth:`__call__` to extract the value from
            the input ``text``. You should not call this method directly.


        Parameters
        ----------
        match : :class:`regex.Match`
            Matched object.
        text : str
            Text in which the match was found.

        Yields
        -------
        :class:`ExpressionResult`
            Extracted value.

        Raises
        ------
        ValueError
            If no capture group was found.

        """
        start, end = match.span()

        captured_groups = match.groups()

        if captured_groups is None:
            raise ValueError("No captured groups")

        captured_groups = list(map(convert_to_number_if_possible, captured_groups))
        if len(captured_groups) == 1:
            captured_groups = captured_groups[0]
        value = captured_groups

        return interfaces.ExpressionResult(start, end, value, self)

    def __str__(self) -> str:
        return self.pattern

    def __add__(self, other: str) -> str:
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)
