import unittest
import bank

class TestBank(unittest.TestCase):
    def test_init(self):
        account = bank.BankAccount("John Doe", 1000.0, 1234)

        self.assertEqual(account.name, "John Doe")
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.account_number, 1234)
        
        self.assertNotEqual(account.name, "foobar")
        self.assertNotEqual(account.balance, 0)
        self.assertNotEqual(account.account_number, 1111)


    def test_withdraw(self):
        account = bank.BankAccount("Jane Doe", 1000.0, 5678)
        self.assertRaises(ValueError, account.withdraw, 100000)
        account.withdraw(1000)
        self.assertEqual(account.balance, 0)
        self.assertNotEqual(account.balance, -1000)
        self.assertRaises(TypeError, account.withdraw, "foo")

    def test_deposit(self):
        account = bank.BankAccount("Lorem Ipsum", 0, 314159)
        self.assertEquals(account.balance, 0)
        account.deposit(500.0)
        self.assertNotEquals(account.balance, 0)
        self.assertEquals(account.balance, 500)
        self.assertRaises(TypeError, account.deposit, "bar")

    def test_print_balance(self):
        account = bank.BankAccount("John Doe", 500.00, 9012)
        self.assertIsNone(account.print_balance())
        self.assertNotEquals(account.print_balance(), 500.00)

if __name__ == "__main__":
    unittest.main()