import React from "react";
import personaUno from "../../../assets/personaUno.png";

function ContentCardImage() {
  return (
    <div className="text-center mb-3">
      <img
        src={personaUno}
        alt="Persona promocional"
        style={{
          width: "90%",
          maxWidth: "250px",
          height: "auto",
          borderRadius: "15px",
          objectFit: "cover",
        }}
      />
    </div>
  );
}

export default ContentCardImage;
