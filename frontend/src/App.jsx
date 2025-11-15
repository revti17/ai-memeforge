// import { useState, useEffect } from "react";
// import { motion } from "framer-motion";
// import axios from "axios";

// const API_BASE = "http://localhost:8000";

// function App() {
//   const [prompt, setPrompt] = useState("");
//   const [image, setImage] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [downloadUrl, setDownloadUrl] = useState(null);
//   const [filename, setFilename] = useState(null);
//   const [trends, setTrends] = useState([]);
//   const [logo, setLogo] = useState(null);
//   const [error, setError] = useState(null);
//   const [brand, setBrand] = useState(null);

//   useEffect(() => {
//     fetchTrends();
//     fetchBrand();
//   }, []);

//   const fetchTrends = async () => {
//     try {
//       const res = await axios.get(`${API_BASE}/trends/`);
//       setTrends(res.data.trending || []);
//     } catch (err) {
//       console.error("Error fetching trends:", err);
//       setTrends(["AI memes", "Viral marketing", "Social media trends"]);
//     }
//   };

//   const fetchBrand = async () => {
//     try {
//       const res = await axios.get(`${API_BASE}/brand/`);
//       if (res.data.brand) {
//         setBrand(res.data.brand);
//       }
//     } catch (err) {
//       console.error("Error fetching brand:", err);
//     }
//   };

//   const handleLogoUpload = async (e) => {
//     const file = e.target.files[0];
//     if (!file) return;

//     setLogo(file);
//     const formData = new FormData();
//     formData.append("logo", file);

//     try {
//       const res = await axios.post(`${API_BASE}/brand/upload`, formData);
//       setBrand(res.data);
//     } catch (err) {
//       console.error("Error uploading logo:", err);
//     }
//   };

//   const generateMeme = async () => {
//     if (!prompt.trim()) {
//       setError("Please enter a prompt!");
//       return;
//     }

//     setLoading(true);
//     setError(null);
//     setImage(null);
//     setDownloadUrl(null);
//     setFilename(null);

//     try {
//       const formData = new FormData();
//       formData.append("prompt", prompt);
//       if (logo) {
//         formData.append("logo", logo);
//       }

//       const res = await axios.post(`${API_BASE}/generate/`, formData);

//       const imageUrl = res.data.image_url ? `${API_BASE}${res.data.image_url}` : null;
//       const downloadEndpoint = res.data.download_url ? `${API_BASE}${res.data.download_url}` : null;

//       if (imageUrl) {
//         setImage(imageUrl);
//       }
//       if (downloadEndpoint) {
//         setDownloadUrl(downloadEndpoint);
//       }
//       if (res.data.filename) {
//         setFilename(res.data.filename);
//       }
//     } catch (err) {
//       setError(err.response?.data?.detail || "Failed to generate meme");
//       console.error("Error generating meme:", err);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const useTrend = (trend) => {
//     setPrompt(trend);
//   };

//   const downloadImage = async () => {
//     if (!downloadUrl) {
//       return;
//     }

//     try {
//       const response = await axios.get(downloadUrl, { responseType: "blob" });
//       const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
//       const link = document.createElement("a");
//       link.href = blobUrl;
//       link.download = filename ? filename : `meme_${Date.now()}.png`;
//       document.body.appendChild(link);
//       link.click();
//       document.body.removeChild(link);
//       window.URL.revokeObjectURL(blobUrl);
//     } catch (err) {
//       console.error("Error downloading meme:", err);
//       setError("Failed to download meme. Please try again.");
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
//       <div className="container mx-auto px-4 py-8">
//         {/* Header */}
//         <motion.div
//           initial={{ opacity: 0, y: -20 }}
//           animate={{ opacity: 1, y: 0 }}
//           className="text-center mb-12"
//         >
//           <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
//             🎨 AI MemeForge
//           </h1>
//           <p className="text-gray-300 text-lg">
//             Generate viral memes and marketing posts with AI
//           </p>
//         </motion.div>

//         <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
//           {/* Main Content */}
//           <div className="lg:col-span-2 space-y-8">
//             {/* Input Section */}
//             <motion.div
//               initial={{ opacity: 0, x: -20 }}
//               animate={{ opacity: 1, x: 0 }}
//               className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700"
//             >
//               <h2 className="text-2xl font-semibold mb-4">Create Your Meme</h2>
              
