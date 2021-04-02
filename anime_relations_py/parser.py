import re
from typing import Dict, List, Optional

from .rule import Rule

aiohttp_installed = False
requests_installed = False

try:
    import aiohttp
    aiohttp_installed = True
except ImportError:
    pass

try:
    import requests
    requests_installed = True
except ImportError:
    pass


if not aiohttp_installed and not requests_installed:
    raise ImportError("At least one web driver is required. Please install aiohttp or requests.")


class AnimeRelations:
    session: Optional[aiohttp.ClientSession]

    username: str
    repo_name: str
    branch_name: str
    file_path: str

    meta: Dict[str, str]
    rules: List[Rule]

    def __init__(self, **kwargs) -> None:
        """
        Creates a new AnimeRelations parser with the
        passed parameters.

        Parameters
        ----------
        session: Optional[aiohttp.ClientSession]
            Session for retrieving the file(s).
        username: str
            The username the repo is hosted
            under.
        repo_name: str
            The repository the file is hosted
            in.
        branch_name: str
            The branch that the file is located
            in.
        file_path: str
            The name of the file that contains
            the rules.
        """
        self.session = kwargs.pop("session", None)
        if aiohttp_installed and self.session is None:
            self.session = aiohttp.ClientSession()

        self.username = kwargs.pop("username", "erengy")
        self.repo_name = kwargs.pop("repo_name", "anime-relations")
        self.branch_name = kwargs.pop("branch_name", "master")
        self.file_path = kwargs.pop("file_path", "anime-relations.txt")

        self.meta = {}
        self.rules = []

    async def fetch_async(self) -> None:
        """
        Asynchronously fetches new rules with the
        existing configuration.

        Updates the instance with the parsed new rules.
        """
        url = f"https://raw.githubusercontent.com/{self.username}/{self.repo_name}/{self.branch_name}/{self.file_path}"
        async with self.session.get(url) as resp:
            self.parse(await resp.text())

    def fetch_sync(self) -> None:
        """
        Synchronously fetches new rules with the
        existing configuration.

        Updates the instance with the parsed new rules.
        """
        url = f"https://raw.githubusercontent.com/{self.username}/{self.repo_name}/{self.branch_name}/{self.file_path}"
        resp = requests.get(url)
        self.parse(resp.text)

    def parse(self, data: str) -> None:
        """
        Parses a string of data for rules and meta.

        Parameters
        ----------
        data: str
            String to parse for rules and meta.
        """
        in_meta = False
        in_rules = False

        for line in data.split("\n"):
            if line.startswith("#"):
                continue
            elif line.startswith("::meta"):
                in_meta = True
                in_rules = False
            elif line.startswith("::rules"):
                in_rules = True
                in_meta = False

            if in_meta:
                rule = re.match(r"- (\S+): (\S+)", line)
                if rule is None:
                    continue
                self.meta[rule.group(1)] = rule.group(2)
            elif in_rules:
                rules = Rule.from_line(line)
                self.rules += rules

    def from_mal(self, mal_id: int) -> Optional[Rule]:
        """
        Retrieves a Rule based on the passed MAL id.

        Parameters
        ----------
        mal_id: int
            The rule with the MAL id to
            search for.

        Returns
        -------
        Optional[Rule]
            The found rule.
        """
        for rule in self.rules:
            if rule.mal_from == mal_id:
                return rule

    def from_kitsu(self, kitsu_id: int) -> Optional[Rule]:
        """
        Retrieves a Rule based on the passed kitsu id.

        Parameters
        ----------
        kitsu_id: int
            The rule with the kitsu id to
            search for.

        Returns
        -------
        Optional[Rule]
            The found rule.
        """
        for rule in self.rules:
            if rule.kitsu_from == kitsu_id:
                return rule

    def from_anilist(self, anilist_id: int) -> Optional[Rule]:
        """
        Retrieves a Rule based on the passed anilist id.

        Parameters
        ----------
        anilist_id: int
            The rule with the anilist id to
            search for.

        Returns
        -------
        Optional[Rule]
            The found rule.
        """
        for rule in self.rules:
            if rule.anilist_from == anilist_id:
                return rule
