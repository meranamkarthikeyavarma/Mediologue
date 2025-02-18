# from flask import Flask, request, jsonify
# from huggingface_hub import InferenceClient
# import os
# import whisper

# app = Flask(__name__)


# HF_TOKEN = "hf2"  
# repo_id = "microsoft/Phi-3-mini-4k-instruct"


# SAVE_FOLDER = r"D:\Seeta\Audios"
# os.makedirs(SAVE_FOLDER, exist_ok=True)

# @app.route('/upload', methods=['POST'])
# def upload_audio():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
    
#     audio_file = request.files['audio']
#     file_path = os.path.join(SAVE_FOLDER, "recording.wav")
    
#     audio_file.save(file_path)


#     os.environ["PATH"] += os.pathsep + r"C:\Users\apjmu\Downloads\ffmpeg-7.1-essentials_build\ffmpeg-7.1-essentials_build\bin"

#     model = whisper.load_model("medium")
#     print("Model loaded successfully")

#     result = model.transcribe(r"D:\Seeta\Audios\recording.wav", language="en")

#     text_values = [segment['text'] for segment in result['segments']]

#     # for text in text_values:
#     #     print(text)

#     return jsonify({"message": "File saved successfully", "path": file_path})

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)


from flask import Flask, request, jsonify
from huggingface_hub import InferenceClient
import os
import whisper
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

HF_TOKEN = "hf"  
repo_id = "microsoft/Phi-3-mini-4k-instruct"

llm_client = InferenceClient(model=repo_id, token=HF_TOKEN, timeout=120)

SAVE_FOLDER = r"D:\Seeta\Audios"
os.makedirs(SAVE_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    audio_file = request.files['audio']
    file_path = os.path.join(SAVE_FOLDER, "recording.wav")
    print("Save File Check")
    audio_file.save(file_path)

    print("File Saved Successfully")

    os.environ["PATH"] += os.pathsep + r"C:\Users\apjmu\Downloads\ffmpeg-7.1-essentials_build\ffmpeg-7.1-essentials_build\bin"

    model = whisper.load_model("medium")
    print("Model loaded successfully")

    file_path2 = "D:\\Seeta\\backend\\audio.wav"

    result = model.transcribe(file_path2, language="en")
    transcribed_text = " ".join(segment['text'] for segment in result.get('segments', []))
    print("transcribe_text", transcribed_text)

    # Few-shot prompt for better extraction
    prompt = f"""You are a medical assistant extracting structured patient data from doctor-patient conversations.
    Extract key details like symptoms, duration, and medication history.

    ### Example 1:
    *Conversation:*
    "I have been feeling very fatigued for the past few days."
    "I feel tired even after a full night's sleep, and I’ve noticed some shortness of breath when climbing stairs."
    "Is the fatigue constant or does it fluctuate?"
    "It’s pretty constant."
    "Sometimes I feel slightly better in the morning, but by the afternoon, I’m exhausted again."
    "Have you had any chest pain or discomfort?"
    "Yes"
    "I’ve had a tight feeling in my chest, but it’s not sharp. It just feels heavy, especially after I exert myself."

    *Extracted Data:*
    - Symptoms: Fatigue, shortness of breath, chest tightness
    - Duration: Fatigue for several days
    - Medication History: None

    ### Example 2:
    *Conversation:*
    "I’ve been having a sore throat and a cough for the past three days."
    "The sore throat is especially worse in the mornings, and it feels scratchy."
    "Does the sore throat get worse with swallowing?"
    "Yes"
    "It does. When I swallow, it feels like something is stuck in my throat. It’s also painful when I talk for too long."
    "Have you had any fever or chills?"
    "Yes, I had a mild fever yesterday, but it went down after I took some paracetamol."

    *Extracted Data:*
    - Symptoms: Sore throat, cough, mild fever
    - Duration: Sore throat and cough for 3 days
    - Medication History: Paracetamol for fever

    ### Now extract data from this conversation:
    *Conversation:*
    {transcribed_text}

    *Extracted Data:*"""

    print("prompt check")

    phi3_response = llm_client.text_generation(prompt, max_new_tokens=100)

    print("prompt check -2")

    print(phi3_response)

    return jsonify({
        "message": "File saved and transcribed successfully",
        "transcribed_text": transcribed_text,
        "structured_data": phi3_response.strip()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

