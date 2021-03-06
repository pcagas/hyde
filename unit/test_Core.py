import hyde
import unittest

userManager = hyde.UserManager()
# create some users
ammar = userManager.createNewUser("Ammar Hakim", "ammar", "ahakim@pppl.gov", "127.0.0.1", "super")
petr = userManager.createNewUser("Petr Cagas", "petr", "cagas@vt.edu", "127.0.0.2")
bhuvana = userManager.createNewUser("Bhuvana Srinivasan", "srinbhu", "bhuvana@vt.edu", "127.0.0.3")
jimmy = userManager.createNewUser("Jimmy Juno", "jjuno", "jjuno@pppl.gov", "127.0.0.4")
guest = userManager.createNewUser("guest", "guest", "guest@gmail.gov", "127.0.0.5")

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
        slist = simManager.getSimsInState("editing")
        self.assertEqual(3, len(slist))
        
        a = hyde.User(ammar.userId)
        ammarEditing = a.simList("editing")
        self.assertEqual(1, len(ammarEditing))

        ammarTemplate = a.simList("template")
        self.assertEqual(1, len(ammarTemplate))

        j = hyde.User(jimmy.userId)

        jimmyEditing = j.simList("editing")
        self.assertEqual(2, len(jimmyEditing))

        jimmyTemplate = j.simList("template")
        self.assertEqual(0, len(jimmyTemplate))

if __name__ == '__main__':
    unittest.main()

