# """
# AI Engine Service - Final Updated Version
# Handles: Image Generation, Caption Generation, Prompt Enhancement, and Meme Creation
# """

# import os
# import io
# import time
# import json
# import logging
# import requests
# from pathlib import Path
# from PIL import Image, ImageDraw, ImageFont
# from typing import Dict, List, Optional
# from datetime import datetime
# from dotenv import load_dotenv
# from requests.exceptions import HTTPError, RequestException

# # === Setup ===
# load_dotenv()
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # === Directories ===
# BACKEND_DIR = Path(__file__).parent.parent
# OUTPUTS_DIR = BACKEND_DIR / "outputs"
# DATASETS_DIR = BACKEND_DIR / "datasets"
# OUTPUTS_DIR.mkdir(exist_ok=True)
# DATASETS_DIR.mkdir(exist_ok=True)

# # === Hugging Face API ===
# HF_TOKEN = os.getenv("HF_TOKEN")
# HF_API_BASE = "https://router.huggingface.co/hf-inference/models"
# HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# # === Models ===
# FLUX_MODEL = "black-forest-labs/FLUX.1-schnell"
# IMAGE_MODEL_CANDIDATES = [
#     FLUX_MODEL,
#     "stabilityai/stable-diffusion-2-1",
#     "runwayml/stable-diffusion-v1-5",
# ]
# CAPTION_MODEL = "HuggingFaceH4/zephyr-7b-beta"
# BLIP_MODEL = "Salesforce/blip-image-captioning-large"
# PROMPT_ENHANCER_MODELS = [
#     "HuggingFaceH4/zephyr-7b-beta",
#     "meta-llama/Llama-3-8b-chat-hf",
# ]


# class AIEngine:
#     """Main AI Engine for meme generation"""

#     def __init__(self):
#         self.brand_memory = self._load_brand_memory()
#         self.caption_templates = self._load_caption_templates()
#         self.prompt_examples = self._load_prompt_examples()
#         self.prompt_enhancer_model_used = None
#         self.image_model_used = None

#     # ==========================================================
#     # Brand & Prompt Setup
#     # ==========================================================
#     def _load_brand_memory(self) -> Dict:
#         file = DATASETS_DIR / "brand_memory.json"
#         if file.exists():
#             with open(file, "r") as f:
#                 return json.load(f)
#         return {
#             "tone": "humorous",
#             "voice": "casual",
#             "colors": [],
#             "hashtags": [],
#             "past_captions": [],
#         }

#     def _load_caption_templates(self) -> List[str]:
#         return [
#             "When {topic} hits different 💀",
#             "POV: You just discovered {topic}",
#             "Nobody:\nAbsolutely nobody:\n{topic}:",
#             "{topic} be like:",
#             "The {topic} experience",
#             "Tell me you love {topic} without telling me",
#             "{topic} > everything else",
#             "Why is {topic} so relatable though?",
#         ]

#     def _load_prompt_examples(self) -> List[Dict]:
#         return [
#             {
#                 "user_input": "cat coding",
#                 "enhanced_prompt": "A cute cat typing code on a laptop in a cozy home office.",
#             },
#             {
#                 "user_input": "monday mood",
#                 "enhanced_prompt": "A tired person dragging themselves out of bed Monday morning, holding coffee.",
#             },
#         ]

#     # ==========================================================
#     # Generic Hugging Face API Call
#     # ==========================================================
#     def call_hf_api(
#         self,
#         model: str,
#         payload: Dict,
#         headers: Optional[Dict] = None,
#         max_retries: int = 3,
#     ):
#         url = f"{HF_API_BASE}/{model}"
#         headers = headers or HEADERS

#         for attempt in range(max_retries):
#             try:
#                 response = requests.post(
#                     url, headers=headers, json=payload, timeout=120
#                 )

#                 if response.status_code in (503, 524):
#                     logger.warning(f"Model loading... retrying (attempt {attempt + 1})")
#                     time.sleep(30)
#                     continue

#                 if response.status_code == 429:
#                     logger.warning(f"Rate limited... waiting (attempt {attempt + 1})")
#                     time.sleep(60)
#                     continue

#                 response.raise_for_status()
#                 return response
#             except Exception as e:
#                 logger.warning(f"API call failed ({model}): {e}")
#                 if attempt == max_retries - 1:
#                     raise
#                 time.sleep(5 * (attempt + 1))

