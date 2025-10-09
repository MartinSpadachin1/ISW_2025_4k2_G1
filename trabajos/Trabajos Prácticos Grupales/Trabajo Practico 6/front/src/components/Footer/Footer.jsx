import React from "react";
import LogoUTN from "../../assets/logo-utn-frc.png"

function Footer() {
  return (
    <footer
      style={{
        backgroundColor: "#3da35d",
        color: "white",
        width: "100%",
        padding: 0,
        margin: 0
      }}
    >
      <div
        className="container text-center py-4"
        style={{
          fontFamily: "Montserrat",
          fontSize: "1rem",
        }}
      >
        <img src={LogoUTN} alt="logo-utn-blanco" style={{ marginTop: '3vh', marginBottom: '3vh',maxHeight: '10vh' }}/>
        <p className="mb-0">
          Elaborado por los alumnos del <strong>Grupo 1</strong> de la <strong>Comisión 4k2</strong><br />
          <strong>UTN-FRC</strong> — Materia: <em>Ingeniería y Calidad de Software</em>
        </p>
      </div>
    </footer>
  );
}

export default Footer;
