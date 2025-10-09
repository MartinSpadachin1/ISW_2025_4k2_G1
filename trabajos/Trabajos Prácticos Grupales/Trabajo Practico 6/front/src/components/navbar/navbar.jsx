import React from "react";
import logo from "../../../public/EHP-Logo.png";
import { Link } from "react-router-dom";
import "../../App.css";

const Navbar = () => {
  const listaItemsNavbar = ["Inicio", "Quiénes Somos", "Comprar Entradas"];
  const listaBotones = ["Registrarse", "Iniciar Sesión"];

  return (
    <nav
      className="navbar navbar-expand-lg fixed-top"
      style={{ backgroundColor: "#134611" }}
    >
      <div className="container-fluid">
        {/* Logo */}
        <Link className="navbar-brand d-flex align-items-center" to="/">
          <img
            src={logo}
            alt="Logo"
            style={{
              height: "8vh",
              objectFit: "contain",
            }}
          />
        </Link>

        {/* Botón hamburguesa (solo visible en pantallas chicas) */}
        <button
          className="navbar-toggler bg-light border-0"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarContenido"
          aria-controls="navbarContenido"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        {/* Contenido */}
        <div className="collapse navbar-collapse" id="navbarContenido">
          {/* Ítems centrados */}
          <ul className="navbar-nav mx-auto mb-2 mb-lg-0">
            {listaItemsNavbar.map((item, index) => (
              <li className="nav-item mx-3" key={index}>
                <Link
                  to={
                    item === "Inicio"
                      ? "/"
                      : item === "Quiénes Somos"
                      ? "/quienes-somos" : item === "Comprar Entradas" ? '/comprar-entradas'
                      : "#"
                  }
                  className="nav-link text-white"
                  style={{
                    textDecoration: "none",
                    fontWeight: 500,
                    fontSize: "1.05rem",
                  }}
                >
                  {item}
                </Link>
              </li>
            ))}
          </ul>

          {/* Botones responsive */}
          <div className="d-flex align-items-center gap-2 flex-wrap">
            {listaBotones.map((boton, index) => (
              <Link
                key={index}
                to={
                  boton === "Registrarse"
                    ? "/registrarse"
                    : boton === "Iniciar Sesión"
                    ? "/iniciar-sesion"
                    : "#"
                }
                className="btn btn-success text-white fw-semibold px-3 py-2"
                style={{
                  border: "none",
                  fontSize: "0.95rem",
                  transition: "all 0.2s ease-in-out",
                }}
              >
                {boton}
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Responsive behavior con CSS adicional */}
      <style>{`
        @media (max-width: 992px) {
          .navbar-nav {
            text-align: center;
          }
          .btn {
            width: 100%;
            font-size: 1rem;
          }
        }
        @media (max-width: 1200px) {
          .btn {
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
          }
          .nav-link {
            font-size: 1rem;
          }
        }
      `}</style>
    </nav>
  );
};

export default Navbar;
