from __future__ import annotations

from dataclasses import dataclass
import re
from typing import List, Optional, Tuple


RULE_PATTERN = re.compile(r"- (?P<mal_from>[\d\?]+)\|(?P<kitsu_from>[\d\?]+)\|(?P<anilist_from>[\d\?]+):(?P<episodes_from>[\d\-]+) -> (?P<mal_to>[\d\?~]+)\|(?P<kitsu_to>[\d\?~]+)\|(?P<anilist_to>[\d\?~]+):(?P<episodes_to>[\d\-!]+)")


@dataclass
class Rule:
    raw: str

    mal_from: Optional[int]
    kitsu_from: Optional[int]
    anilist_from: Optional[int]

    episodes_from: Tuple[int, Optional[int]]

    mal_to: Optional[int]
    kitsu_to: Optional[int]
    anilist_to: Optional[int]

    episodes_to: Tuple[int, Optional[int]]

    @classmethod
    def from_line(cls, line: str) -> List[Rule]:
        """
        Creates a Rule instance from a line
        of text.

        Returns a list of rules, as it is possible
        that multiple rules can be created from a
        single line.

        If there is not a valid rule in the passed
        string, then nothing will be returned.

        Parameters
        ----------
        line: str
            The line to find a rule in.

        Returns
        -------
        List[Rule]
            The rules.
        """
        instances = []
        parsed = re.match(RULE_PATTERN, line)
        if parsed is None:
            return instances

        episodes_from = parsed.group("episodes_from")
        if "-" in episodes_from:
            start, end = episodes_from.split("-")
            if end != "?":
                episodes_from = (int(start), int(end))
            else:
                episodes_from = (int(start), None)
        else:
            episodes_from = (int(episodes_from), int(episodes_from))

        mal_from = parsed.group("mal_from")
        mal_from = int(mal_from) if mal_from != "?" else None

        kitsu_from = parsed.group("kitsu_from")
        kitsu_from = int(kitsu_from) if kitsu_from != "?" else None

        anilist_from = parsed.group("anilist_from")
        anilist_from = int(anilist_from) if anilist_from != "?" else None

        mal_to = parsed.group("mal_to")
        if mal_to == "~":
            mal_to = mal_from
        else:
            mal_to = int(mal_to) if mal_to != "?" else None

        kitsu_to = parsed.group("kitsu_to")
        if kitsu_to == "~":
            kitsu_to = kitsu_from
        else:
            kitsu_to = int(kitsu_to) if kitsu_to != "?" else None

        anilist_to = parsed.group("anilist_to")
        if anilist_to == "~":
            anilist_to = anilist_from
        else:
            anilist_to = int(anilist_to) if anilist_to != "?" else None

        episodes_to = parsed.group("episodes_to").replace("!", "")
        if "-" in episodes_to:
            start, end = episodes_to.split("-")
            if end != "?":
                episodes_to = (int(start), int(end))
            else:
                episodes_to = (int(start), None)
        else:
            episodes_to = (int(episodes_to), int(episodes_to))

        if parsed.group("episodes_to").endswith("!"):
            redirect = cls(
                raw=parsed.group(0),
                mal_from=mal_to,
                kitsu_from=kitsu_to,
                anilist_from=anilist_to,
                episodes_from=episodes_from,
                mal_to=mal_to,
                kitsu_to=kitsu_to,
                anilist_to=anilist_to,
                episodes_to=episodes_to
            )
            instances.append(redirect)

        instance = cls(
            raw=parsed.group(0),
            mal_from=mal_from,
            kitsu_from=kitsu_from,
            anilist_from=anilist_from,
            episodes_from=episodes_from,
            mal_to=mal_to,
            kitsu_to=kitsu_to,
            anilist_to=anilist_to,
            episodes_to=episodes_to
        )

        instances.append(instance)

        return instances

    def get_episode_redirect(self, episode: int) -> Optional[int]:
        """
        Retrieves the redirect for a passed episode.

        Parameters
        ----------
        episode: int
            The episode to get the redirect
            for.

        Returns
        -------
        Optional[int]
            The redirected episode.
            None if it could not be calculated.
        """
        try:
            if episode < self.episodes_from[0] or episode > self.episodes_from[1]:
                return None
        except TypeError:
            pass

        offset = episode - self.episodes_from[0]

        try:
            if offset + self.episodes_to[0] > self.episodes_to[1]:
                return None
        except TypeError:
            pass

        return offset + self.episodes_to[0]