#     # ==========================================================
#     # Prompt Enhancement
#     # ==========================================================
#     def enhance_prompt(self, user_input: str, trends: Optional[List[str]] = None) -> str:
#         examples_text = "\n\n".join(
#             [
#                 f"User: {ex['user_input']}\nEnhanced: {ex['enhanced_prompt']}"
#                 for ex in self.prompt_examples
#             ]
#         )
#         trend_text = f"\nInclude trending topics: {', '.join(trends)}" if trends else ""

#         full_prompt = f"""
# You are a visual prompt expert. Convert the user's text into a rich visual scene for AI image generation.

# {examples_text}

# User: {user_input}{trend_text}
# Enhanced:
# """

#         payload = {"inputs": full_prompt, "parameters": {"max_new_tokens": 120, "temperature": 0.7}}

#         for model in PROMPT_ENHANCER_MODELS:
#             try:
#                 resp = self.call_hf_api(model, payload)
#                 result = resp.json()
#                 if isinstance(result, list) and len(result) > 0:
#                     enhanced = result[0].get("generated_text", "").strip()
#                     if enhanced:
#                         logger.info(f"Enhanced with {model}: {enhanced[:100]}...")
#                         self.prompt_enhancer_model_used = model
#                         return enhanced
#             except Exception as e:
#                 logger.warning(f"Enhancement via {model} failed: {e}")

#         logger.warning("Prompt enhancement fallback used.")
#         return f"{user_input}, cinematic lighting, ultra detailed, trending on social media"

#     # ==========================================================
#     # Image Generation
#     # ==========================================================
#     def generate_image(self, prompt: str) -> bytes:
#         payload = {
#             "inputs": prompt,
#             "parameters": {
#                 "negative_prompt": "low quality, blurry, distorted",
#             },
#         }

#         for model in IMAGE_MODEL_CANDIDATES:
#             try:
#                 logger.info(f"Generating image using {model} ...")
#                 resp = requests.post(
#                     f"{HF_API_BASE}/{model}",
#                     headers={**HEADERS, "Accept": "image/png"},
#                     json=payload,
#                     timeout=300,
#                 )
#                 if resp.status_code == 200 and resp.headers.get("content-type", "").startswith("image/"):
#                     self.image_model_used = model
#                     return resp.content
#                 else:
#                     logger.warning(f"{model} failed (status {resp.status_code})")
#             except Exception as e:
#                 logger.warning(f"{model} error: {e}")

#         raise Exception("❌ All image generation models failed.")

#     # ==========================================================
#     # Caption Generation
#     # ==========================================================
#     def generate_captions(
#         self, prompt: str, image_description: str, brand_context: Optional[Dict] = None, num_candidates: int = 5
#     ) -> List[str]:
#         text_prompt = f"Generate {num_candidates} short, viral meme captions for this: {prompt}\nImage context: {image_description}\nUse emojis and humor!"
#         payload = {"inputs": text_prompt, "parameters": {"max_new_tokens": 100, "temperature": 0.9}}

#         try:
#             resp = self.call_hf_api(CAPTION_MODEL, payload)
#             result = resp.json()
#             if isinstance(result, list) and len(result) > 0:
#                 captions_raw = result[0].get("generated_text", "")
#                 captions = [
#                     line.strip(" -0123456789.") for line in captions_raw.split("\n") if line.strip()
#                 ]
#                 return captions[:num_candidates]
#         except Exception as e:
#             logger.warning(f"Caption generation failed: {e}")

#         topic = prompt.split()[0] if prompt else "life"
#         return [t.format(topic=topic) for t in self.caption_templates[:num_candidates]]

#     # ==========================================================
#     # Add Caption Overlay
#     # ==========================================================
#     def add_caption_to_image(
#         self, image: Image.Image, caption: str, brand_colors: Optional[List[str]] = None
#     ) -> Image.Image:
#         img = image.copy()
#         draw = ImageDraw.Draw(img)
#         font_size = max(30, image.height // 20)

#         try:
#             font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", font_size)
#         except:
#             font = ImageFont.load_default()