//               <div className="space-y-4">
//                 <div>
//                   <label className="block text-sm font-medium mb-2">
//                     Enter your idea or prompt
//                   </label>
//                   <textarea
//                     className="w-full p-4 rounded-lg bg-gray-700 text-white placeholder-gray-400 border border-gray-600 focus:border-purple-500 focus:outline-none resize-none"
//                     placeholder="e.g., A cat wearing sunglasses saying 'Deal with it'"
//                     value={prompt}
//                     onChange={(e) => setPrompt(e.target.value)}
//                     rows={3}
//                   />
//                 </div>

//                 <div>
//                   <label className="block text-sm font-medium mb-2">
//                     Upload Brand Logo (Optional)
//                   </label>
//                   <input
//                     type="file"
//                     accept="image/*"
//                     onChange={handleLogoUpload}
//                     className="w-full p-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:border-purple-500 focus:outline-none"
//                   />
//                   {brand && (
//                     <div className="mt-2 flex items-center gap-2">
//                       <span className="text-sm text-gray-400">Brand color:</span>
//                       <div
//                         className="w-6 h-6 rounded-full border border-gray-600"
//                         style={{ backgroundColor: brand.dominant_color }}
//                       />
//                     </div>
//                   )}
//                 </div>

//                 <button
//                   onClick={generateMeme}
//                   disabled={loading}
//                   className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
//                 >
//                   {loading ? (
//                     <>
//                       <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
//                         <circle
//                           className="opacity-25"
//                           cx="12"
//                           cy="12"
//                           r="10"
//                           stroke="currentColor"
//                           strokeWidth="4"
//                           fill="none"
//                         />
//                         <path
//                           className="opacity-75"
//                           fill="currentColor"
//                           d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
//                         />
//                       </svg>
//                       Generating...
//                     </>
//                   ) : (
//                     "✨ Generate Meme"
//                   )}
//                 </button>

//                 {error && (
//                   <div className="bg-red-500/20 border border-red-500 text-red-200 px-4 py-3 rounded-lg">
//                     {error}
//                   </div>
//                 )}
//               </div>
//             </motion.div>

//             {/* Generated Image */}
//             {image && (
//               <motion.div
//                 initial={{ opacity: 0, scale: 0.9 }}
//                 animate={{ opacity: 1, scale: 1 }}
//                 className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700"
//               >
//                 <h2 className="text-2xl font-semibold mb-4">Your Generated Meme</h2>
//                 <div className="relative">
//                   <img
//                     src={image}
//                     alt="Generated Meme"
//                     className="w-full rounded-lg shadow-2xl"
//                   />
//                   <div className="mt-4 flex gap-4">
//                     <button
//                       onClick={downloadImage}
//                       className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
//                     >
//                       📥 Download
//                     </button>
//                     <button
//                       onClick={() => {
//                         setImage(null);
//                         setDownloadUrl(null);
//                         setFilename(null);
//                       }}
//                       className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
//                     >
//                       ✨ Generate Another
//                     </button>
//                   </div>
//                 </div>
//               </motion.div>
//             )}
//           </div>

//           {/* Sidebar */}
//           <div className="space-y-6">
//             {/* Trending Topics */}
//             <motion.div
//               initial={{ opacity: 0, x: 20 }}
//               animate={{ opacity: 1, x: 0 }}
//               className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700"
//             >
//               <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
//                 🔥 Trending Topics
//               </h2>
//               <div className="space-y-2">
//                 {trends.map((trend, idx) => (
//                   <button
//                     key={idx}
//                     onClick={() => useTrend(trend)}
//                     className="w-full text-left p-3 rounded-lg bg-gray-700/50 hover:bg-gray-700 transition-colors text-sm"
//                   >
//                     {trend}
//                   </button>
//                 ))}
//               </div>
//             </motion.div>

