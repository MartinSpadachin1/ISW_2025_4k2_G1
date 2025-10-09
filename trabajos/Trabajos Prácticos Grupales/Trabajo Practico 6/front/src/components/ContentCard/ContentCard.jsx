import React from "react";
import ContentCardImage from "./ContentCardImage/ContentCardImage";

function ContentCard({ title, text }) {
  return (
    <div
      className="p-4 d-flex flex-column align-items-center text-white"
      style={{
        marginLeft: '5vw',
        marginTop: '10vh',
        backgroundColor: "#3da35d",
        borderRadius: "20px",
        height: "100%",
        minWidth:'20vw',
        minHeight: "60vh",
        textAlign: "center",
      }}
    >
      {/* Imagen arriba */}
      <ContentCardImage />

      {/* Título */}
      <h2 className="fw-bold mb-3">{title}</h2>

      {/* Descripción */}
      <p style={{ fontSize: "1.1rem", lineHeight: "1.6", maxWidth: "80%" }}>
        {text}
      </p>
    </div>
  );
}

export default ContentCard;
