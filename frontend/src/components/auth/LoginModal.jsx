import { GoogleLogin } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";
import { useAuth } from "../../context/AuthContext";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const LoginModal = ({ isOpen, onClose }) => {
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
      onClose(); // Close modal after successful login
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
      onClose();
    }
  };

  const handleGoogleError = () => {
    console.error("Google Login Failed");
    alert("Failed to login with Google. Please try again.");
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50"
            onClick={onClose}
          />

          {/* Modal */}
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              transition={{ type: "spring", duration: 0.5 }}
              className="bg-gray-800/95 backdrop-blur-xl border border-gray-700 rounded-3xl p-8 max-w-md w-full shadow-2xl relative"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Close Button */}
              <button
                onClick={onClose}
                className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
                aria-label="Close"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>

              {/* Logo/Brand */}
              <div className="text-center mb-6">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                  className="inline-block mb-4"
                >
                  <div className="text-6xl">🎨</div>
                </motion.div>
                <h2 className="text-3xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                  AI MemeForge
                </h2>
                <p className="text-gray-300">
                  Create viral memes with AI
                </p>
              </div>

              {/* Description */}
              <div className="mb-6">
                <p className="text-gray-400 text-center text-sm">
                  Sign in to start generating amazing memes, track your creations, and access exclusive features.
                </p>
              </div>

              {/* Google Login Button */}
              <div className="flex justify-center mb-6">
                <GoogleLogin
                  onSuccess={handleGoogleSuccess}
                  onError={handleGoogleError}
                  theme="filled_black"
                  size="large"
                  text="signin_with"
                  shape="rectangular"
                  logo_alignment="left"
                />
              </div>

              {/* Features List */}
              <div className="pt-6 border-t border-gray-700">
                <p className="text-gray-400 text-xs text-center mb-3 font-semibold">
                  What you'll get:
                </p>
                <ul className="space-y-2 text-sm text-gray-300">
                  <li className="flex items-center gap-2">
                    <span className="text-green-400">✓</span>
                    <span>Unlimited meme generation</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="text-green-400">✓</span>
                    <span>Personal dashboard</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="text-green-400">✓</span>
                    <span>Save and manage your memes</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="text-green-400">✓</span>
                    <span>Brand customization</span>
                  </li>
                </ul>
              </div>

              {/* Terms */}
              <p className="text-xs text-gray-500 text-center mt-6">
                By signing in, you agree to our Terms of Service and Privacy Policy
              </p>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
};
