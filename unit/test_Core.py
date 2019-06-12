import hyde
import unittest

userManager = hyde.UserManager()
# create some users
ammar = userManager.createNewUser("Ammar Hakim", "super")
petr = userManager.createNewUser("Petr Cagas")
bhuvana = userManager.createNewUser("Bhuvana Srinivasan")
jimmy = userManager.createNewUser("Jimmy Juno")
guest = userManager.createNewUser("guest")

simManager = hyde.SimManager()
# add simulation objects
ammar_s1 = simManager.createNewSim("two-stream", ammar.userId, "print('two-stream')")
ts = simManager.createNewTemplateSim(ammar_s1)
jimmy_s1 = simManager.createNewSim("weibel", jimmy.userId, "print('weibel')")
jimmy_s2 = simManager.createNewSim("shock", jimmy.userId, "print('shock')")

class TestUser(unittest.TestCase):

    def test_users(self):
        userManager = hyde.UserManager()
        ulist = userManager.getUsers()
        self.assertEqual(5, len(ulist))

        u = hyde.User(ammar.userId)
        self.assertEqual(u.name(), "Ammar Hakim")
        self.assertEqual(u.group(), "super")

        u = hyde.User(petr.userId)
        self.assertEqual(u.name(), "Petr Cagas")
        self.assertEqual(u.group(), "regular")

    def test_sims(self):
        simManager = hyde.SimManager()
        slist = simManager.getSimsInState("pending")
        self.assertEqual(3, len(slist))
        
        a = hyde.User(ammar.userId)
        ammarPending = a.simList("pending")
        self.assertEqual(1, len(ammarPending))

        ammarTemplate = a.simList("template")
        self.assertEqual(1, len(ammarTemplate))

        j = hyde.User(jimmy.userId)

        jimmyPending = j.simList("pending")
        self.assertEqual(2, len(jimmyPending))

        jimmyTemplate = j.simList("template")
        self.assertEqual(0, len(jimmyTemplate))

if __name__ == '__main__':
    unittest.main()

