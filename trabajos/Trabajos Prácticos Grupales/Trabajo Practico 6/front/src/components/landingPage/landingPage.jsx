import React from "react";
import ContentCard from "../ContentCard/ContentCard";
import parquePromocionalUno from "../../assets/parquePromocionalUno.jpg";
import parquePromocionalDos from "../../assets/parquePromocionalDos.jpg";
import parquePromocionalTres from "../../assets/parquePromocionalTres.jpg";
import "../../App.css";

export default function LandingPage() {
  // Lista de imágenes + descripciones
  const imagenes = [
    {
      src: parquePromocionalUno,
      alt: "Vista panorámica del parque ecológico",
      captionTitle: "Naturaleza en equilibrio",
      captionText: "Descubrí espacios verdes diseñados para cuidar el planeta.",
    },
    {
      src: parquePromocionalDos,
      alt: "Senderos naturales entre árboles",
      captionTitle: "Explorá y conectá",
      captionText: "Caminos y actividades que promueven la conexión con la naturaleza.",
    },
    {
      src: parquePromocionalTres,
      alt: "Área recreativa del EcoHarmony Park",
      captionTitle: "Diversión sustentable",
      captionText: "Disfrutá de experiencias únicas en armonía con el medio ambiente.",
    },
  ];

  return (
    <div
      className="container-fluid py-5"
      style={{ minHeight: "90vh", marginTop: "10vh" }}
    >

      <h1 className=" text-center " style={{ marginTop: '5vh' }} >Qué podrás encontrar en nuestro Ecoparque...</h1>

      <div className="row align-items-center" style={{ marginBottom: '10vh' }}> {/* Éste es el CONTENEDOR de ambas columnas... */}
        {/* Columna izquierda: Card descriptiva */}
        <div className="col-lg-4 col-md-12 mb-4 mb-lg-0">
          <ContentCard
            title="Bienvenido a EcoHarmony Park"
            text="Explorá la naturaleza en equilibrio. Conectate con un espacio sustentable donde cada rincón está diseñado para el bienestar del planeta y sus visitantes."
          />
        </div>

        {/* Columna derecha: Carrusel */}
        <div className="col-lg-8 col-md-12">
          <div
            id="promocionalCarousel"
            className="carousel slide"
            data-bs-ride="carousel"
            style={{ marginTop: '10vh', marginRight: '5vw' }}
          >
            <div className="carousel-inner rounded shadow">
              {imagenes.map((img, index) => (
                <div
                  key={index}
                  className={`carousel-item ${index === 0 ? "active" : ""}`}
                >
                  <img
                    src={img.src}
                    className="d-block w-100 img-fluid"
                    alt={img.alt}
                    style={{
                      maxHeight: "60vh",
                      objectFit: "cover",
                      borderRadius: "20px",
                    }}
                  />
                  <div className="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-2">
                    <h5 className="fw-bold text-white">{img.captionTitle}</h5>
                    <p className="text-white">{img.captionText}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* Controles del carrusel */}
            <button
              className="carousel-control-prev"
              type="button"
              data-bs-target="#promocionalCarousel"
              data-bs-slide="prev"
            >
              <span
                className="carousel-control-prev-icon"
                aria-hidden="true"
              ></span>
              <span className="visually-hidden">Anterior</span>
            </button>
            <button
              className="carousel-control-next"
              type="button"
              data-bs-target="#promocionalCarousel"
              data-bs-slide="next"
            >
              <span
                className="carousel-control-next-icon"
                aria-hidden="true"
              ></span>
              <span className="visually-hidden">Siguiente</span>
            </button>
          </div>
        </div>
      </div>

    </div>
  );
}
