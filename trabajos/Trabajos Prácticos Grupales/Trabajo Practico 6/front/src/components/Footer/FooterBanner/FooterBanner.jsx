import React from "react";
import footerUpperBanner from "../../../assets/footer-upper-banner.png";

function FooterBanner() {
  return (
    <div style={{
      width: "100%",
      margin: 0,
      padding: 0,
      overflow: "hidden",
    }}>
      <img
        src={footerUpperBanner}
        alt="Banner superior del footer"
        style={{
          width: "100vw",
          maxHeight: "30vh", // Limita el alto máximo para que no se vea gigante
          objectFit: "contain", // Muestra la imagen completa sin recortes
          display: "block",
          margin: "0 auto", // Centra la imagen horizontalmente
          padding: 0,
        }}
      />
    </div>
  );
}

export default FooterBanner;
