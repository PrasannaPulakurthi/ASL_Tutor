import React, { useState, useRef } from "react";
import axios from "axios";
import Webcam from "react-webcam";

const App = () => {
  const [greyscaleImage, setGreyscaleImage] = useState(null);
  const webcamRef = useRef(null);

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();

    // Convert base64 image to a blob
    const blob = await fetch(imageSrc).then(res => res.blob());

    const formData = new FormData();
    formData.append("image", blob, "webcam_image.png");

    try {
      const response = await axios.post("http://localhost:5001/upload-image", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        responseType: "blob", // Expecting binary data (image) as response
      });

      const imageBlob = URL.createObjectURL(response.data);
      setGreyscaleImage(imageBlob);
    } catch (error) {
      console.error("Error uploading the image:", error);
    }
  };

  return (
    <div>
      <h1>Capture Image from Webcam</h1>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/png"
        width={640}
        height={480}
      />
      <button onClick={capture}>Capture and Convert</button>

      {greyscaleImage && (
        <div>
          <h2>Greyscale Image</h2>
          <img src={greyscaleImage} alt="Greyscale" />
        </div>
      )}
    </div>
  );
};

export default App;
