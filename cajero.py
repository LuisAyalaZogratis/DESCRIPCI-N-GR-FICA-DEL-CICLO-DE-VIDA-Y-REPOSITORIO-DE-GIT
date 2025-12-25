import sys
from datetime import datetime

class Cuenta:
    def __init__(self, id_cuenta, pin, saldo_inicial=0):
        self.id_cuenta = id_cuenta
        self.pin = pin
        self.saldo = saldo_inicial
        self.historial = []
        self._registrar_movimiento("Creación de cuenta", saldo_inicial)

    def validar_pin(self, pin_ingresado):
        return self.pin == pin_ingresado

    def depositar(self, monto):
        if monto > 0:
            self.saldo += monto
            self._registrar_movimiento("Depósito", monto)
            return True, f"Depósito exitoso. Nuevo saldo: ${self.saldo:.2f}"
        return False, "El monto debe ser positivo."

    def retirar(self, monto):
        if monto > 0:
            if self.saldo >= monto:
                self.saldo -= monto
                self._registrar_movimiento("Retiro", -monto)
                return True, f"Retiro exitoso. Nuevo saldo: ${self.saldo:.2f}"
            return False, "Fondos insuficientes."
        return False, "El monto debe ser positivo."

    def ver_saldo(self):
        return self.saldo

    def ver_historial(self):
        return self.historial

    def _registrar_movimiento(self, tipo, monto):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.historial.append({
            "fecha": fecha,
            "tipo": tipo,
            "monto": monto,
            "saldo_post": self.saldo
        })

class Cajero:
    def __init__(self):
        # Simulación de base de datos
        self.cuentas = {
            "12345": Cuenta("12345", "1234", 1000),
            "67890": Cuenta("67890", "0000", 500)
        }
        self.cuenta_actual = None

    def iniciar(self):
        print("=== BIENVENIDO AL CAJERO AUTOMÁTICO ===")
        while True:
            if not self.cuenta_actual:
                if not self.login():
                    continue

            self.mostrar_menu()

    def login(self):
        id_cuenta = input("\nIngrese su número de cuenta: ")
        if id_cuenta in self.cuentas:
            pin = input("Ingrese su PIN: ")
            if self.cuentas[id_cuenta].validar_pin(pin):
                self.cuenta_actual = self.cuentas[id_cuenta]
                print(f"\nBienvenido/a. Saldo actual: ${self.cuenta_actual.ver_saldo():.2f}")
                return True
            else:
                print("PIN incorrecto.")
        else:
            print("Cuenta no encontrada.")
        return False

    def mostrar_menu(self):
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Consultar Saldo")
        print("2. Depositar")
        print("3. Retirar")
        print("4. Ver Movimientos")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print(f"\nSaldo actual: ${self.cuenta_actual.ver_saldo():.2f}")
        elif opcion == "2":
            try:
                monto = float(input("\nMonto a depositar: "))
                exito, mensaje = self.cuenta_actual.depositar(monto)
                print(mensaje)
            except ValueError:
                print("Entrada inválida. Por favor ingrese un número.")
        elif opcion == "3":
            try:
                monto = float(input("\nMonto a retirar: "))
                exito, mensaje = self.cuenta_actual.retirar(monto)
                print(mensaje)
            except ValueError:
                print("Entrada inválida. Por favor ingrese un número.")
        elif opcion == "4":
            print("\n--- Últimos Movimientos ---")
            for mov in self.cuenta_actual.ver_historial():
                print(f"{mov['fecha']} | {mov['tipo']:<15} | {mov['monto']:>10.2f} | Saldo: {mov['saldo_post']:.2f}")
        elif opcion == "5":
            print("\nGracias por usar nuestro cajero. ¡Hasta luego!")
            self.cuenta_actual = None
            # Regresa al bucle principal en iniciar(), pidiendo login nuevamente
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    cajero = Cajero()
    try:
        cajero.iniciar()
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
