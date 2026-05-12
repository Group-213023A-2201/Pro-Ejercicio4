
import datetime

from models import Client, Consulting, EquipmentRental, Reservation, RoomRental

class SystemLogger:
    # Define a class variable for the log file name.
    FILE_NAME = "software_fj_logs.txt"

    # Define a static method to log events, which takes a message string as input and appends it to the log file with a timestamp.
    @staticmethod
    def log_event(message: str) -> None:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(SystemLogger.FILE_NAME, "a") as log_file:
            log_file.write(f"[{current_time}] - {message}\n")

            # --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    SystemLogger.log_event("=== SYSTEM START: Executing 10 Operations ===")

    # Setup base variables
    client_valid = None
    service_room = None
    reservation_valid = None

    # OPERATION 1: Valid Client
    try:
        client_valid = Client("C001", "Alice", "alice@email.com")
        SystemLogger.log_event("Op 1 Success: Valid Client created.")
    except Exception as e:
        SystemLogger.log_event(f"Op 1 Failed: {e}")

    # OPERATION 2: Invalid Client (Intentional Error - Missing @)
    try:
        client_invalid = Client("C002", "Bob", "bob_email.com")
        SystemLogger.log_event("Op 2 Success: Client created.")
    except Exception as e:
        SystemLogger.log_event(f"Op 2 Failed (Handled Exception): {e}")

    # OPERATION 3: Room Rental Service
    try:
        service_room = RoomRental("S001", client_valid.get_name(), hours=5, rate_per_hour=20.0)
        SystemLogger.log_event(f"Op 3 Success: {service_room.describe_service()}")
    except Exception as e:
        SystemLogger.log_event(f"Op 3 Failed: {e}")

    # OPERATION 4: Equipment Rental Service
    try:
        service_equipment = EquipmentRental("S002", "Charlie", days=3, daily_rate=50.0)
        SystemLogger.log_event(f"Op 4 Success: {service_equipment.describe_service()}")
    except Exception as e:
        SystemLogger.log_event(f"Op 4 Failed: {e}")

    # OPERATION 5: Consulting Service (Testing Default Parameter Overloading)
    try:
        service_consulting = Consulting("S003", "Diana", sessions=4, fee_per_session=100.0)
        cost_no_discount = service_consulting.calculate_cost()
        cost_with_discount = service_consulting.calculate_cost(discount_percentage=10.0)
        SystemLogger.log_event(f"Op 5 Success: Consulting cost {cost_no_discount} (Discounted: {cost_with_discount})")
    except Exception as e:
        SystemLogger.log_event(f"Op 5 Failed: {e}")

    # OPERATION 6: Valid Reservation Creation
    try:
        reservation_valid = Reservation("R001", client_valid, service_room, duration=5)
        SystemLogger.log_event("Op 6 Success: Reservation R001 created.")
    except Exception as e:
        SystemLogger.log_event(f"Op 6 Failed: {e}")

    # OPERATION 7: Process Unconfirmed Reservation (Intentional Error)
    try:
        # Fails because status is "Pending"
        reservation_valid.process_reservation() 
        SystemLogger.log_event("Op 7 Success: Reservation processed.")
    except Exception as e:
        SystemLogger.log_event(f"Op 7 Failed (Handled Exception): {e}")

    # OPERATION 8: Confirm Reservation
    try:
        reservation_valid.confirm_reservation()
        SystemLogger.log_event("Op 8 Success: Reservation status changed to Confirmed.")
    except Exception as e:
        SystemLogger.log_event(f"Op 8 Failed: {e}")

    # OPERATION 9: Process Confirmed Reservation
    try:
        cost = reservation_valid.process_reservation()
        SystemLogger.log_event(f"Op 9 Success: Reservation processed with cost {cost}.")
    except Exception as e:
        SystemLogger.log_event(f"Op 9 Failed: {e}")

    # OPERATION 10: Cancel Reservation
    try:
        reservation_valid.cancel_reservation()
        SystemLogger.log_event("Op 10 Success: Reservation cancelled.")
    except Exception as e:
        SystemLogger.log_event(f"Op 10 Failed: {e}")


    SystemLogger.log_event("=== SYSTEM SHUTDOWN: All operations completed ===")