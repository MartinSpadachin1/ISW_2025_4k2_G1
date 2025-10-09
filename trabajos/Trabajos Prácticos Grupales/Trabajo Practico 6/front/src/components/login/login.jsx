import React from "react";

export default function Login() {
  return (

      <div
        className="card shadow d-flex justify-content-center align-items-center"
        style={{
          width: "30vw",
          minWidth: "20rem",
          borderRadius: "1rem",
        }}
      >
        <div className="card-body">
           <div>
          <h3 className="card-title text-center mt-1 mb-4">Iniciar Sesión</h3>
            </div>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Email
            </label>
            <input
              type="email"
              id="email"
              className="form-control"
              placeholder="Ingresá tu email"
            />
          </div>

          <div className="mb-3">
            <label htmlFor="password" className="form-label">
              Contraseña
            </label>
            <input
              type="password"
              id="password"
              className="form-control"
              placeholder="Ingresá tu contraseña"
            />
          </div>

          <div className="text-center mb-3">
            <small>
              <a href="#" className="text-decoration-none">
                Registrarse
              </a>
            </small>
          </div>

          <div className="d-flex justify-content-between">
            <button className="btn btn-secondary">Cancelar</button>
            <button className="btn btn-primary">Ingresar</button>
          </div>
        </div>
      </div>

);
}
