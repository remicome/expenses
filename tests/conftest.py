import random

import pytest
from expenses.definitions import Member, Transaction


@pytest.fixture()
def transactions(members):
    """a list of random transactions."""
    return [
        Transaction(
            value=random.randint(0, 10),
            payer=random.choice(members),
            members=random.sample(members, k=random.randint(1, len(members))),
        )
        for _ in range(10)
    ]


@pytest.fixture()
def members():
    return [
        Member(name="first"),
        Member(name="second"),
        Member(name="third"),
    ]
