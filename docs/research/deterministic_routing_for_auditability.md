# Deterministic Routing for Auditability

Soft routing can be useful, but it is difficult to audit when decisions vary
across runs. A deterministic toy router makes routing behavior reviewable:

- capabilities are explicit
- priorities are visible
- ties are stable
- reasons are returned with decisions

The router in this package is intentionally weak. It demonstrates audit shape,
not production routing advantage.

