import streamlit as st
#from annotated_text import annotated_text
def render_annotations(text, annotations):
    annotated_text = ""
    current_idx = 0

    for ann in sorted(annotations, key=lambda x: x["start"]):
        # Add plain text before the annotation
        annotated_text += text[current_idx:ann["start"]]
        # Add the annotated text
        annotated_text += f'<span style="background-color: #8ef;">{ann["text"]} ({ann["label"]})</span>'
        current_idx = ann["end"]

    # Add the remaining text
    annotated_text += text[current_idx:]
    return annotated_text

# Initialize session state for labels and annotations
if "labels" not in st.session_state:
    st.session_state.labels = []
if "annotations" not in st.session_state:
    st.session_state.annotations = []

# Title
st.title("Interactive Text Annotation Tool")

# Section 1: Define Labels
st.header("Step 1: Define Labels")
new_label = st.text_input("Enter a new label:")
if st.button("Add Label"):
    if new_label and new_label not in st.session_state.labels:
        st.session_state.labels.append(new_label)
        st.success(f"Label '{new_label}' added!")
    elif new_label in st.session_state.labels:
        st.warning(f"Label '{new_label}' already exists.")
    else:
        st.error("Label cannot be empty.")

st.write("### Current Labels")
st.write(st.session_state.labels)

# Section 2: Annotate Text
st.header("Step 2: Annotate Text")
text = st.text_area("Enter the text you want to annotate:")

if text and st.session_state.labels:
    st.subheader("Annotate Text")
    annotated = []

    # Display the text with existing annotations
    for ann in st.session_state.annotations:
        annotated.append((ann["text"], ann["label"], "#8ef"))

    if annotated:
        st.markdown(render_annotations(text, st.session_state.annotations), unsafe_allow_html=True)
    else:
        st.write(text)


    # Selection box for label
    selected_label = st.selectbox("Select Label", st.session_state.labels)

    # Add annotation button
    selected_text = st.text_input("Enter the text you want to label (copy-paste from the text above):")
    if st.button("Add Annotation"):
        if selected_text in text:
            start_idx = text.index(selected_text)
            end_idx = start_idx + len(selected_text)
            annotation = {
                "text": selected_text,
                "label": selected_label,
                "start": start_idx,
                "end": end_idx,
            }
            st.session_state.annotations.append(annotation)
            st.success(f"Annotation for '{selected_text}' as '{selected_label}' added!")
        else:
            st.error("Selected text not found in the input text.")

# Section 3: View and Download Annotations
if st.session_state.annotations:
    st.header("Step 3: View and Download Annotations")
    st.write("### Annotations")
    st.json(st.session_state.annotations)

    # Download Annotations
    import json
    annotations_json = json.dumps(st.session_state.annotations, indent=4)
    st.download_button("Download Annotations as JSON", annotations_json, file_name="annotations.json")
else:
    st.warning("No annotations added yet.")
