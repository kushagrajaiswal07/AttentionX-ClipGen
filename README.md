# 🎬 ClipGen AI - AttentionX Hackathon

**Automated Content Repurposing Engine** built for the AttentionX Hackathon to turn long-form educational content into viral, snackable vertical videos.

## 🚀 The Solution
Mentors and creators produce high-value long-form content, but modern audiences consume information in 60-second bursts. ClipGen AI solves this by automatically finding the "golden nuggets" in a video and reformatting them for TikTok/Reels.

### ✨ Key Features Implemented:
* **🤖 Identify "Emotional Peaks":** Integrated Google Gemini 1.5 Flash to analyze transcript segments and calculate the 3 most engaging 15+ second highlights.
* **📱 Smart-Crop to Vertical:** Built an OpenCV-powered computer vision pipeline to track the speaker's face and dynamically center them in a 9:16 vertical crop.
* **🔥 Dynamic Captions & Hooks:** Leveraged Gemini to generate custom, viral "hook" headlines for each clip, and utilized OpenCV to permanently draw high-contrast, attention-grabbing banners onto every frame.
* **💻 Modern UI:** Created a sleek, dark-mode web interface using Pico.css with responsive grids and async loading states.

## 📹 Live Demo
**https://drive.google.com/file/d/1xKFODS3OfaOnHOt0gPqUSfCqeN6DFGPb/view?usp=drive_link** 

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **AI & NLP:** Google Gemini 1.5 Flash API, OpenAI Whisper (Speech-to-Text)
* **Video & Image Processing:** MoviePy 2.0, OpenCV (Haar Cascades for face detection)
* **Frontend:** HTML5, JS, Pico.css

## ⚙️ How to Run Locally
1. Clone the repository: `git clone https://github.com/kushagrajaiswal07/AttentionX-ClipGen`
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment and install dependencies:
   `pip install flask moviepy opencv-python google-generativeai openai-whisper`
4. Add your Google Gemini API key to `utils/highlight_detection.py`.
5. Run the server: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.
