import axios from "axios";
import React, { useEffect, useRef, useState } from "react";
import CountUp from "react-countup";
import { FaCheck, FaSpinner, FaUpload } from "react-icons/fa";
import Webcam from "react-webcam";
import "./App.css";

interface HistoryItem {
  image: string;
  age: number;
  confidence: number;
}

const App: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [predictedAge, setPredictedAge] = useState<number | null>(null);
  const [confidence, setConfidence] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<HistoryItem[]>([]);

  const inputRef = useRef<HTMLInputElement | null>(null);
  const webcamRef = useRef<Webcam>(null);

  // Load history from localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem("predictionHistory");
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory));
    }
  }, []);

  const handleImageChange = (file: File) => {
    setSelectedImage(file);
    setPreview(URL.createObjectURL(file));
    setPredictedAge(null);
    setConfidence(null);
  };

  // Capture from webcam
  const captureFromWebcam = () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        fetch(imageSrc)
          .then((res) => res.blob())
          .then((blob) => {
            const file = new File([blob], "webcam.png", { type: "image/png" });
            handleImageChange(file);
          });
      }
    }
  };

  // Predict age via backend
  const handlePredict = async () => {
    if (!selectedImage) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("image", selectedImage);

    try {
      const response = await axios.post("http://localhost:5000/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const age = response.data.age;
      setPredictedAge(age);

      // Simulated confidence
      const conf = Math.floor(Math.random() * 20 + 80);
      setConfidence(conf);

      // Save history
      const newEntry = { image: preview!, age, confidence: conf };
      const updatedHistory = [newEntry, ...history];
      setHistory(updatedHistory);
      localStorage.setItem("predictionHistory", JSON.stringify(updatedHistory));
    } catch (error) {
      console.error(error);
      alert("Failed to predict age.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">Age Prediction App</h1>

      <div className="app-content">
        {/* Upload / Webcam */}
        {!preview && (
          <div className="upload-webcam-container">
            <label className="upload-card" onClick={() => inputRef.current?.click()}>
              <FaUpload className="upload-icon" />
              <span>Click or Drag & Drop to Upload Image</span>
              <input
                type="file"
                accept="image/*"
                ref={inputRef}
                onChange={(e) => e.target.files && handleImageChange(e.target.files[0])}
              />
            </label>

            <div className="webcam-container">
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/png"
                width={256}
                height={256}
                className="webcam-feed"
              />
              <button onClick={captureFromWebcam} className="predict-btn">
                Capture Photo
              </button>
            </div>
          </div>
        )}

        {/* Image Preview */}
        {preview && (
          <div className="image-preview">
            <img src={preview} alt="Preview" />
          </div>
        )}

        {/* Predict Button */}
        <button
          onClick={handlePredict}
          disabled={!selectedImage || loading}
          className="predict-btn"
        >
          {loading ? <FaSpinner className="spinner" /> : "Predict Age"}
        </button>

        {/* Predicted Age */}
        {predictedAge !== null && (
          <div className="predicted-age">
            <FaCheck className="check-icon" />
            Predicted Age: <CountUp end={predictedAge} duration={1.5} />
            {confidence && <span className="confidence">Confidence: {confidence}%</span>}
          </div>
        )}

        {/* History Panel */}
        {history.length > 0 && (
          <div className="history-panel">
            <h2>Prediction History</h2>
            <div className="history-grid">
              {history.map((item, idx) => (
                <div className="history-card" key={idx}>
                  <img src={item.image} alt={`History ${idx}`} />
                  <p>Age: {item.age}</p>
                  <p>Confidence: {item.confidence}%</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
