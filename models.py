
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