//             {/* Info Card */}
//             <motion.div
//               initial={{ opacity: 0, x: 20 }}
//               animate={{ opacity: 1, x: 0 }}
//               transition={{ delay: 0.2 }}
//               className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700"
//             >
//               <h3 className="text-lg font-semibold mb-3">💡 Tips</h3>
//               <ul className="space-y-2 text-sm text-gray-300">
//                 <li>• Be specific with your prompts</li>
//                 <li>• Use trending topics for better reach</li>
//                 <li>• Upload your brand logo for personalization</li>
//                 <li>• Download and share your creations</li>
//               </ul>
//             </motion.div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;

import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { LoginModal } from "./components/auth/LoginModal";
import { UserDashboard } from "./components/dashboard/UserDashboard";
import { GradientBackground } from "./components/layout/GradientBackground";
import { AppHeader } from "./components/layout/AppHeader";
import { AppFooter } from "./components/layout/AppFooter";
import { HeroSection } from "./components/sections/HeroSection";
import { GeneratorSection } from "./components/sections/GeneratorSection";
import { ShowcaseSection } from "./components/sections/ShowcaseSection";
import { FeatureSection } from "./components/sections/FeatureSection";
import { PricingSection } from "./components/sections/PricingSection";
import { TestimonialsSection } from "./components/sections/TestimonialsSection";
import { useMemeGenerator } from "./hooks/useMemeGenerator";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

// Google OAuth Client ID - Get this from Google Cloud Console
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || "YOUR_GOOGLE_CLIENT_ID_HERE";

function AppContent() {
  const { isAuthenticated, loading, showLoginModal, setShowLoginModal } = useAuth();
  const generator = useMemeGenerator();
  const { state } = generator;
  const { setBrandProfile } = state;
  const [trendingTopics, setTrendingTopics] = useState([]);
  const [scrollTarget, setScrollTarget] = useState(null);
  const [showDashboard, setShowDashboard] = useState(false);

  useEffect(() => {
    const fetchBrand = async () => {
      try {
        const res = await axios.get(`${API_BASE}/brand/`);
        if (res.data?.brand) {
          setBrandProfile(res.data.brand);
        }
      } catch (error) {
        console.warn("Unable to load brand profile", error);
      }
    };

    const fetchTrends = async () => {
      try {
        const res = await axios.get(`${API_BASE}/trends/`);
        const topics = res.data?.trending || res.data?.trends || [];
        const normalized = topics.map((topic) =>
          typeof topic === "string" ? topic : topic.keyword || topic.title || ""
        );
        setTrendingTopics(normalized.filter(Boolean));
      } catch (error) {
        console.warn("Unable to load trends", error);
        setTrendingTopics(["AI memes", "Product launch", "Culture drops", "Founder moments"]);
      }
    };

    fetchBrand();
    fetchTrends();
  }, [setBrandProfile]);

  useEffect(() => {
    if (scrollTarget) {
      scrollTarget.scrollIntoView({ behavior: "smooth", block: "start" });
      setScrollTarget(null);
    }
  }, [scrollTarget]);

  const handleLaunchStudio = () => {
    const studioSection = document.getElementById("studio");
    if (studioSection) {
      setScrollTarget(studioSection);
    }
  };

  const generatorProps = useMemo(
    () => ({
      generator,
      trends: trendingTopics,
    }),
    [generator, trendingTopics]
  );

  // Show loading spinner while checking auth
  if (loading) {
    return (
      <GradientBackground>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-purple-500 mx-auto mb-4"></div>
            <p className="text-white text-lg">Loading...</p>
          </div>
        </div>
      </GradientBackground>
    );
  }

  // Show app with login modal overlay when needed
  return (
    <GradientBackground>
      <LoginModal isOpen={showLoginModal} onClose={() => setShowLoginModal(false)} />
      <AppHeader 
        onDashboardClick={() => {
          if (isAuthenticated) {
            setShowDashboard(!showDashboard);
          } else {
            setShowLoginModal(true);
          }
        }} 
      />
      <main>
        {showDashboard && isAuthenticated ? (
          <UserDashboard />
        ) : (
          <>
            <HeroSection onGenerate={handleLaunchStudio} />
            <GeneratorSection {...generatorProps} />
            <ShowcaseSection generator={generator} />
            <FeatureSection />
            <TestimonialsSection />
            <PricingSection />
          </>
        )}
      </main>
      <AppFooter />
    </GradientBackground>
  );
}

function App() {
  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}

export default App;
