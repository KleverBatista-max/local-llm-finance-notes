import unittest
from clasificar import validar

class T(unittest.TestCase):
    def test_valida(self): self.assertEqual(validar('{"categoria":"transporte"}'), "transporte")
    def test_inventada(self): self.assertEqual(validar('{"categoria":"yates"}'), "desconocido")
    def test_json_roto(self): self.assertEqual(validar('claro, es transporte'), "desconocido")
    def test_no_dict(self): self.assertEqual(validar('[1]'), "desconocido")

if __name__ == "__main__": unittest.main()
