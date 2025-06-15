import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from elevenlabs.core.api_error import ApiError  # ✅ Import the error class
from config import ELEVENLABS_API_KEY

elevenlabs = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def text_to_speech_file(text: str, folder: str) -> str:
    save_file_path = os.path.join(f"user_uploads/{folder}", "audio.mp3")

    try:
        # 🚀 Attempt to call ElevenLabs
        response = elevenlabs.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Adam
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
                speed=1.0,
            ),
        )

        # Save audio response to file
        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        print(f"{save_file_path}: A new audio file was saved successfully!")

    except ApiError as e:
        # ⚠️ Handle the API block without crashing the app
        print("❌ ElevenLabs API Error:", e)
        # Write silent or fallback audio (or skip)
        with open(save_file_path, "wb") as f:
            f.write(b"")  # Empty file or your own fallback bytes
        print("⚠️ Wrote fallback audio due to API error.")

    return save_file_path
