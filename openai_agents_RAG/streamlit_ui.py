import streamlit as st
from pdf_backend import load_and_embed_pdf, ask_question_from_agent
import asyncio

st.set_page_config(page_title="PDF QA Agent", layout="centered")

st.title("🤖 PDF Question Answering Agent")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    # Save uploaded file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
        load_and_embed_pdf("temp.pdf")

    st.success("✅ PDF uploaded successfully!")
    
    st.success("PDF processed and embedded into knowledge base.")

    st.markdown("---")
    query = st.text_input("Ask a question related to this PDF:")

    if st.button("Ask"):
        if query:
            with st.spinner("Getting answer..."):
               
                answer = asyncio.run(ask_question_from_agent(query))  # ✅ Correct

                st.success("Answer:")
                st.write(answer)
        else:
            st.warning("Please enter a question.")





































# import streamlit as st
# from pdf_backend import load_and_embed_pdf, ask_question_from_agent
# import asyncio

# # App configuration
# st.set_page_config(page_title="PDF QA Agent", layout="wide")

# # Sidebar branding
# with st.sidebar:
#     st.markdown("## 📄 PDF QA Agent")
#     st.markdown("Easily upload a PDF and ask questions about its content using an AI-powered agent.")
#     st.markdown("---")
#     st.info("Developed by Tehreem Asghar 🚀", icon="💡")

# # Title
# st.markdown("<h1 style='text-align: center;'>🤖 PDF Question Answering Dashboard</h1>", unsafe_allow_html=True)
# st.markdown("### Upload your PDF and ask anything about its content below 👇")

# # Layout: Upload and Q&A in two columns
# col1, col2 = st.columns([1, 2])

# with col1:
#     st.markdown("#### 📤 Upload PDF")
#     uploaded_file = st.file_uploader("Choose your PDF file", type=["pdf"])

#     if uploaded_file:
#         with open("temp.pdf", "wb") as f:
#             f.write(uploaded_file.read())
#             load_and_embed_pdf("temp.pdf")
      


#         st.success("✅ PDF uploaded successfully!")
#         st.success("📚 PDF embedded into knowledge base.")
#         # with st.spinner("🔍 Processing and embedding PDF..."):
#         #  load_and_embed_pdf("temp.pdf")
#         # st.success("📚 PDF embedded into knowledge base.")

# with col2:
#     st.markdown("#### ❓ Ask a Question")
#     query = st.text_input("Type your question related to the uploaded PDF:")

#     # Ask button centered
#     ask_btn = st.button("Ask", key="ask_btn", use_container_width=True)

#     # Answer appears below input & button
#     if ask_btn:
#         if query.strip():
#             with st.spinner("🤔 Thinking..."):
#                 answer = asyncio.run(ask_question_from_agent(query))
#             st.markdown("#### ✅ Answer:")
#             st.markdown(
#                 f"<div style='background-color: #f0f2f6; padding: 15px; border-radius: 8px; font-size: 16px;'>{answer}</div>",
#                 unsafe_allow_html=True
#             )
#         else:
#             st.warning("Please enter a question before clicking Ask.")


# # Footer
# st.markdown("---")
# st.markdown("<p style='text-align: center; color: gray;'>© 2025 PDF QA Agent | Made with ❤️ by Tehreem</p>", unsafe_allow_html=True)























