import unittest

import server


class TalosTestCase(unittest.TestCase):
    def setUp(self):
        server.APP.config['TESTING'] = True
        self.app = server.APP.test_client()

    def test_index(self):
        req = self.app.get('/')
        assert req.data.count("<input") == 4
        assert 'name="prototypes"' in req.data
        assert 'name="axioms"' in req.data
        assert 'name="conjecture"' in req.data
        assert 'value="Prove"' in req.data

    def test_prover(self):
        req = self.app.post('/prove', data=dict(
            prototypes="typedef Greeting Action#Greeting hello Agent#Boolean greet Agent Greeting",
            axioms="forAll [x] implies(greet(James,hello(world)),greet(James,hello(x)))#"
                   "greet(James,hello(world))",
            conjecture="greet(James,hello(John))"
        ))
        assert "Proof Found<br />" \
               "Proof:<br />" \
               "(greet James (hello world))<br />" \
               "(forAll (Agent b0) (implies (greet James (hello world)) (greet James " \
               "(hello b0))))<br />" \
               "&nbsp;&nbsp;&nbsp;&nbsp;(forAll (Boolean b0) (forAll (Boolean c0) (implies c0 " \
               "(implies (implies c0 b0) b0))))<br />" \
               "(forAll (Agent b0) (greet James (hello b0)))<br />" \
               "&nbsp;&nbsp;&nbsp;&nbsp;(forAll (Agent b0) (implies (greet James (hello world)) " \
               "(greet James (hello b0))))<br />" \
               "&nbsp;&nbsp;&nbsp;&nbsp;(greet James (hello world))<br />" \
               "(leads_to_conclusion )<br />" \
               "&nbsp;&nbsp;&nbsp;&nbsp;(forAll (Agent b0) (greet James (hello b0)))<br />" \
               "&nbsp;&nbsp;&nbsp;&nbsp;(leads_to_conclusion (greet James (hello John)))<br />" \
               "(forAll (Boolean b0) (forAll (Boolean c0) (implies c0 (implies (implies c0 b0) " \
               "b0))))<br />" \
               "&nbsp;&nbsp;&nbsp;&nbsp;(forAll (Boolean b0) (forAll (Boolean c0) (implies b0 " \
               "(implies (implies " \
               "b0 c0) c0))))<br />" \
               "(forAll (Boolean b0) (forAll (Boolean c0) (implies b0 (implies (implies b0 c0) " \
               "c0))))<br />" \
               "(leads_to_conclusion (greet James (hello John)))<br />" in req.data

        a = "hello adlafd" \
            ";af"
if __name__ == "__main__":
    unittest.main()
