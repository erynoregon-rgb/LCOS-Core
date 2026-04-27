# SKOS to LCOS Boundary

LCOS Toy is public. SKOS remains private.

## Shared at concept level

- receipt-gated thinking
- governed decisions
- explicit hold/escalate states
- bounded execution surfaces
- replayable audit trails

## Not shared

- SKOS implementation code
- SKOS vocabulary dependence
- private system internals
- production configuration
- internal implementation details
- real operational data

## Boundary check

LCOS Toy code imports only `lcos_toy` modules and Python standard library
modules. There are no SKOS dependencies.
