import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import Webcam from "react-webcam";

const App = () => {
  const [predictedChar, setPredictedChar] = useState(null); // Store predicted char
  const webcamRef = useRef(null);

  // Set a flag to stop/start streaming
  const [isStreaming, setIsStreaming] = useState(false);

  // Function to capture a single frame from the webcam
  const captureFrame = async () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();

      // Convert base64 image to a blob
      const blob = await fetch(imageSrc).then(res => res.blob());

      const formData = new FormData();
      formData.append("image", blob, "webcam_image.png");

      try {
        // POST the image to the backend
        const response = await axios.post("http://localhost:5001/upload-image", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          }
        });

        // Extract the predicted character from the response
        const { predicted_char } = response.data;
        setPredictedChar(predicted_char);  // Set the predicted character to the state
      } catch (error) {
        console.error("Error uploading the image:", error);
      }
    }
  };

  // Function to continuously capture frames
  const startStreaming = () => {
    setIsStreaming(true);
  };

  const stopStreaming = () => {
    setIsStreaming(false);
  };

  // Effect to handle continuous streaming
  useEffect(() => {
    let intervalId;
    if (isStreaming) {
      intervalId = setInterval(() => {
        captureFrame();  // Capture frames every set interval
      }, 1000);  // Adjust the interval (in milliseconds) as needed
    } else {
      clearInterval(intervalId);
    }

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, [isStreaming]);

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
      {!isStreaming ? (
        <button onClick={startStreaming}>Start Streaming</button>
      ) : (
        <button onClick={stopStreaming}>Stop Streaming</button>
      )}

      {predictedChar && (
        <div>
          <h2>Predicted Character: {predictedChar}</h2>
        </div>
      )}
    </div>
  );
};

export default App;
