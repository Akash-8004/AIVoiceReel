# 🎙️ AI Voice Reel

> A web app that converts text to voice and generates video reels using AI. Built with Flask and ElevenLabs.

---

## 🚀 Features

- Text-to-audio conversion using ElevenLabs  
- Automatic video reel generation  
- Web interface with gallery and upload support  
- Audio cleanup and processing  

---

## 🛠️ How to Run Locally

1. **Clone the repo**

   ```bash
   git clone https://github.com/Akash-8004/AIVoiceReel.git
   cd AIVoiceReel
   ```

2. **Create virtual environment and activate it**

   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Uncomments important Functions from code
     from file - generate_process.py/ Function - def process_folder(folder):
        #text_to_audio(folder)
        #create_reel(folder)

4. **Run the app**

   ```bash
   python main.py
   ```

---

## 🧠 Tech Stack

- Python  
- Flask  
- ElevenLabs API  
- HTML/CSS  
- JavaScript (for UI enhancements)  

---

## 📂 Project Structure

```
AIVoiceReel/
│
├── static/             # Images, CSS, and video reels
│   ├── css/
│   ├── reels/
│   └── *.jpg
│
├── templates/          # HTML templates
│
├── main.py             # App entry point
├── text_to_audio.py    # Voice generation logic
├── generate_process.py
├── cleanup.py
├── config.py
├── requirements.txt
└── .gitignore
```

---

## 📜 License

This project is licensed under the **MIT License**.