#         bbox = draw.textbbox((0, 0), caption, font=font)
#         text_width = bbox[2] - bbox[0]
#         x = (image.width - text_width) / 2
#         y = image.height - font_size * 2

#         text_color = "white"
#         outline_color = "black"
#         if brand_colors:
#             text_color = brand_colors[0] if brand_colors else "white"

#         for dx in range(-2, 3):
#             for dy in range(-2, 3):
#                 draw.text((x + dx, y + dy), caption, font=font, fill=outline_color)
#         draw.text((x, y), caption, font=font, fill=text_color)

#         return img

#     # ==========================================================
#     # Meme Generation Pipeline
#     # ==========================================================
#     def generate_meme(
#         self,
#         user_prompt: str,
#         logo_path: Optional[str] = None,
#         trends: Optional[List[str]] = None,
#         brand_context: Optional[Dict] = None,
#     ) -> Dict:
#         start_time = time.time()
#         try:
#             # Step 1: Enhance Prompt
#             logger.info("Step 1: Enhancing prompt...")
#             enhanced_prompt = self.enhance_prompt(user_prompt, trends)

#             # Step 2: Generate Image
#             logger.info("Step 2: Generating image...")
#             image_bytes = self.generate_image(enhanced_prompt)
#             image = Image.open(io.BytesIO(image_bytes))

#             # Step 3: Generate Captions
#             logger.info("Step 3: Generating captions...")
#             captions = self.generate_captions(user_prompt, "generated image", brand_context)
#             best_caption = captions[0] if isinstance(captions, list) else captions

#             # Step 4: Overlay Caption
#             logger.info(f"Step 4: Overlaying caption '{best_caption}'...")
#             brand_colors = None
#             if brand_context and brand_context.get("colors"):
#                 brand_colors = brand_context["colors"]

#             final_image = self.add_caption_to_image(image, best_caption, brand_colors)

#             # Step 5: Save Image
#             filename = f"meme_{int(time.time())}.png"
#             path = OUTPUTS_DIR / filename
#             final_image.save(path, "PNG", quality=95, optimize=True)
#             logger.info(f"✅ Meme saved: {path}")

#             return {
#                 "success": True,
#                 "filename": filename,
#                 "path": str(path),
#                 "caption": best_caption,
#                 "enhanced_prompt": enhanced_prompt,
#                 "image_description": "auto-generated meme image",
#                 "image_model": self.image_model_used,
#                 "prompt_model": self.prompt_enhancer_model_used,
#                 "generation_time": round(time.time() - start_time, 2),
#                 "metadata": {
#                     "trends_used": trends or [],
#                     "brand_colors": brand_colors,
#                 },
#             }

#         except Exception as e:
#             logger.error(f"❌ Meme generation failed: {e}", exc_info=True)
#             raise Exception(f"Failed to generate meme: {str(e)}")


# # ==========================================================
# # Singleton Helper
# # ==========================================================
# _ai_engine = None


# def get_ai_engine() -> AIEngine:
#     global _ai_engine
#     if _ai_engine is None:
#         _ai_engine = AIEngine()
#     return _ai_engine
"""
AI Engine Service - Final Updated Version (Mistral 7B Integrated with OpenRouter + Working Flux Endpoint)
Handles: Image Generation, Caption Generation, Prompt Enhancement, and Meme Creation
"""

import os
import io
import time
import json
import logging
import random
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from requests.exceptions import HTTPError, RequestException

# === Setup ===
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Directories ===
BACKEND_DIR = Path(__file__).parent.parent
OUTPUTS_DIR = BACKEND_DIR / "outputs"
DATASETS_DIR = BACKEND_DIR / "datasets"
OUTPUTS_DIR.mkdir(exist_ok=True)
DATASETS_DIR.mkdir(exist_ok=True)

# === API KEYS ===
HF_TOKEN = os.getenv("HF_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is required")
if not OPENROUTER_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is required")

# === BASE URLs ===
HF_API_TEXT_BASE = "https://api-inference.huggingface.co/models"
FLUX_API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Accept": "image/png"}

# === Models ===
FLUX_MODEL = "black-forest-labs/FLUX.1-schnell"
CAPTION_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
PROMPT_MODEL = "mistralai/mistral-7b-instruct-v0.3"


