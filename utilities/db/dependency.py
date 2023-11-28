from typing import Annotated

from fastapi import Depends

from .repository import OffsetLimitPaginator, PagePaginator

OffsetLimitPaginator = Annotated[OffsetLimitPaginator, Depends()]
PagePaginator = Annotated[PagePaginator, Depends()]
