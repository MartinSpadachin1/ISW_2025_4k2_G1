import React from "react";
import LogoUTN from "../../assets/logo-utn-frc.png";

function Footer() {
  return (
    <footer
      className="bg-success text-white"
      style={{
        margin: 0,
        width: "100vw", // Ancho total del viewport
        padding: "1rem 0", // Padding vertical para que no quede pegado
        fontFamily: "Montserrat",
        fontSize: "1rem",
        boxSizing: "border-box", // Para que el padding no aumente el ancho
      }}
    >
      {/* Usamos container-fluid para ocupar todo el ancho */}
      <div className="container-fluid text-center py-3">
        <img
          src={LogoUTN}
          alt="logo-utn-blanco"
          style={{
            maxHeight: "10vh",
            marginBottom: "1rem",
          }}
        />
        <p className="mb-0">
          Elaborado por los alumnos del <strong>Grupo 1</strong> de la <strong>Comisión 4k2</strong>
          <br />
          <strong>UTN-FRC</strong> — Materia: <em>Ingeniería y Calidad de Software</em>
        </p>
      </div>
    </footer>
  );
}

export default Footer;