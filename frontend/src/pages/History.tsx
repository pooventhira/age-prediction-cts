import React, { useEffect, useState } from "react";

interface HistoryItem {
  id: number;
  image: string;
  predictedAge: number;
  uploadedAt: string;
}

const History: React.FC = () => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [previewItem, setPreviewItem] = useState<HistoryItem | null>(null);

  useEffect(() => {
    const savedHistory = localStorage.getItem("predictionHistory");
    if (savedHistory) setHistory(JSON.parse(savedHistory));
  }, []);

  const handleDelete = (id: number) => {
    const updatedHistory = history.filter(item => item.id !== id);
    setHistory(updatedHistory);
    localStorage.setItem("predictionHistory", JSON.stringify(updatedHistory));
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4 text-teal-700">Prediction History</h2>

      {history.length === 0 ? (
        <p className="text-gray-600">No history available yet.</p>
      ) : (
        <div className="grid md:grid-cols-3 sm:grid-cols-2 gap-6">
          {history.map((item) => (
            <div
              key={item.id}
              className="bg-white shadow-lg rounded-2xl overflow-hidden border border-gray-200 transition-transform transform hover:scale-105 relative"
            >
              {/* Image */}
              <img
                src={item.image}
                alt="Uploaded"
                className="w-full h-52 object-cover"
              />

              {/* Buttons */}
              <div className="absolute top-2 right-2 flex gap-2">
                <button
                  onClick={() => handleDelete(item.id)}
                  className="bg-red-600 text-white px-3 py-1 rounded-lg hover:bg-red-700 transition"
                >
                  Delete
                </button>
                <button
                  onClick={() => setPreviewItem(item)}
                  className="bg-blue-600 text-white px-3 py-1 rounded-lg hover:bg-blue-700 transition"
                >
                  Preview
                </button>
              </div>

              {/* Card Content */}
              <div className="p-4">
                <p className="text-lg font-semibold text-teal-700">
                  Predicted Age: <span className="text-gray-800">{item.predictedAge}</span>
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  Uploaded on:{" "}
                  <span className="font-medium text-gray-800">
                    {new Date(item.uploadedAt).toLocaleString()}
                  </span>
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Preview Modal */}
      {previewItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white rounded-2xl shadow-lg max-w-lg w-full p-6 relative">
            <button
              onClick={() => setPreviewItem(null)}
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-800 font-bold text-lg"
            >
              ×
            </button>
            <img
              src={previewItem.image}
              alt="Preview"
              className="w-full h-80 object-contain rounded-lg mb-4"
            />
            <p className="text-lg font-semibold text-teal-700">
              Predicted Age: <span className="text-gray-800">{previewItem.predictedAge}</span>
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Uploaded on:{" "}
              <span className="font-medium text-gray-800">
                {new Date(previewItem.uploadedAt).toLocaleString()}
              </span>
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default History;
