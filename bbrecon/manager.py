from typing import Optional, List, Generator
from pydantic import HttpUrl
from datetime import datetime

from .client import AuthenticatedClient
from .api.programs import get_programs, get_program
from .api.domains import get_domains
from .models import Program, Domain
from .utils import paginate


class BugBountyRecon:
    def __init__(
        self, token: str, *, base_url: HttpUrl = "https://api.bugbountyrecon.com"
    ):
        self.client = AuthenticatedClient(base_url=base_url, token=token)

    def program(self, slug: str) -> Program:
        return get_program(client=self.client, slug=slug)

    def programs(
        self,
        *,
        name: Optional[str] = None,
        types: Optional[List[str]] = None,
        platforms: Optional[List[str]] = None,
        exclude_platforms: Optional[List[str]] = None,
        rewards: Optional[List[str]] = None,
        created_since: Optional[datetime] = None,
    ) -> Generator[Program, None, None]:
        for program in paginate(
            self.client,
            get_programs,
            name=name,
            types=types,
            platforms=platforms,
            exclude_platforms=exclude_platforms,
            rewards=rewards,
            created_since=created_since,
        ):
            yield program

    def domains(
        self,
        *,
        programs: Optional[List[str]] = None,
        created_since: Optional[datetime] = None,
    ) -> Generator[Domain, None, None]:
        for domain in paginate(
            self.client, get_domains, programs=programs, created_since=created_since
        ):
            yield domain
