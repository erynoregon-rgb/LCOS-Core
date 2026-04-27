from lcos.routing.registry import KernelDescriptor
from lcos.routing.router import DeterministicRouter


def test_router_routes_known_capability() -> None:
    router = DeterministicRouter([
        KernelDescriptor(kernel_id="k1", capability="receipt", schema="receipt_record", priority=1)
    ])
    result = router.route("receipt example")
    assert result.decision == "ROUTE"
    assert result.kernel_id == "k1"


def test_router_escalates_novel_content() -> None:
    router = DeterministicRouter([])
    result = router.route("novel unknown task")
    assert result.decision == "ESCALATE"
