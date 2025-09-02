import React, { useRef, useState } from "react";
import Webcam from "react-webcam";

// History Interface
interface HistoryItem {
  id: number;
  image: string;
  predictedAge: number;
  uploadedAt: string;
}

const Home: React.FC = () => {
  const [preview, setPreview] = useState<string | null>(null);
  const [mode, setMode] = useState<"upload" | "webcam">("upload"); // default to upload
  const [startWebcam, setStartWebcam] = useState(false);
  const [dragging, setDragging] = useState(false);
  const webcamRef = useRef<Webcam>(null);

  // File Upload
  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      setPreview(URL.createObjectURL(e.target.files[0]));
    }
  };

  // Drag & Drop
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragging(false);
    if (e.dataTransfer.files?.[0]) {
      setPreview(URL.createObjectURL(e.dataTransfer.files[0]));
    }
  };

  // Webcam Capture
  const captureFromWebcam = () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      setPreview(imageSrc);
      setStartWebcam(false); // Stop webcam, but stay in webcam mode
    }
  };

  // Predict Age (placeholder for ML model)
  const predictAgeFromModel = async (image: string): Promise<number> => {
    return 25; // temporary placeholder
  };

  // Handle Predict
  const handlePredict = async () => {
    if (!preview) return;

    const predictedAge = await predictAgeFromModel(preview);

    // Save history to localStorage
    const savedHistory = localStorage.getItem("predictionHistory");
    const history: HistoryItem[] = savedHistory ? JSON.parse(savedHistory) : [];
    const newItem: HistoryItem = {
      id: history.length + 1,
      image: preview,
      predictedAge,
      uploadedAt: new Date().toISOString(),
    };
    localStorage.setItem(
      "predictionHistory",
      JSON.stringify([newItem, ...history])
    );

    setPreview(null);
    alert(`Predicted Age: ${predictedAge}`);
  };

  return (
    <div className="p-6">
      {/* Webcam / Upload Buttons */}
      <div className="flex justify-center gap-6 mb-8">
        <button
          onClick={() => {
            setMode("upload");
            setPreview(null);
          }}
          className={`px-6 py-2 rounded-lg shadow transition ${
            mode === "upload" ? "bg-teal-600 text-white" : "bg-gray-200"
          }`}
        >
          Upload Image
        </button>

        <button
          onClick={() => {
            setMode("webcam");
            setPreview(null);
            setStartWebcam(false);
          }}
          className={`px-6 py-2 rounded-lg shadow transition ${
            mode === "webcam" ? "bg-teal-600 text-white" : "bg-gray-200"
          }`}
        >
          Use Webcam
        </button>
      </div>

      {/* Upload Section */}
      {mode === "upload" && !preview && (
        <div className="bg-white shadow-lg rounded-2xl p-10 border max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold mb-6 text-teal-700">
            Upload an Image
          </h2>
          <div
            onDragOver={(e) => {
              e.preventDefault();
              setDragging(true);
            }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-lg p-10 text-center cursor-pointer transition ${
              dragging ? "border-teal-600 bg-teal-50" : "border-gray-300"
            }`}
          >
            <p className="text-gray-600 text-lg">Drag & Drop an image here</p>
            <p className="text-gray-400 text-sm">or</p>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
              id="fileUpload"
            />
            <label
              htmlFor="fileUpload"
              className="mt-4 inline-block bg-teal-600 text-white py-3 px-6 rounded-lg hover:bg-teal-700 transition cursor-pointer text-lg"
            >
              Browse Files
            </label>
          </div>
        </div>
      )}

      {/* Show Preview in Upload Mode */}
      {mode === "upload" && preview && (
        <div className="bg-white shadow-lg rounded-2xl p-10 border max-w-3xl mx-auto">
          <img
            src={preview}
            alt="Preview"
            className="rounded-lg w-full max-h-[600px] object-contain border"
          />
          <button
            onClick={handlePredict}
            className="mt-6 w-full bg-teal-600 text-white py-3 rounded-lg text-lg hover:bg-teal-700 transition disabled:opacity-50"
            disabled={!preview}
          >
            Predict Age
          </button>
        </div>
      )}

      {/* Webcam Section */}
      {mode === "webcam" && (
        <div className="bg-white shadow-lg rounded-2xl p-6 border max-w-3xl mx-auto flex flex-col items-center mt-10">
          <h2 className="text-xl font-bold mb-4 text-teal-700">
            Capture from Webcam
          </h2>

          {!startWebcam && !preview && (
            <button
              onClick={() => setStartWebcam(true)}
              className="bg-teal-600 text-white px-6 py-2 rounded-lg hover:bg-teal-700 transition"
            >
              Start Webcam
            </button>
          )}

          {startWebcam && (
            <>
              <div className="w-full h-[500px] flex justify-center items-center bg-gray-100 rounded-lg overflow-hidden">
                <Webcam
                  ref={webcamRef}
                  screenshotFormat="image/png"
                  className="w-full h-full object-cover"
                  videoConstraints={{
                    width: 1280,
                    height: 720,
                    facingMode: "user",
                  }}
                />
              </div>
              <div className="flex gap-4 mt-4">
                <button
                  onClick={captureFromWebcam}
                  className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
                >
                  Capture
                </button>
              </div>
            </>
          )}

          {preview && (
            <>
              <img
                src={preview}
                alt="Captured"
                className="mt-6 rounded-lg w-full max-h-96 object-contain border"
              />
              <button
                onClick={handlePredict}
                className="mt-4 bg-teal-600 text-white px-6 py-2 rounded-lg hover:bg-teal-700 transition disabled:opacity-50"
              >
                Predict Age
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default Home;
