from lcos.routing.registry import KernelDescriptor
from lcos.routing.router import DeterministicRouter
from lcos.kernels.mock import MockKernel


def main() -> None:
    registry = [
        KernelDescriptor(kernel_id="kernel-receipts", capability="receipt", schema="receipt_record", priority=10),
        KernelDescriptor(kernel_id="kernel-intake", capability="intake", schema="intake_record", priority=9),
    ]
    router = DeterministicRouter(registry)

    for query in [
        "route this receipt example",
        "this is a novel unknown task",
        "small ambiguous request",
    ]:
        result = router.route(query)
        if result.kernel_id:
            output = MockKernel(result.kernel_id, "demo_schema").process(query)
        else:
            output = {"decision": result.decision, "reason": result.reason}
        print(output)


if __name__ == "__main__":
    main()
