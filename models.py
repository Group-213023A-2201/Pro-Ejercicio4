

from abc import ABC, abstractmethod
import random

#Validación de seguridad 
class InvalidDurationError(ValueError):
  
    pass
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
        pass


    # ESTOS SON MIS PRIMEROS APORTES
 

# Clase cliente con encapsulamiento para proteccion de los datos
class Client:
    def __init__(self, client_id, name, email):
        self.__client_id = client_id
        self.__name = name  
        self.__email = email
# Método para que Reserva pueda obtener el nombre
    def get_name(self): 
        return self.__name

    def show_details(self):
        return f"Client: {self.__name} (ID: {self.__client_id})"

# Aqui  se crea la clase abstracta servicio que nos pide la tarea 4 donde utilizamos el polimorfismo para calcular costos de cada servicio, validaciones y descripciones.
class Service(ABC):
    def __init__(self, service_name: str, base_cost: float):
        self.service_name = service_name
        self.base_cost = base_cost
#cada clase tiene su propia forma de calcular su costo esto es polimorfismo
    #Métodos sobrecargados (por ejemplo, diferentes variantes del 
#cálculo de costos con impuestos, descuentos o parámetros 
#opcionales). 
    @abstractmethod
    def calculate_cost(self, quantity: int, tax: float = 0.0, discount: float = 0.0) -> float:
     pass

    @abstractmethod
    def describe_service(self) -> str:
        pass 
#Con este método se lanzan excepciones si los datos estan mal
    @abstractmethod
    def validate_parameter(self, quantity: int):
                pass

 # Tres servicios o clases hijas especializados que hereden de ella osea de la clase Servicio, implementando polimorfismo y métodos sobrescritos para calcular costos, describir servicios y 
#validar parámetros. 
# Las tres clases usan super()__init__ para heredar nombre y costo base de la clase servicio.
class RoomBooking(Service):
    def __init__(self, service_name, base_cost):
        super().__init__(service_name, base_cost)

    def validate_parameter(self, hours):
        if hours <= 0: 
            raise InvalidDurationError("Hours must be a positive value.")
 #Métodos sobrecargados (por ejemplo, diferentes variantes del 
#cálculo de costos con impuestos, descuentos o parámetros 
#opcionales).
    def calculate_cost(self, hours: int, tax: float = 0.0, discount: float = 0.0) -> float:
        self.validate_parameter(hours)
        subtotal = self.base_cost * hours
        
        # Aplicamos la sobrecarga (si el usuario manda impuestos o descuentos)
        total = subtotal + (subtotal * tax) - (subtotal * discount)
        return total
    
    def describe_service(self) -> str:
        return f"Room Booking: {self.service_name}"
        
class EquipmentRental(Service):
    def __init__(self, service_name: str, base_cost: float):
        super().__init__(service_name, base_cost)

    def validate_parameter(self, days):
        if days <= 0: 
            raise InvalidDurationError("Days must be a positive value.")

    def calculate_cost(self, days):
        self.validate_parameter(days)
        return self.base_cost * days

    def describe_service(self) -> str:
        return f"Equipment Rental: {self.service_name}"
            
class Consulting(Service):
    def __init__(self, service_name: str, base_cost: float):
        super().__init__(service_name, base_cost)

    def validate_parameter(self, sessions):
        if sessions <= 0: 
            raise InvalidDurationError("Sessions must be a positive value.")

    def calculate_cost(self, sessions):
        self.validate_parameter(sessions)
        total = self.base_cost * sessions
        if sessions >= 10:
            total *= 0.70  # 30% descuento
        return total

    def describe_service(self) -> str:
        return f"Consulting Service: {self.service_name}"
# Clase reserva con manejo de excepciones usando try para intentar procesar la reserva
class Booking:
    def __init__(self, client, service, duration):
        self.client = client
        self.service = service
        self.duration = duration
        self.status = "PENDING"

    def confirm(self):
        try:
            print(f"Processing booking for {self.client.get_name()}...")
            total = self.service.calculate_cost(self.duration)
            print(f"Service: {self.service.describe_service()}")
            print(f"Total Amount: ${total:.2f}")
            self.status = "CONFIRMED"

        except InvalidDurationError as e:
            print(f"Validation Error: {e}")
            self.status = "CANCELLED DUE TO ERROR"
        except Exception as e:
            print(f"Unexpected Error: {e}")
            self.status = "SYSTEM ERROR"
        finally:
            print(f"Final Status: {self.status}\n")


