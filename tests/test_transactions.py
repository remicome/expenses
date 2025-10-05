from expenses.definitions import Discount, Food, Housing, Member


def test_food():
    alice = Member(name="alice", discount=Discount.P1, stay_duration=1)
    bob = Member(name="bob", discount=Discount.P2, stay_duration=2)

    transaction = Food(
        value=100,
        payer=alice,
        members=[alice, bob],
    )
    assert 2 * transaction.weights[alice] == 0.75 * transaction.weights[bob]


def test_housing_maxed_out():
    alice = Member(name="alice", discount=Discount.P1, stay_duration=9)
    bob = Member(name="bob", discount=Discount.P2, stay_duration=10)

    transaction = Housing(
        value=100,
        payer=alice,
        members=[alice, bob],
    )
    assert transaction.weights[alice] == 0.75 * transaction.weights[bob]


def test_housing_halved():
    alice = Member(name="alice", discount=Discount.P1, stay_duration=5)
    bob = Member(name="bob", discount=Discount.P2, stay_duration=10)

    transaction = Housing(
        value=100,
        payer=alice,
        members=[alice, bob],
    )
    assert 2 * transaction.weights[alice] == 0.75 * transaction.weights[bob]
