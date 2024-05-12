function iniciarSesion() {
  console.log("Iniciaste sesion :DDDD");
}

function obtenerDatosUsuario() {
  fetch("http://127.0.0.1:8000/obtenerDatos/")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Hubo un problema al realizar la solicitud.");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
