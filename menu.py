from utilities import *
import sys

reservas = []

def main_menu():
    print("🎫 === Ticket System === 🎫")
    while True:
        option = input_option("Ingrese 1 para Admin o 2 para Usuario", ["1", "2"])
        if option == "1":
            admin_menu(reservas)
        elif option == "2":
            user_menu(reservas)
        else:
            message_danger("❌ Opción inválida.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n👋 Saliendo del programa...")
        sys.exit()
