// Registrar.jsx
import React, { useState } from "react";
import Elefanta from '../../assets/elefanta.png';
import { Link, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { useToast } from '../common/ToastContext';

export default function Registrar() {
  const navigate = useNavigate();
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const toast = useToast();
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
        {/* Imagen: solo en desktop */}
        <div className="col-12 col-md-4 d-none d-md-flex">
          <img
            src={Elefanta}
            alt="Claudia la leona en el parque"
            className="w-100 h-100"
            style={{
              objectFit: 'cover',
              maxHeight: '80vh',
              borderRadius: '12px 0 0 12px',
            }}
          />
        </div>

        {/* Formulario de registro */}
        <div className="col-12 col-md-8 d-flex">
          <div
            className="card shadow w-100 border-0 rounded-3"
            style={{ backgroundColor: 'white' }}
          >
            <div className="card-body p-4 p-md-5 d-flex flex-column">
              <h3 className="card-title text-center mb-4">Registrarse</h3>

              {/* Campo Nombre */}
              <div className="mb-3">
                <label htmlFor="nombre" className="form-label">Nombre</label>
                <input
                  type="text"
                  id="nombre"
                  className="form-control"
                  placeholder="Ingresá tu nombre"
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                />
              </div>

              {/* Campo Email */}
              <div className="mb-3">
                <label htmlFor="email" className="form-label">Email</label>
                <input
                  type="email"
                  id="email"
                  className="form-control"
                  placeholder="Ingresá tu email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              {/* Campo Contraseña */}
              <div className="mb-3">
                <label htmlFor="password" className="form-label">Contraseña</label>
                <div style={{ position: 'relative' }}>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    id="password"
                    className="form-control"
                    placeholder="Ingresá tu contraseña"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{ paddingRight: '70px' }}
                  />
                  <span
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      position: 'absolute',
                      right: '15px',
                      top: '50%',
                      transform: 'translateY(-50%)',
                      fontSize: '0.9rem',
                      color: '#3da35d',
                      fontWeight: 600,
                      cursor: 'pointer',
                      userSelect: 'none',
                      background: 'white',
                      paddingLeft: '4px',
                    }}
                  >
                    {showPassword ? 'Ocultar' : 'Mostrar'}
                  </span>
                </div>
              </div>

              {error && <div className="alert alert-danger">{error}</div>}

              {/* Texto + enlace a Iniciar Sesión */}
              <div className="text-center mb-3 mt-auto">
                <p className="mb-1" style={{ fontSize: '0.95rem', color: '#555' }}>
                  ¿Ya tenés una cuenta?
                </p>
                <small>
                  <Link to="/iniciar-sesion" className="text-decoration-none fw-semibold" style={{ color: '#3da35d' }}>
                    Iniciar Sesión
                  </Link>
                </small>
              </div>

              <div className="d-flex justify-content-between">
                <button className="btn btn-secondary" onClick={() => { setNombre(''); setEmail(''); setPassword(''); setError(null); }}>Cancelar</button>
                <button className="btn btn-success" onClick={async () => {
                  setError(null);
                  setLoading(true);
                  try {
                    await api.register(nombre, email, password);
                    toast.show('Registro exitoso. Ya podés iniciar sesión.');
                    navigate('/iniciar-sesion');
                  } catch (err) {
                    setError(err.detail || err.message || 'Error al registrarse');
                  } finally { setLoading(false); }
                }} disabled={loading}>{loading ? 'Registrando...' : 'Registrarse'}</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}