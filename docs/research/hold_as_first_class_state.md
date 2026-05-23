# Hold as a First-Class State

Simple systems often model execution as accept/reject. Governed systems need a
third stable state: hold.

Hold means the system preserves the request, explains the reason it did not
execute, and waits for more evidence. In this package, hold appears in the
intake workbench and router as a safe default when information is incomplete.

This is a public research note. It does not publish production hold policy.
