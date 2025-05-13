import streamlit as st
import requests
import soundfile as sf
import io

st.set_page_config(page_title="RagaAI - Voice Financial Assistant", layout="centered")
st.title("🎙️ RagaAI: Voice-Powered Financial Assistant")

st.markdown("Speak a query like: **'What are the latest earnings for TSLA?'** or **'Give me a risk analysis on AAPL.'**")

# Upload audio file for voice query
audio_file = st.file_uploader("Upload your voice query (WAV format, <1MB)", type=["wav"])

if audio_file:
    st.audio(audio_file, format="audio/wav")
    audio_bytes = audio_file.read()

    if st.button("Submit Voice Query"):
        with st.spinner("Transcribing and processing..."):

            # 1. Transcribe using Voice Agent (Whisper endpoint)
            try:
                files = {'file': ("query.wav", audio_bytes, "audio/wav")}
                transcribe_response = requests.post("http://localhost:8005/transcribe", files=files)
                transcript = transcribe_response.json().get("text", "")

                st.success(f"Transcribed Query: {transcript}")
            except Exception as e:
                st.error(f"Transcription failed: {str(e)}")
                st.stop()

            # 2. Process via Orchestrator
            try:
                process_response = requests.post("http://localhost:8000/process_query", json={"query": transcript})
                result = process_response.json()
            except Exception as e:
                st.error(f"Orchestrator failed: {str(e)}")
                st.stop()

            # 3. Display results
            st.subheader("📋 Retrieved Context")
            st.json(result.get("retrieved_context", "No context"))

            if "analysis" in result:
                st.subheader("📊 Risk / Earnings Analysis")
                st.json(result["analysis"])

            if "stock_data" in result:
                st.subheader("💵 Stock Data")
                st.json(result["stock_data"])

            if "earnings_data" in result:
                st.subheader("📈 Earnings Reports")
                for item in result["earnings_data"]:
                    st.markdown(f"- {item.get('title', item)}")

            if "filings_data" in result:
                st.subheader("📄 SEC Filings")
                for item in result["filings_data"]:
                    st.markdown(f"- {item.get('title', item)}")

            if "news_data" in result:
                st.subheader("📰 Latest News")
                for item in result["news_data"]:
                    st.markdown(f"- {item.get('title', item)}")

            st.success("✅ Response sent to Text-to-Speech")

