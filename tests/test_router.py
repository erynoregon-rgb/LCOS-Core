import unittest

from lcos_public.router import Capability, PublicRouter


class RouterTests(unittest.TestCase):
    def test_router_is_deterministic(self):
        router = PublicRouter([Capability("b", "audit", 1), Capability("a", "audit", 1)])
        first = router.route("audit this receipt")
        second = router.route("audit this receipt")
        self.assertEqual(first, second)
        self.assertEqual(first.kernel_id, "a")

    def test_unknown_escalates(self):
        router = PublicRouter([Capability("receipt", "receipt", 1)])
        route = router.route("novel unknown request")
        self.assertEqual(route.decision.kind, "ESCALATE")

    def test_unmatched_holds(self):
        router = PublicRouter([Capability("receipt", "receipt", 1)])
        route = router.route("please do something")
        self.assertEqual(route.decision.kind, "HOLD")


if __name__ == "__main__":
    unittest.main()
