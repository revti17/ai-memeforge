import { GoogleLogin } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";
import { useAuth } from "../../context/AuthContext";
import axios from "axios";
import { motion } from "framer-motion";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const LoginPage = () => {
  const { login } = useAuth();

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      const decoded = jwtDecode(credentialResponse.credential);
      
      // Send to backend for verification and user creation
      const response = await axios.post(`${API_BASE}/auth/google`, {
        token: credentialResponse.credential,
        email: decoded.email,
        name: decoded.name,
        picture: decoded.picture,
      });

      // Login user with backend response
      login(response.data.user, response.data.token);
    } catch (error) {
      console.error("Login failed:", error);
      // Fallback: login with decoded Google info
      const decoded = jwtDecode(credentialResponse.credential);
      const userData = {
        email: decoded.email,
        name: decoded.name,
        picture: decoded.picture,
        sub: decoded.sub,
      };
      login(userData, credentialResponse.credential);
    }
  };

  const handleGoogleError = () => {
    console.error("Google Login Failed");
    alert("Failed to login with Google. Please try again.");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-gray-900 to-pink-900">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="bg-gray-800/50 backdrop-blur-xl border border-gray-700 rounded-3xl p-12 max-w-md w-full mx-4 shadow-2xl"
      >
        {/* Logo/Brand */}
        <div className="text-center mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="inline-block mb-6"
          >
            <div className="text-7xl mb-4">🎨</div>
          </motion.div>
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            AI MemeForge
          </h1>
          <p className="text-gray-300 text-lg">
            Create viral memes with AI
          </p>
        </div>

        {/* Description */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-8"
        >
          <p className="text-gray-400 text-center text-sm">
            Sign in to start generating amazing memes, track your creations, and access exclusive features.
          </p>
        </motion.div>

        {/* Google Login Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="flex justify-center"
        >
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={handleGoogleError}
            theme="filled_black"
            size="large"
            text="signin_with"
            shape="rectangular"
            logo_alignment="left"
          />
        </motion.div>

        {/* Features List */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mt-10 pt-8 border-t border-gray-700"
        >
          <p className="text-gray-400 text-xs text-center mb-4 font-semibold">
            What you'll get:
          </p>
          <ul className="space-y-3 text-sm text-gray-300">
            <motion.li
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.7 }}
              className="flex items-center gap-3"
            >
              <span className="text-green-400 text-xl">✓</span>
              <span>Unlimited meme generation</span>
            </motion.li>
            <motion.li
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.8 }}
              className="flex items-center gap-3"
            >
              <span className="text-green-400 text-xl">✓</span>
              <span>Personal dashboard</span>
            </motion.li>
            <motion.li
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.9 }}
              className="flex items-center gap-3"
            >
              <span className="text-green-400 text-xl">✓</span>
              <span>Save and manage your memes</span>
            </motion.li>
            <motion.li
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 1.0 }}
              className="flex items-center gap-3"
            >
              <span className="text-green-400 text-xl">✓</span>
              <span>Brand customization</span>
            </motion.li>
          </ul>
        </motion.div>

        {/* Privacy Note */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.1 }}
          className="text-xs text-gray-500 text-center mt-8"
        >
          By signing in, you agree to our Terms of Service and Privacy Policy
        </motion.p>
      </motion.div>
    </div>
  );
};
