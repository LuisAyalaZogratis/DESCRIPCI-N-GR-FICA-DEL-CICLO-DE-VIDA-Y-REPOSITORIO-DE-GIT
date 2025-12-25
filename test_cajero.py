import unittest
from cajero import Cuenta

class TestCuenta(unittest.TestCase):
    def setUp(self):
        self.cuenta = Cuenta("test_id", "1234", 1000)

    def test_validar_pin(self):
        self.assertTrue(self.cuenta.validar_pin("1234"))
        self.assertFalse(self.cuenta.validar_pin("0000"))

    def test_depositar(self):
        exito, msg = self.cuenta.depositar(500)
        self.assertTrue(exito)
        self.assertEqual(self.cuenta.ver_saldo(), 1500)

        # Test negative deposit
        exito, msg = self.cuenta.depositar(-100)
        self.assertFalse(exito)
        self.assertEqual(self.cuenta.ver_saldo(), 1500)

    def test_retirar(self):
        # Successful withdrawal
        exito, msg = self.cuenta.retirar(200)
        self.assertTrue(exito)
        self.assertEqual(self.cuenta.ver_saldo(), 800)

        # Insufficient funds
        exito, msg = self.cuenta.retirar(1000)
        self.assertFalse(exito)
        self.assertEqual(self.cuenta.ver_saldo(), 800)

        # Negative withdrawal
        exito, msg = self.cuenta.retirar(-50)
        self.assertFalse(exito)
        self.assertEqual(self.cuenta.ver_saldo(), 800)

    def test_ver_historial(self):
        self.cuenta.depositar(100)
        self.cuenta.retirar(50)
        historial = self.cuenta.ver_historial()
        # 1 initial + 1 deposit + 1 withdrawal = 3 records
        self.assertEqual(len(historial), 3)
        self.assertEqual(historial[1]['tipo'], "Depósito")
        self.assertEqual(historial[2]['tipo'], "Retiro")

if __name__ == '__main__':
    unittest.main()
