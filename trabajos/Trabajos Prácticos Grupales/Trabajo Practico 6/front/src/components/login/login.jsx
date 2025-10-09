import React from "react";

export default function Login() {
  return (
    <div className="container-fluid d-flex align-items-center justify-content-center min-vh-100">
      <div className="row w-100" style={{ maxWidth: "900px" }}>
        {/* Columna del formulario */}
        <div className="col-12 col-md-6">
          <div
            className="card shadow"
            style={{
              borderRadius: "1rem",
            }}
          >
            <div className="card-body p-4">
              <h3 className="card-title text-center mb-4">Iniciar Sesión</h3>

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
        </div>

        {/* Columna de la imagen */}
        <div className="col-12 col-md-6 d-none d-md-flex align-items-center justify-content-center">
          <img
            src="https://via.placeholder.com/400x500?text=Imagen+Login" // Reemplaza con tu imagen real
            alt="Login illustration"
            className="img-fluid"
            style={{ maxHeight: "80vh", objectFit: "cover" }}
          />
        </div>
      </div>
    </div>
  );
}