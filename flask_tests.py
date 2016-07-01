import unittest

from server import APP as app


class TalosTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        req = self.app.get('/')
        response = str(req.data)
        assert response.count("<input") == 4
        assert 'name="prototypes"' in response
        assert 'name="axioms"' in response
        assert 'name="conjecture"' in response
        assert 'value="Prove"' in response

    def test_prover(self):
        req = self.app.post('/prove', data=dict(
            prototypes="typedef Greeting Action#Greeting hello Agent#Boolean greet Agent Greeting",
            axioms="forAll [x] implies(greet(James,hello(world)),greet(James,hello(x)))#"
                   "greet(James,hello(world))",
            conjecture="greet(James,hello(John))"
        ))

        response = str(req.data)

        check_string = "Proof Found<br />" \
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
               "(leads_to_conclusion (greet James (hello John)))<br />"

        for string in check_string.split("<br />"):
            assert string in response

if __name__ == "__main__":
    unittest.main()
