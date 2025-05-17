import re
import datetime

DANGER = "\033[91m"
WARNING = "\033[93m"
SUCCESS = "\033[92m"
INFO = "\033[94m"
RESET = "\033[0m"

def message_danger(text):
    print(f"{DANGER}{text}{RESET}")

def message_warning(text):
    print(f"{WARNING}{text}{RESET}")

def message_success(text):
    print(f"{SUCCESS}{text}{RESET}")

def message_info(text):
    print(f"{INFO}{text}{RESET}")

def input_text(prompt):
    while True:
        text = input(prompt).strip()
        if text.isalpha() or all(c.isalpha() or c.isspace() for c in text):
            return text
        else:
            message_danger("❌ Solo se permiten letras y espacios. Intente de nuevo.")

def input_numbers(prompt, type_cast=int, minimum=None, maximum=None):
    while True:
        value = input(prompt).strip()
        try:
            converted_value = type_cast(value)
            if (minimum is not None and converted_value < minimum) or (maximum is not None and converted_value > maximum):
                message_danger(f"❌ Valor debe estar entre {minimum} y {maximum}. Intente de nuevo.")
            else:
                return converted_value
        except:
            message_danger(f"❌ Entrada inválida. Ingrese un número {type_cast.__name__} válido.")

def input_option(prompt, options):
    options_lower = [o.lower() for o in options]
    while True:
        entry = input(f"{prompt} ({'/'.join(options)}): ").strip().lower()
        if entry in options_lower:
            return entry
        else:
            message_danger(f"❌ Opción inválida. Debe ser una de: {', '.join(options)}")

def input_date(prompt):
    while True:
        date_str = input(f"{prompt} (YYYY-MM-DD): ").strip()
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            return date_str
        except:
            message_danger("❌ Formato de fecha inválido. Use YYYY-MM-DD.")

def validate_main_luggage(weight):
    return weight <= 50

def validate_hand_luggage(weight):
    return weight <= 13

def generate_id(reservation_list):
    if not reservation_list:
        return "COMP0001"
    last_id = reservation_list[-1]["id"]
    number = int(last_id[4:]) + 1
    return f"COMP{number:04d}"

def calculate_cost(trip_type, luggage_weight):
    base = {"nacional": 230000, "internacional": 4200000}
    additional = 0
    if trip_type not in base:
        return None
    if luggage_weight <= 20:
        additional = 50000
    elif luggage_weight <= 30:
        additional = 70000
    elif luggage_weight <= 50:
        additional = 110000
    else:
        return None
    return base[trip_type] + additional

def purchase_summary(reservation):
    print(f"""
🛒 Resumen de Compra
ID: {reservation['id']}
Nombre: {reservation['nombre']}
Destino: {reservation['tipo_viaje'].capitalize()}
Fecha: {reservation['fecha']}
Estado equipaje principal: {reservation['estado_equipaje_principal']}
Estado equipaje de mano: {reservation['estado_equipaje_mano']}
Costo total: ${reservation['costo_total']:,}
""")

def validate_admin_password():
    password = input("🔑 Ingrese la contraseña de administrador: ").strip()
    return password == "jvelez1221"

def user_menu(reservations):
    print("\n🎟️ ===== MENÚ USUARIO ===== 🎟️")
    name = input_text("📝 Ingrese su nombre: ")
    trip_type = input_option("🌍 Tipo de viaje", ["nacional", "internacional"])
    main_luggage_weight = input_numbers("🎒 Peso del equipaje principal (kg): ", type_cast=float, minimum=0)
    if not validate_main_luggage(main_luggage_weight):
        message_danger("❌ Equipaje principal no admitido (más de 50 kg). Debe cancelar o viajar sin equipaje principal.")
        return
    hand_luggage = input_option("👜 ¿Lleva equipaje de mano?", ["sí", "no"])
    hand_luggage_weight = 0
    hand_luggage_status = "🚫 No lleva equipaje de mano"
    if hand_luggage == "sí":
        hand_luggage_weight = input_numbers("🎒 Peso del equipaje de mano (kg): ", type_cast=float, minimum=0)
        if validate_hand_luggage(hand_luggage_weight):
            hand_luggage_status = "✅ Equipaje de mano admitido"
        else:
            hand_luggage_status = "⚠️ Equipaje de mano rechazado (excede 13 kg)"
            message_warning("⚠️ Equipaje de mano rechazado pero puede viajar.")
    date = input_date("📅 Fecha del viaje")
    total_cost = calculate_cost(trip_type, main_luggage_weight)
    if total_cost is None:
        message_danger("❌ No se pudo calcular el costo total. Verifique datos.")
        return
    purchase_id = generate_id(reservations)
    reservation = {
        "id": purchase_id,
        "nombre": name,
        "tipo_viaje": trip_type,
        "peso_equipaje_principal": main_luggage_weight,
        "estado_equipaje_principal": "✅ Equipaje principal admitido",
        "peso_equipaje_mano": hand_luggage_weight,
        "estado_equipaje_mano": hand_luggage_status,
        "fecha": date,
        "costo_total": total_cost
    }
    reservations.append(reservation)
    message_success("\n🎉 ¡Compra realizada con éxito!")
    purchase_summary(reservation)

def report_total_revenue(reservations):
    total = sum(r["costo_total"] for r in reservations)
    message_info(f"💰 Total recaudado en todas las compras: ${total:,}")

def report_total_revenue_by_date(reservations):
    query_date = input_date("📅 Ingrese la fecha para consulta")
    total = sum(r["costo_total"] for r in reservations if r["fecha"] == query_date)
    message_info(f"💰 Total recaudado para la fecha {query_date}: ${total:,}")

def report_total_passengers(reservations):
    message_info(f"👥 Número total de pasajeros procesados: {len(reservations)}")

def report_passengers_by_type(reservations):
    nationals = sum(1 for r in reservations if r["tipo_viaje"] == "nacional")
    internationals = sum(1 for r in reservations if r["tipo_viaje"] == "internacional")
    message_info(f"🛫 Pasajeros nacionales: {nationals}")
    message_info(f"🌐 Pasajeros internacionales: {internationals}")

def search_by_id(reservations):
    search_id = input("🔍 Ingrese el ID de compra a consultar: ").strip().upper()
    found = False
    for r in reservations:
        if r["id"] == search_id:
            purchase_summary(r)
            found = True
            break
    if not found:
        message_danger("❌ No se encontró ninguna compra con ese ID.")

def admin_menu(reservations):
    print("\n🔒 ===== MENU ADMIN ===== 🔒")
    if not validate_admin_password():
        message_danger("❌ Contraseña incorrecta. Acceso denegado.")
        return
    while True:
        print("""
Opciones:
1 - Total recaudado en todas las compras
2 - Total recaudado para una fecha específica
3 - Número de pasajeros procesados en todas las compras
4 - Número de pasajeros nacionales e internacionales
5 - Consultar compra por ID
6 - Salir del modo administrador
""")
        option = input_numbers("🔢 Seleccione una opción: ", type_cast=int, minimum=1, maximum=6)
        if option == 1:
            report_total_revenue(reservations)
        elif option == 2:
            report_total_revenue_by_date(reservations)
        elif option == 3:
            report_total_passengers(reservations)
        elif option == 4:
            report_passengers_by_type(reservations)
        elif option == 5:
            search_by_id(reservations)
        elif option == 6:
            print("🔓 Saliendo del menu Admin")
            break
        else:
            message_danger("❌ Opción inválida.")
