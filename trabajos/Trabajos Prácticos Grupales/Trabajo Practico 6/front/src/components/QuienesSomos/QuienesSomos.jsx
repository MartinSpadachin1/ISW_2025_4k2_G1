// QuienesSomos.jsx
import React from "react";
import Grupito from '../../assets/grupo1.png';

export default function QuienesSomos() {
  const integrantes = [
    "Lerchundi Agustina - 90105",
    "Bustos Joaquin - 94914",
    "Castoldi Thiago Martin - 94986",
    "Noto Claudia Carina - 95215",
    "Romero Moreno Oscar Alfonso - 96454",
    "Spadachini Martin Matias - 95168",
    "Sadir Emilio - 96622",
    "Petrich Ernesto Joaquin - 90431",
    "Filippa Franco Julian - 92191",
    "Recalde Franco - 94661"
  ];

  return (
    <div
      className="w-100 d-flex align-items-center justify-content-center px-3 px-md-4"
      style={{
        minHeight: '100vh',
        paddingTop: '80px',    // Compensa navbar
        paddingBottom: '80px', // Compensa footer
        boxSizing: 'border-box',
      }}
    >
      <div className="row w-100 g-0" style={{ maxWidth: '1200px' }}>
        {/* Imagen: solo en desktop */}
        <div className="col-12 col-md-4 d-none d-md-flex">
          <img
            src={Grupito}
            alt="Grupo 1 - UTN FRC"
            className="w-100 h-100"
            style={{
              objectFit: 'cover',
              maxHeight: '80vh',
              borderRadius: '12px 0 0 12px',
            }}
          />
        </div>

        {/* Contenido: responsive en todo */}
        <div className="col-12 col-md-8 d-flex">
          <div
            className="card shadow w-100 border-0 rounded-3"
            style={{ backgroundColor: 'white' }}
          >
            <div className="card-body p-4 p-md-5">
              <h2
                className="card-title text-center mb-4"
                style={{ color: '#3da35d', marginTop: '0.5rem' }} // 👈 marginTop suave
              >
                ¿Quiénes Somos?
              </h2>

              <p className="mb-4 text-muted">
                Somos estudiantes de la carrera <strong>Ingeniería en Sistemas de Información</strong>, 
                pertenecientes al <strong>Grupo 1</strong> de la <strong>Comisión 4k2</strong>, 
                de la <strong>Universidad Tecnológica Nacional - Facultad Regional Córdoba (UTN-FRC)</strong>.
              </p>

              <p className="mb-4">
                Este proyecto forma parte de la materia <em><strong>Ingeniería y Calidad de Software</strong></em>, 
                donde aplicamos conocimientos de desarrollo ágil, testing, diseño responsivo y buenas prácticas 
                para crear una experiencia digital amigable y funcional para el <strong>EcoHarmony Park</strong>.
              </p>

              <h5 className="mb-3 fw-bold" style={{ color: '#134611' }}>
                Integrantes del Grupo:
              </h5>
              <div className="row">
                {integrantes.map((integrante, index) => (
                  <div className="col-12 col-md-6 mb-2" key={index}>
                    • {integrante}
                  </div>
                ))}
              </div>

              <div className="text-center mt-4 pt-2 border-top">
                <small className="text-muted">
                  UTN-FRC • Ingeniería y Calidad de Software • 2025
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}