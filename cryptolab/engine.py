"""Replay prepaid subscription deposits, periodic charges and cancellation with service entitlement checkpoints."""

from .common import (
    number,
    integer,
    identity,
    records,
    chronology,
    allocate,
    result,
    validate_document,
)
from decimal import Decimal


def _analyze(d):
    period = integer(d["period_seconds"], 1)
    price = integer(d["period_price"], 1)
    balances = {identity(k): integer(v) for k, v in d["balances"].items()}
    paid_until = {k: integer(d["start"]) for k in balances}
    cancelled = set()
    revenue = 0
    trace = []
    for e in chronology(d["events"]):
        account = identity(e["account"])
        kind = e["kind"]
        t = e["timestamp"]
        if account not in balances:
            raise ValueError("unknown subscriber")
        charged = 0
        if kind == "deposit":
            balances[account] += integer(e["amount"], 1)
        elif kind == "cancel":
            cancelled.add(account)
        elif kind == "renew":
            if account in cancelled:
                raise ValueError("cancelled subscription")
            if t < paid_until[account]:
                raise ValueError("subscription not due")
            if balances[account] >= price:
                balances[account] -= price
                charged = price
                revenue += price
                paid_until[account] = t + period
        else:
            raise ValueError("unknown subscription event")
        trace.append(
            {
                "timestamp": t,
                "account": account,
                "charged": charged,
                "balance": balances[account],
                "paid_until": paid_until[account],
                "cancelled": account in cancelled,
            }
        )
    return {
        "balances": balances,
        "paid_until": paid_until,
        "revenue": revenue,
        "cancelled": sorted(cancelled),
        "trace": trace,
    }


def analyze(document):
    validate_document(document)
    try:
        return result(_analyze(document))
    except (KeyError, TypeError, ArithmeticError, RecursionError) as error:
        raise ValueError("invalid domain input: " + str(error)) from error