class AIEngine:
    """Main AI Engine for meme generation"""

    def __init__(self):
        self.brand_memory = self._load_brand_memory()
        self.caption_templates = self._load_caption_templates()
        self.prompt_examples = self._load_prompt_examples()
        self.prompt_enhancer_model_used = None
        self.image_model_used = None

    # ==========================================================
    # Brand & Prompt Setup
    # ==========================================================
    def _load_brand_memory(self) -> Dict:
        file = DATASETS_DIR / "brand_memory.json"
        if file.exists():
            with open(file, "r") as f:
                return json.load(f)
        return {
            "tone": "humorous",
            "voice": "casual",
            "colors": [],
            "hashtags": [],
            "past_captions": [],
        }

    def _load_caption_templates(self) -> List[str]:
        return [
            "When {topic} hits different 💀",
            "POV: You just discovered {topic}",
            "Nobody:\nAbsolutely nobody:\n{topic}:",
            "{topic} be like:",
            "The {topic} experience",
            "Tell me you love {topic} without telling me",
            "{topic} > everything else",
            "Why is {topic} so relatable though?",
        ]

    def _load_prompt_examples(self) -> List[Dict]:
        return [
            {"user_input": "cat coding", "enhanced_prompt": "A cute cat typing code on a laptop in a cozy home office."},
            {"user_input": "monday mood", "enhanced_prompt": "A tired person dragging themselves out of bed Monday morning, holding coffee."},
        ]

    # ==========================================================
    # Prompt Enhancement via OpenRouter (Mistral 7B)
    # ==========================================================
    def enhance_prompt(self, user_input: str, trends: Optional[List[str]] = None) -> str:
        """Enhanced prompt generation using OpenRouter (Mistral 7B)."""
        trend_text = f"Include trending topics: {', '.join(trends)}." if trends else ""
        system_prompt = (
            "You are a professional AI prompt engineer. "
            "Your task is to expand a short idea into a cinematic, vivid, and highly detailed prompt "
            "for an image generation model such as Flux, SDXL, or DALL·E 3. "
            "Describe the scene with artistic depth, realistic lighting, mood, atmosphere, and composition. "
            "Incorporate environment, color tones, textures, and perspective to make the image visually striking "
            "and photorealistic. Focus on style, storytelling, and emotional impact."
        )
        user_prompt = f"{user_input}. {trend_text}\nEnhanced prompt:"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "PromptEnhancer"
        }
        payload = {
            "model": PROMPT_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)
            if response.status_code != 200:
                logger.error(f"❌ OpenRouter error {response.status_code}: {response.text}")
                return f"{user_input}, cinematic lighting, ultra detailed."

            data = response.json()
            enhanced = data["choices"][0]["message"]["content"].strip()
            self.prompt_enhancer_model_used = PROMPT_MODEL
            logger.info(f"✅ Enhanced prompt generated via OpenRouter: {enhanced[:100]}...")
            return enhanced
        except Exception as e:
            logger.warning(f"OpenRouter prompt enhancement failed: {e}")
            return f"{user_input}, cinematic lighting, ultra detailed."

    # ==========================================================
    # ✅ Image Generation using Flux (your working version)
    # ==========================================================
    def generate_image(self, prompt: str) -> bytes:
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": "blurry, distorted, bad quality, watermark"
            }
        }

        print("🎨 Generating image via Hugging Face... please wait...")

        response = requests.post(FLUX_API_URL, headers=HEADERS, json=payload)
        if response.status_code != 200:
            logger.error(f"❌ Error: {response.text}")
            raise Exception(f"Flux generation failed: {response.text}")

        image_bytes = response.content
        self.image_model_used = "black-forest-labs/FLUX.1-schnell"
        logger.info("✅ Image generated successfully via Flux.")
        return image_bytes

    # ==========================================================
    # Caption Generation & Meme Pipeline
    # ==========================================================
    def _clean_caption_line(self, line: str) -> str:
        cleaned = line.strip().strip('"').strip("'")
        # Remove leading bullets/numbers
        cleaned = cleaned.lstrip("-•*").strip()
        while cleaned and (cleaned[0].isdigit() or cleaned[0] in {")", ".", ":"}):
            cleaned = cleaned[1:].strip()
        return cleaned

    def _dedupe_captions(self, captions: List[str], brand_context: Optional[Dict]) -> List[str]:
        seen = set()
        history = set()
        if brand_context:
            history_entries = brand_context.get("caption_history") or brand_context.get("past_captions") or []
            if isinstance(history_entries, list):
                for entry in history_entries:
                    if isinstance(entry, dict):
                        caption = entry.get("caption")
                        if caption:
                            history.add(caption.strip().lower())
                    elif isinstance(entry, str):
                        history.add(entry.strip().lower())

        unique = []
        for caption in captions:
            key = caption.strip().lower()
            if not caption or key in seen or key in history:
                continue
            seen.add(key)
            unique.append(caption)
        return unique

    def _generate_template_captions(self, prompt: str, num_candidates: int) -> List[str]:
        topic = prompt.split()[0] if prompt else "life"
        templates = [t.format(topic=topic) for t in self.caption_templates]
        random.shuffle(templates)
        return templates[:num_candidates]

    def _generate_captions_openrouter(
        self,
        prompt: str,
        image_description: str,
        trends: Optional[List[str]],
        brand_context: Optional[Dict],
        num_candidates: int,
    ) -> List[str]:
        tone = (brand_context or {}).get("tone", "humorous")
        voice = (brand_context or {}).get("voice", "casual")
        brand_name = (brand_context or {}).get("brand_name", "the brand")
        trend_text = ", ".join(trends) if trends else "none"

        system_prompt = (
            "You are a social media strategist who writes fresh, viral meme captions. "
            "Produce short, punchy lines that feel native to internet culture. "
            "Avoid repeating the same structure, avoid generic phrases like 'hits different', "
            "and keep each caption unique."
        )

        user_prompt = (
            f"Original prompt: {prompt}\n"
            f"Image description: {image_description}\n"
            f"Brand voice: {voice}\n"
            f"Brand tone: {tone}\n"
            f"Brand name: {brand_name}\n"
            f"Relevant trends or references: {trend_text}\n"
            f"Write {num_candidates} distinct caption options. "
            "Format them as a simple list, one caption per line, no numbering needed."
        )

        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "CaptionGenerator",
        }
        payload = {
            "model": PROMPT_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)
            if response.status_code != 200:
                logger.error(f"OpenRouter caption error {response.status_code}: {response.text}")
                return []
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            captions = [self._clean_caption_line(line) for line in content.splitlines()]
            captions = [c for c in captions if len(c) > 3]
            return captions[:num_candidates]
        except Exception as e:
            logger.warning(f"OpenRouter caption generation failed: {e}")
            return []

    def _generate_captions_hf(
        self,
        prompt: str,
        image_description: str,
        num_candidates: int,
    ) -> List[str]:
        text_prompt = (
            f"Write {num_candidates} short, viral meme captions.\n"
            f"Prompt: {prompt}\n"
            f"Image context: {image_description}\n"
            "Keep them witty, concise, and varied. No numbering required."
        )
        payload = {"inputs": text_prompt, "parameters": {"max_new_tokens": 120, "temperature": 0.9}}

        try:
            resp = requests.post(
                f"{HF_API_TEXT_BASE}/{CAPTION_MODEL}",
                headers={"Authorization": f"Bearer {HF_TOKEN}"},
                json=payload,
                timeout=60,
            )
            if resp.status_code != 200:
                logger.error(f"Hugging Face caption error {resp.status_code}: {resp.text}")
                return []
            result = resp.json()
            if isinstance(result, list) and result:
                captions_raw = result[0].get("generated_text", "")
            elif isinstance(result, dict):
                captions_raw = result.get("generated_text", "")
            else:
                captions_raw = ""

            captions = [self._clean_caption_line(line) for line in captions_raw.splitlines()]
            captions = [c for c in captions if len(c) > 3]
            return captions[:num_candidates]
        except Exception as e:
            logger.warning(f"Hugging Face caption generation failed: {e}")
            return []

    def generate_captions(
        self,
        prompt: str,
        image_description: str,
        brand_context: Optional[Dict] = None,
        trends: Optional[List[str]] = None,
        num_candidates: int = 5,
    ) -> List[str]:
        captions = self._generate_captions_openrouter(
            prompt, image_description, trends, brand_context, num_candidates
        )

        if not captions:
            captions = self._generate_captions_hf(prompt, image_description, num_candidates)

        if not captions:
            captions = self._generate_template_captions(prompt, num_candidates)

        captions = self._dedupe_captions(captions, brand_context)
        if not captions:
            captions = self._generate_template_captions(prompt, num_candidates)

        random.shuffle(captions)
        return captions[:num_candidates]

    def _load_font(self, font_size: int) -> ImageFont.FreeTypeFont:
        font_candidates = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/System/Library/Fonts/Arial Unicode.ttf",
            "/Library/Fonts/Arial Unicode.ttf",
        ]
        for path in font_candidates:
            if Path(path).exists():
                try:
                    return ImageFont.truetype(path, font_size)
                except Exception:
                    continue
        return ImageFont.load_default()

    def _wrap_caption(self, draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:
        words = text.split()
        if not words:
            return text
        lines = []
        current = words[0]
        for word in words[1:]:
            test_line = f"{current} {word}"
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            if width <= max_width:
                current = test_line
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return "\n".join(lines)

    def add_caption_to_image(self, image: Image.Image, caption: str, brand_colors: Optional[List[str]] = None) -> Image.Image:
        img = image.copy()
        draw = ImageDraw.Draw(img)
        font_size = max(32, image.height // 18)
        font = self._load_font(font_size)
        max_text_width = int(image.width * 0.9)
        wrapped_caption = self._wrap_caption(draw, caption, font, max_text_width)
        bbox = draw.multiline_textbbox((0, 0), wrapped_caption, font=font, align="center", spacing=4)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (image.width - text_width) / 2
        y = image.height - text_height - font_size
        text_color = "white"
        outline_color = "black"
        if brand_colors:
            primary = brand_colors.get("primary") if isinstance(brand_colors, dict) else None
            if primary:
                text_color = primary
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx == 0 and dy == 0:
                    continue
                draw.multiline_text((x + dx, y + dy), wrapped_caption, font=font, fill=outline_color, align="center", spacing=4)
        draw.multiline_text((x, y), wrapped_caption, font=font, fill=text_color, align="center", spacing=4)
        return img

    def generate_meme(self, user_prompt: str, logo_path: Optional[str] = None, trends: Optional[List[str]] = None, brand_context: Optional[Dict] = None) -> Dict:
        start_time = time.time()
        try:
            logger.info("Step 1: Enhancing prompt via OpenRouter...")
            enhanced_prompt = self.enhance_prompt(user_prompt, trends)
            logger.info("Step 2: Generating image...")
            image_bytes = self.generate_image(enhanced_prompt)
            image = Image.open(io.BytesIO(image_bytes))
            logger.info("Step 3: Generating captions...")
            captions = self.generate_captions(
                user_prompt,
                "generated image",
                brand_context=brand_context,
                trends=trends,
            )
            best_caption = captions[0] if isinstance(captions, list) and captions else captions
            logger.info(f"Step 4: Overlaying caption '{best_caption}'...")
            brand_colors = None
            if brand_context and brand_context.get("colors"):
                brand_colors = brand_context["colors"]
            final_image = self.add_caption_to_image(image, best_caption, brand_colors)
            filename = f"meme_{int(time.time())}.png"
            path = OUTPUTS_DIR / filename
            final_image.save(path, "PNG", quality=95, optimize=True)
            logger.info(f"✅ Meme saved: {path}")
            return {
                "success": True,
                "filename": filename,
                "path": str(path),
                "caption": best_caption,
                "enhanced_prompt": enhanced_prompt,
                "image_description": "auto-generated meme image",
                "image_model": self.image_model_used,
                "prompt_model": self.prompt_enhancer_model_used,
                "generation_time": round(time.time() - start_time, 2),
                "metadata": {
                    "trends_used": trends or [],
                    "brand_colors": brand_colors,
                    "caption_options": captions,
                    "enhanced_prompt": enhanced_prompt,
                },
            }
        except Exception as e:
            logger.error(f"❌ Meme generation failed: {e}", exc_info=True)
            raise Exception(f"Failed to generate meme: {str(e)}")


# ==========================================================
# Singleton Helper
# ==========================================================
_ai_engine = None
def get_ai_engine() -> AIEngine:
    global _ai_engine
    if _ai_engine is None:
        _ai_engine = AIEngine()
    return _ai_engine
