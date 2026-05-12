import streamlit as st
from groq import Groq
import requests

# Groq API Key Setup
client = Groq(
    api_key="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",
)

# Page Layout
st.set_page_config(page_title="Jarvis AI", page_icon="🤖")
st.title("🤖 Jarvis System Online (Fixed)")
st.markdown("---")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            # Har message ke liye unique download button
            st.download_button(
                label="📥 Download Answer",
                data=message["content"],
                file_name=f"jarvis_response_{i}.txt",
                mime="text/plain",
                key=f"download_{i}"
            )

# User Input
if query := st.chat_input("Aap kuch poochein..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate Response
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are Jarvis. Always answer in short Roman Urdu."},
                {"role": "user", "content": query}
            ],
            # Yahan naya model add kar diya hai taake Error 400 na aaye
            model="llama-3.1-8b-instant", 
        )
        
        full_response = chat_completion.choices[0].message.content

        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        with st.chat_message("assistant"):
            st.markdown(full_response)
            
            # Download Button for the latest response
            st.download_button(
                label="📥 Download Answer",
                data=full_response,
                file_name="jarvis_latest.txt",
                mime="text/plain",
                key=f"dl_{len(st.session_state.messages)}"
            )
            
            st.info("💡 Copy karne ke liye text ko select karein, browser khud option de dega.")

    except Exception as e:
        st.error(f"Error: {e}")