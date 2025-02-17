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
"I have been feeling very fatigued for the past few days."
" I feel tired even after a full night's sleep, and I’ve noticed some shortness of breath when climbing stairs."
"Is the fatigue constant or does it fluctuate?"
"It’s pretty constant."
" Sometimes I feel slightly better in the morning, but by the afternoon, I’m exhausted again."
"Have you had any chest pain or discomfort?"
"Yes"
" I’ve had a tight feeling in my chest, but it’s not sharp. It just feels heavy, especially after I exert myself."

*Extracted Data:*
- Symptoms: Fatigue, shortness of breath, chest tightness
- Duration: Fatigue for several days
- Medication History: None

### Example 2:
*Conversation:*
"I’ve been having a sore throat and a cough for the past three days."
" The sore throat is especially worse in the mornings, and it feels scratchy."
"Does the sore throat get worse with swallowing?"
"Yes"
" it does. When I swallow, it feels like something is stuck in my throat. It’s also painful when I talk for too long."
"Have you had any fever or chills?"
"Yes, I had a mild fever yesterday, but it went down after I took some paracetamol."

*Extracted Data:*
- Symptoms: Sore throat, cough, mild fever
- Duration: Sore throat and cough for 3 days
- Medication History: Paracetamol for fever

### Now extract data from this conversation:
*Conversation:*
"What is the problem?"
 "I have been having a swelling in my voice for the past 2 days."
 "I think I also have  fever."
 "Is there any problem while eating due to swelling?"
 "Yes, there is a problem while eating."
 "But I don't feel any problem while drinking."
 "Did you take the medication?"
 "Yes, I took it from my childhood."
 "I contacted doctors and they prescribed some medicines."
 "and I am using those medicines".
 "Did you take the medicine for fever?"
 "Yes, I took it."
 "Is any of  your family have this problem of  swelling?"
 "Yes, my father has it."
 "Doctors said that they inherited it from my father."
 "I also think it might be."
 "I will prescribe some medicines."
 "Follow them."
 "It will be fine."

*Extracted Data:*"""

# Make API call to Phi-3 model
response = llm_client.text_generation(prompt, max_new_tokens=100)

# Print the extracted structured data
print(response)
