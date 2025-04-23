import streamlit as st
import re
from io import StringIO

# Initialize session state if not already initialized
if 'documents' not in st.session_state:
    st.session_state.documents = [{
        "title": "Sample Mail Template",
        "content": """
Dear [Hiring Manager's Name],

I hope this message finds you well.

I am writing to express my interest in the AI/ML Engineer position at [Company Name], as advertised on [Job Board/Company Website]. With a strong background in developing end-to-end AI solutions, including LLM-powered assistants and cloud-based analytics dashboards, I am eager to contribute to your team's success.

Please find my resume and portfolio attached for your review. I look forward to the opportunity to discuss how my skills align with your company's needs.

Thank you for considering my application.
"""
    }]

if 'active_doc' not in st.session_state:
    st.session_state.active_doc = 0

# Main function
def main():
    st.title("Mail Editor")
    
    # Sidebar for document management
    with st.sidebar:
        st.header("Document Management")
        
        # Add new document
        st.subheader("Add New Document")
        new_doc_title = st.text_input("Document Title", key="new_doc_title")
        
        # Text area for new document content
        new_doc_content = st.text_area("Document Content", height=100, key="new_doc_content")
        
        if st.button("Add Document"):
            if new_doc_title:
                st.session_state.documents.append({
                    "title": new_doc_title,
                    "content": new_doc_content
                })
                st.success(f"Added document: {new_doc_title}")
            else:
                st.error("Please provide a document title")
        
        # File upload option
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader("Choose a text file", type=['txt'])
        if uploaded_file is not None:
            content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            st.session_state.documents.append({
                "title": uploaded_file.name,
                "content": content
            })
            st.success(f"Uploaded document: {uploaded_file.name}")
        
        # Document selection
        st.subheader("Select Document")
        doc_titles = [doc["title"] for doc in st.session_state.documents]
        selected_doc_index = st.selectbox(
            "Choose a document to edit",
            range(len(doc_titles)),
            format_func=lambda i: doc_titles[i],
            key="doc_selector"
        )
        
        st.session_state.active_doc = selected_doc_index
        
        # Delete document button
        if len(st.session_state.documents) > 1:  # Prevent deleting all documents
            if st.button("Delete Current Document"):
                del st.session_state.documents[st.session_state.active_doc]
                st.session_state.active_doc = 0
                st.rerun()
    
    # Main content area
    active_doc = st.session_state.documents[st.session_state.active_doc]
    
    # Text replacement interface
    st.subheader("Text Replacement")
    col1, col2 = st.columns(2)
    
    with col1:
        target_text = st.text_input("Find:", placeholder="Enter text to replace", key="target")
    
    with col2:
        replacement_text = st.text_input("Replace with:", placeholder="Enter replacement text", key="replacement")
    
    if st.button("Replace All Occurrences"):
        if target_text:
            # Replace all occurrences
            original_content = active_doc["content"]
            updated_content = original_content.replace(target_text, replacement_text)
            
            # Count replacements
            count = original_content.count(target_text)
            
            # Update document
            active_doc["content"] = updated_content
            
            if count > 0:
                st.success(f"Replaced {count} occurrences of '{target_text}'")
            else:
                st.info(f"No occurrences of '{target_text}' found")
        else:
            st.warning("Please enter text to find")
    
    # Document display and editing
    st.subheader(f"Editing: {active_doc['title']}")
    
    # Allow direct editing of the document
    edited_content = st.text_area(
        "Edit document content:", 
        value=active_doc["content"],
        height=300,
        key="doc_editor"
    )
    
    # Update document content if edited
    if edited_content != active_doc["content"]:
        active_doc["content"] = edited_content
    
    # Preview section
    st.subheader("Preview")
    st.code(active_doc["content"], wrap_lines=True)

# Run the app
if __name__ == "__main__":
    main()