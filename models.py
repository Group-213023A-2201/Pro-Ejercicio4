
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
         
    def calculate_cost(self) -> float:
        return self._hours * self._rate_per_hour        

    def describe_service(self) -> str:
        return f"Room Rental for {self._client_name} - {self._hours} hours."
    
class EquipmentRental(Service):
    def __init__(self, service_id: str, client_name: str, days: int, daily_rate: float):
            super().__init__(service_id, client_name)
            self._days = days
            self._daily_rate = daily_rate
    def calculate_cost(self) -> float:
            return self._days * self._daily_rate
    def describe_service(self) -> str:
            return f"Equipment Rental for {self._client_name} - {self._days} days."

class Consulting(Service):
    def __init__(self, service_id: str, client_name: str, sessions: int, fee_per_session: float):
        super().__init__(service_id, client_name)
        self._sessions = sessions
        self._fee_per_session = fee_per_session
    
    def calculate_cost(self, discount_percentage: float = 0.0) -> float:
        base_cost = self._sessions * self._fee_per_session
        deduction = base_cost * (discount_percentage / 100)
        return base_cost - deduction
       
    def describe_service(self) -> str:
            return f"Consulting for {self._client_name} - {self._sessions} sessions."

   