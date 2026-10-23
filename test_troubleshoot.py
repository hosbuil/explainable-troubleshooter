import unittest
from troubleshoot import diagnose

class DiagnosisTests(unittest.TestCase):
    def test_dns_evidence(self):
        result = diagnose(dict(power=True, wifi=True, internet_ip=True, dns=False))
        self.assertEqual([r['rule'] for r in result['recommendations']], ['dns'])

    def test_unknown_is_not_false(self):
        self.assertEqual(diagnose({})['recommendations'], [])
        self.assertEqual(diagnose({})['status'], 'insufficient_evidence')

    def test_power_blocks_downstream_rules(self):
        result = diagnose(dict(power=False, wifi=True, internet_ip=True, dns=False, disk_full=True))
        self.assertEqual([r['rule'] for r in result['recommendations']], ['power'])

    def test_multiple_findings(self):
        result = diagnose(dict(power=True, wifi=False, disk_full=True))
        self.assertEqual([r['rule'] for r in result['recommendations']], ['wifi', 'disk'])

    def test_healthy_observations_do_not_prove_a_fault(self):
        result = diagnose(dict(power=True, wifi=True, internet_ip=True, dns=True, other_sites=False, disk_full=False))
        self.assertEqual(result['status'], 'no_matching_rule')

    def test_invalid_values(self):
        for value in [0, 1, 'false', [], {}]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                diagnose({'power': value})

    def test_unknown_key(self):
        with self.assertRaises(ValueError): diagnose({'password': True})

    def test_non_object(self):
        with self.assertRaises(ValueError): diagnose([])

if __name__ == '__main__': unittest.main()
