import { useState, useMemo } from "react";
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export function useMemeGenerator() {
  const [prompt, setPrompt] = useState("");
  const [logoFile, setLogoFile] = useState(null);
  const [brandColor, setBrandColor] = useState("#a855f7");
  const [tone, setTone] = useState("humorous");
  const [voice, setVoice] = useState("casual");
  const [useTrends, setUseTrends] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [filename, setFilename] = useState(null);
  const [captionOptions, setCaptionOptions] = useState([]);
  const [selectedCaption, setSelectedCaption] = useState(null);
  const [brandProfile, setBrandProfile] = useState(null);

  const resetOutput = () => {
    setImageUrl(null);
    setDownloadUrl(null);
    setFilename(null);
    setCaptionOptions([]);
    setSelectedCaption(null);
  };

  const uploadLogo = async (file) => {
    if (!file) return;
    setLogoFile(file);
    const formData = new FormData();
    formData.append("logo", file);
    try {
      const res = await axios.post(`${API_BASE}/brand/upload`, formData);
      setBrandProfile(res.data);
      if (res.data?.dominant_color) {
        setBrandColor(res.data.dominant_color);
      }
    } catch (err) {
      console.error("Logo upload failed", err);
      setError("Failed to upload logo. Please try again.");
    }
  };

  const generateMeme = async () => {
    if (!prompt.trim()) {
      setError("Please enter a prompt to get started.");
      return;
    }
    setLoading(true);
    setError(null);
    resetOutput();

    try {
      const formData = new FormData();
      formData.append("prompt", prompt);
      formData.append("use_trends", String(useTrends));
      formData.append("tone", tone);
      formData.append("voice", voice);
      if (brandProfile?.brand_name) {
        formData.append("brand_name", brandProfile.brand_name);
      }
      if (logoFile) {
        formData.append("logo", logoFile);
      }
      const res = await axios.post(`${API_BASE}/generate/`, formData);
      const image = res.data.image_url ? `${API_BASE}${res.data.image_url}` : null;
      setImageUrl(image);
      setDownloadUrl(res.data.download_url ? `${API_BASE}${res.data.download_url}` : null);
      setFilename(res.data.filename || null);

      const options = res.data.metadata?.caption_options || [];
      const caption = res.data.caption || options[0] || null;
      setCaptionOptions(options.length ? options : caption ? [caption] : []);
      setSelectedCaption(caption);
    } catch (err) {
      console.error("Generation failed", err);
      const detail = err.response?.data?.detail;
      setError(
        typeof detail === "string"
          ? detail
          : detail?.issues?.join(", ") || "Failed to generate meme. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const downloadMeme = async () => {
    if (!downloadUrl) return;
    try {
      const response = await axios.get(downloadUrl, { responseType: "blob" });
      const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = blobUrl;
      link.download = filename || `meme_${Date.now()}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);
    } catch (err) {
      console.error("Download failed", err);
      setError("Could not download image. Please try again shortly.");
    }
  };

  const palette = useMemo(() => {
    const fallback = brandColor || "#a855f7";
    return {
      primary: fallback,
      soft: `${fallback}22`,
      gradient: `linear-gradient(135deg, ${fallback} 0%, #6366f1 100%)`,
    };
  }, [brandColor]);

  return {
    state: {
      prompt,
      setPrompt,
      logoFile,
      uploadLogo,
      tone,
      setTone,
      voice,
      setVoice,
      useTrends,
      setUseTrends,
      brandColor,
      setBrandColor,
      brandProfile,
      setBrandProfile,
      loading,
      error,
      imageUrl,
      downloadUrl,
      filename,
      captionOptions,
      selectedCaption,
      setSelectedCaption,
      palette,
    },
    actions: {
      generateMeme,
      downloadMeme,
      resetOutput,
    },
  };
}


