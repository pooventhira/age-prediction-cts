import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (username && password) {
      // Navigate to Home/Capture page after login
      navigate("/capture");
    } else {
      alert("Please enter username and password");
    }
  };

  return (
    <div className="flex justify-center items-center h-[90vh] bg-gray-50">
      <div className="bg-white shadow-2xl rounded-3xl p-12 w-[500px] border">
        <h2 className="text-3xl font-bold mb-8 text-center text-teal-700">Login</h2>

        {/* Username */}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full border rounded-xl p-3 mb-5 text-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
        />

        {/* Password */}
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border rounded-xl p-3 mb-8 text-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
        />

        {/* Login Button */}
        <button
          onClick={handleLogin}
          className="w-full bg-teal-600 text-white py-3 text-lg rounded-xl hover:bg-teal-700 transition"
        >
          Login
        </button>
      </div>
    </div>
  );
};

export default Login;
