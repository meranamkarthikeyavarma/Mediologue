import { useState, useRef } from "react";

const MedicalDataExtraction = () => {
    const [recording, setRecording] = useState(false);
    const [audioURL, setAudioURL] = useState(null);
    const [transcribedText, setTranscribedText] = useState("Waiting for response...");
    const [medicalData, setMedicalData] = useState("Waiting for response...");
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            audioChunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (event) => {
                audioChunksRef.current.push(event.data);
            };

            mediaRecorderRef.current.onstop = async () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
                const audioUrl = URL.createObjectURL(audioBlob);
                setAudioURL(audioUrl);

                const formData = new FormData();
                formData.append("audio", audioBlob, "recording.wav");

                try {
                    const response = await fetch("http://127.0.0.1:5000/upload", {
                        method: "POST",
                        body: formData,
                    });
                    const result = await response.json();
                    setTranscribedText(result.transcribed_text || "No transcription available.");
                    setMedicalData(result.structured_data || "No extracted data.");
                } catch (error) {
                    console.error("Error uploading file:", error);
                    setTranscribedText("Error processing audio.");
                    setMedicalData("Error extracting data.");
                }
            };

            mediaRecorderRef.current.start();
            setRecording(true);
        } catch (error) {
            console.error("Error accessing microphone:", error);
            alert("Could not access microphone. Please check your settings.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current) {
            mediaRecorderRef.current.stop();
            setRecording(false);
        }
    };

    return (
        <div className="container bg-gray-100 p-6 text-center">
            <h2 className="text-2xl font-bold text-gray-800">Real-Time Medical Data Extraction</h2>
            <div className="mt-4">
                <button 
                    className="px-4 py-2 text-white rounded bg-green-600 hover:bg-green-700 disabled:opacity-50"
                    onClick={startRecording} 
                    disabled={recording}
                >
                    Start Recording
                </button>
                <button 
                    className="px-4 py-2 ml-2 text-white rounded bg-red-600 hover:bg-red-700 disabled:opacity-50"
                    onClick={stopRecording} 
                    disabled={!recording}
                >
                    Stop Recording
                </button>
            </div>

            {audioURL && (
                <audio className="mt-4" controls src={audioURL}></audio>
            )}

            <div className="mt-6 p-4 bg-white shadow-md rounded text-left max-w-xl mx-auto">
                <p className="font-bold">Transcribed Text:</p>
                <p>{transcribedText}</p>
                <p className="font-bold mt-4">Extracted Medical Data:</p>
                <p>{medicalData}</p>
            </div>
        </div>
    );
};

export default MedicalDataExtraction;
