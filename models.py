
# Iniciamos la clase Client con los atributos privados client_id, name y email.
class Client:
    # Colocamos el constructor de la clase, el cual recibe los parámetros client_id, name y email y son privados.
    def __init__(self, client_id: str, name: str, email: str):
        self.__client_id = client_id
        self.__name = name
        self.set_email(email)

    # Obtiene el ID del cliente.
    def get_client_id(self) -> str:
        """Returns the client's ID."""
        return self.__client_id

    # Obtiene el nombre del cliente.
    def get_name(self) -> str:
        """Returns the client's name."""
        return self.__name

    # Obtiene el email del cliente.
    def get_email(self) -> str:
        """Returns the client's email."""
        return self.__email

    # Establece y verifica que sea correcto el email del cliente.
    def set_email(self, new_email: str) -> None:
        if '@' not in new_email:
            raise ValueError("Invalid email format: missing '@' symbol.")
        self.__email = new_email    

# Inicializamos la clase Service.
class Service:
    # Constructor de la clase Service.
    def __init__(self, service_id: str, client_name: str):
        self._service_id = service_id
        self._client_name = client_name  
        self._status = "Pending"
             
    # Obtiene el ID del servicio.
    def calculate_cost(self) -> float:
        return 0.0
    
    # Describe el servicio.
    def describe_service(self) -> str:
        return "Generic Service Description"
    
# Inicializamos la clase RoomRental, la cual hereda de Service.
class RoomRental(Service):
    # Definimos lo que usaremos.
    def __init__(self, service_id: str, client_name: str, hours: int, rate_per_hour: float):
         super().__init__(service_id, client_name)
         self._hours = hours
         self._rate_per_hour = rate_per_hour
         
    # Calcula el costo del servicio de alquiler de sala.
    def calculate_cost(self) -> float:
        return self._hours * self._rate_per_hour

    # Describe el servicio de alquiler de sala.
    def describe_service(self) -> str:
        return f"Room Rental for {self._client_name} - {self._hours} hours."
    
# Inicializamos la clase EquipmentRental, la cual hereda de Service.
class EquipmentRental(Service):
    # Definimos lo que usaremos.
    def __init__(self, service_id: str, client_name: str, days: int, daily_rate: float):
            super().__init__(service_id, client_name)
            self._days = days
            self._daily_rate = daily_rate
            
    # Calcula el costo del servicio de alquiler de equipo.
    def calculate_cost(self) -> float:
            return self._days * self._daily_rate
        
    # Describe el servicio de alquiler de equipo.
    def describe_service(self) -> str:
            return f"Equipment Rental for {self._client_name} - {self._days} days."

# Inicializamos la clase Consulting, la cual hereda de Service.
class Consulting(Service):
    def __init__(self, service_id: str, client_name: str, sessions: int, fee_per_session: float):
        super().__init__(service_id, client_name)
        self._sessions = sessions
        self._fee_per_session = fee_per_session
        
    # Calcula el costo del servicio de consultoría, aplicando un descuento opcional.
    def calculate_cost(self, discount_percentage: float = 0.0) -> float:
        base_cost = self._sessions * self._fee_per_session
        deduction = base_cost * (discount_percentage / 100)
        return base_cost - deduction
    
    # Describe el servicio de consultoría.  
    def describe_service(self) -> str:
            return f"Consulting for {self._client_name} - {self._sessions} sessions."
        
# Creamos la clase Reserva.
class Reservation:
    
    # Usamos el constructor de la clase, el cual recibe los parámetros reservation_id, client, service y duration. Además, se establece un estado inicial de "Pending".
    def __init__(self, reservation_id: str, client: Client, service: Service, duration: int):
        self._reservation_id = reservation_id
        self._client = client
        self._service = service
        self._duration = duration
        self._status = "Pending"  # Initial state
    
    # Define el método para confirmar la reserva, el cual cambia el estado a "Confirmed" y muestra un mensaje de confirmación.
    def confirm_reservation(self) -> None:
        self._status = "Confirmed"
        print(f"Reservation {self._reservation_id} confirmed for {self._client.get_name()}.")
    
    # Define el método para cancelar la reserva, el cual cambia el estado a "Cancelled" y muestra un mensaje de cancelación.
    def cancel_reservation(self) -> None:
        self._status = "Cancelled"
        print(f"Reservation {self._reservation_id} has been cancelled.")

    # Define el método para procesar la reserva, el cual verifica si el estado es "Confirmed" y, de ser así, calcula el costo del servicio utilizando el método calculate_cost() del servicio asociado. Si la reserva no está confirmada, se lanza un error. 
    def process_reservation(self) -> float:
        if self._status == "Confirmed":
            return self._service.calculate_cost()
        else:
            raise ValueError("Cannot process a non-confirmed reservation.")