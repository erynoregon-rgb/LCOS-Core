# SKOS to LCOS Boundary

LCOS is public. SKOS remains private.

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

LCOS code imports only `lcos_public` modules and Python standard library
modules. There are no SKOS dependencies.
