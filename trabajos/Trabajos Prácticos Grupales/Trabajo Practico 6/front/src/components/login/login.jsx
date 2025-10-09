// Login.jsx
import React from "react";
import Claudia from '../../assets/claudia.png';

export default function Login() {
  return (
    <div
      className="w-100 d-flex align-items-center justify-content-center p-3 p-md-4"
      style={{
        minHeight: '100vh',
        paddingTop: '80px',    // ≈ altura del navbar
        paddingBottom: '80px', // ≈ altura del footer
        boxSizing: 'border-box',
      }}
    >
      {/* Contenedor principal: 1/3 imagen + 2/3 formulario en desktop */}
      <div className="row w-100 g-0" style={{ maxWidth: '1200px' }}>
        {/* Imagen: 12/12 en móvil (oculta), 4/12 en desktop */}
        <div className="col-12 col-md-4 d-none d-md-flex">
          <img
            src={Claudia}
            alt="Claudia la leona en el parque"
            className="w-100 h-100"
            style={{
              objectFit: 'cover',
              maxHeight: '80vh',
              borderRadius: '12px 0 0 12px',
            }}
          />
        </div>

        {/* Formulario: 12/12 en móvil, 8/12 en desktop */}
        <div className="col-12 col-md-8 d-flex">
          <div
            className="card shadow w-100 border-0 rounded-3"
            style={{ backgroundColor: 'white' }}
          >
            <div className="card-body p-4 p-md-5 d-flex flex-column">
              <h3 className="card-title text-center mb-4">Iniciar Sesión</h3>

              <div className="mb-3">
                <label htmlFor="email" className="form-label">Email</label>
                <input
                  type="email"
                  id="email"
                  className="form-control"
                  placeholder="Ingresá tu email"
                />
              </div>

              <div className="mb-3">
                <label htmlFor="password" className="form-label">Contraseña</label>
                <input
                  type="password"
                  id="password"
                  className="form-control"
                  placeholder="Ingresá tu contraseña"
                />
              </div>

              <div className="text-center mb-3 mt-auto">
                <small>
                  <a href="#" className="text-decoration-none">Registrarse</a>
                </small>
              </div>

              <div className="d-flex justify-content-between">
                <button className="btn btn-secondary">Cancelar</button>
                <button className="btn btn-primary">Ingresar</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}