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
        <nav className="bg-teal-600 text-white px-6 py-4 shadow-md">
          <div className="max-w-7xl mx-auto flex items-center relative">
            {/* Left: Logo */}
            <div>
              <h1 className="text-xl font-bold tracking-wide">Age Prediction</h1>
            </div>

            {/* Center: History Button */}
            <div className="absolute left-1/2 transform -translate-x-1/2">
              <Link
                to="/history"
                className="hover:text-gray-200 transition font-medium"
              >
                History
              </Link>
            </div>

            {/* Right: Login/Logout */}
            <div className="ml-auto">
              {!isLoggedIn ? (
                <Link
                  to="/login"
                  className="bg-white text-teal-600 px-4 py-2 rounded-lg shadow-md font-semibold hover:bg-gray-100 transition"
                >
                  Login
                </Link>
              ) : (
                <button
                  onClick={() => setIsLoggedIn(false)}
                  className="bg-white text-teal-600 px-4 py-2 rounded-lg shadow-md font-semibold hover:bg-gray-100 transition"
                >
                  Logout
                </button>
              )}
            </div>
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
