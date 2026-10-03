# Subscription escrow billing replay: domain model

Replay prepaid subscription deposits, periodic charges and cancellation with service entitlement checkpoints.

## Input contract

| Field | Example JSON shape |
|---|---|
| `period_seconds` | `int` |
| `period_price` | `int` |
| `start` | `int` |
| `balances` | `dict` |
| `events` | `list` |

The fixture includes nested records and concrete units. Engine validation is authoritative: required keys are read explicitly, identifiers must be nonempty, integer amounts reject booleans, record IDs are unique where indicated, and chronological logs reject reversed timestamps. A document is bounded to 100,000 values, depth 25 and 10,000 entries per collection. Domain-specific tighter bounds apply where required. Extra fields are tolerated and ignored.

## Calculation and outputs

The domain function executes on supplied data without mutation. Results include intermediate allocations, traces or per-scenario records so aggregate outputs can be reconciled. Four known-answer assertions in `tests/test_domain.py` cover the example independently of the generated regression output. Inspect `cryptolab/engine.py` for the executable algorithm and explicit rejection paths.

## Explicit assumptions

Insufficient deposits leave renewal uncharged. Cancellation prevents future renewals; current paid service remains valid until paid_until. No automatic debit or refund processing.

Input correctness and completeness remain the caller's responsibility. Offline results are educational and cannot prove external account ownership, protocol safety, source authenticity or future outcomes. Decimal precision follows Python's default 28 significant digits. Do not use illustrative fixture numbers as market data.
