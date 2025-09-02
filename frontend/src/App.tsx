import React, { useState } from "react";
import { Link, Route, BrowserRouter as Router, Routes } from "react-router-dom";
import History from "./pages/History";
import Home from "./pages/Home";
import Login from "./pages/Login";

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navbar */}
        <nav className="bg-teal-600 text-white px-6 py-4 flex justify-between items-center shadow-md">
          <h1 className="text-xl font-bold tracking-wide">Age Prediction</h1>

          <div className="flex items-center gap-6">
            <Link to="/capture" className="hover:text-gray-200 transition">Capture</Link>
            <Link to="/history" className="hover:text-gray-200 transition">History</Link>

            {!isLoggedIn ? (
              <Link to="/login" className="bg-white text-teal-600 px-4 py-2 rounded-lg shadow-md font-semibold hover:bg-gray-100 transition">
                Login
              </Link>
            ) : (
              <button onClick={() => setIsLoggedIn(false)} className="bg-white text-teal-600 px-4 py-2 rounded-lg shadow-md font-semibold hover:bg-gray-100 transition">
                Logout
              </button>
            )}
          </div>
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/capture" element={<Home />} />
          <Route path="/history" element={<History />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
