import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useAuth } from "../../context/AuthContext";
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const UserDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({ total_memes: 0, total_downloads: 0 });
  const [recentMemes, setRecentMemes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      // Fetch user's memes
      const memesRes = await axios.get(`${API_BASE}/generate/history?limit=6`);
      setRecentMemes(memesRes.data.memes || []);

      // Fetch stats
      const statsRes = await axios.get(`${API_BASE}/generate/stats/mongodb`);
      if (statsRes.data.stats) {
        setStats({
          total_memes: statsRes.data.stats.total_memes || 0,
          total_downloads: statsRes.data.stats.total_downloads || 0,
        });
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center gap-4 mb-2">
          {user.picture && (
            <img
              src={user.picture}
              alt={user.name}
              className="w-16 h-16 rounded-full border-2 border-purple-500"
            />
          )}
          <div>
            <h1 className="text-3xl font-bold text-white">
              Welcome back, {user.name?.split(" ")[0]}! 👋
            </h1>
            <p className="text-gray-400">{user.email}</p>
          </div>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 backdrop-blur-sm border border-purple-500/30 rounded-2xl p-6"
        >
          <div className="text-4xl mb-2">🎨</div>
          <h3 className="text-gray-400 text-sm mb-1">Total Memes</h3>
          <p className="text-3xl font-bold text-white">{stats.total_memes}</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 backdrop-blur-sm border border-blue-500/30 rounded-2xl p-6"
        >
          <div className="text-4xl mb-2">📥</div>
          <h3 className="text-gray-400 text-sm mb-1">Downloads</h3>
          <p className="text-3xl font-bold text-white">{stats.total_downloads}</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 backdrop-blur-sm border border-green-500/30 rounded-2xl p-6"
        >
          <div className="text-4xl mb-2">⭐</div>
          <h3 className="text-gray-400 text-sm mb-1">Member Since</h3>
          <p className="text-xl font-bold text-white">
            {new Date().toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}
          </p>
        </motion.div>
      </div>

      {/* Recent Memes */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-6"
      >
        <h2 className="text-2xl font-bold text-white mb-6">Recent Creations 🔥</h2>
        
        {recentMemes.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🎨</div>
            <p className="text-gray-400 text-lg mb-4">No memes yet!</p>
            <p className="text-gray-500 text-sm">Start creating amazing memes to see them here</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recentMemes.map((meme, index) => (
              <motion.div
                key={meme.event_id || index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="bg-gray-700/30 rounded-xl overflow-hidden border border-gray-600 hover:border-purple-500 transition-all duration-300 group"
              >
                <div className="relative">
                  <img
                    src={`${API_BASE}/outputs/${meme.filename}`}
                    alt={meme.prompt}
                    className="w-full h-48 object-cover"
                    onError={(e) => {
                      e.target.src = "https://via.placeholder.com/400x300?text=Meme";
                    }}
                  />
                  <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                    <a
                      href={`${API_BASE}/generate/download/${meme.filename}`}
                      download
                      className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors"
                    >
                      Download
                    </a>
                  </div>
                </div>
                <div className="p-4">
                  <p className="text-gray-300 text-sm line-clamp-2 mb-2">
                    {meme.prompt || "No prompt"}
                  </p>
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>{new Date(meme.timestamp).toLocaleDateString()}</span>
                    <span className="flex items-center gap-1">
                      <span>📥</span>
                      {meme.engagement?.downloads || 0}
                    </span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>
    </div>
  );
};
