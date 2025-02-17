from huggingface_hub import InferenceClient

# Use your Hugging Face API token
HF_TOKEN = ""  # Replace with your token
repo_id = "microsoft/Phi-3-mini-4k-instruct"

# Initialize API client
llm_client = InferenceClient(model=repo_id, token=HF_TOKEN, timeout=120)

# Few-shot prompt for medical data extraction
prompt = """You are a medical assistant extracting structured patient data from doctor-patient conversations.
Extract key details like symptoms, duration, and medication history.

### Example 1:
*Conversation:*
Patient: "I've had a fever and cough for three days. Feeling very tired."
Doctor: "Are you taking any medication?"
Patient: "No."

*Extracted Data:*
- Symptoms: Fever, cough, fatigue since 3 days
- Medication History: None

### Example 2:
*Conversation:*
Patient: "I have stomach pain and nausea since yesterday. I also have diarrhea."
Doctor: "Did you eat anything unusual?"
Patient: "Not sure, but I had street food two days ago."
Doctor: "Any medication?"
Patient: "No."

*Extracted Data:*
- Symptoms: Stomach pain, nausea, diarrhea since 1 day
- Medication History: None

### Now extract data from this conversation:
*Conversation:*
Patient: "I feel weak and have chills. Vomiting for two days, headace, stomach ace, leg pain , ears pain and I can’t eat."
Doctor: "Did you check your temperature?"
Patient: "No, but I feel hot."
Doctor: "Any medication?"
Patient: "Nothing."

*Extracted Data:*"""

# Make API call to Phi-3 model
response = llm_client.text_generation(prompt, max_new_tokens=100)

# Print the extracted structured data
print(response)