import os
import google.generativeai as genai
import streamlit as st
from PDF_Extractor import text_extractor
from wordextractor import doc_text_extract
from image2text import extract_text_image


# lets configire genai model 

gemini_key = os.getenv('GOOGLE_API_KEY2')
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite',
                              generation_config={'temperature':0.9})


# Lets create the sidebar

st.sidebar.title(':red[UPLOAD YOUR NOTES:]')
st.sidebar.subheader(':blue[Only upload Image, PDFs and DOCX]')
user_file = st.sidebar.file_uploader('upload Here:',
                                     type=['pdf','docx','png','jpf','jfif','jpeg'])

if user_file:
    st.sidebar.success('File Uploaded Successfully')
    if user_file.type == 'application/pdf':
        user_text = text_extractor(user_file)
    elif user_file.type in ['image/png', 'image/jpeg', 'image/jfif']:
        user_text = extract_text_image(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = doc_text_extract(user_file)
    else:
        st.sidebar.error('Enter the correct file type')
        
        
# Lets create the main page 

st.title(':orange[MoM Generator:-] :blue[AI Assisted Minutes of Meeting Generator]')
st.header(':violet[This application created generalised minutes of meeting]')
st.write('''
Follow the steps:-
1. Upload the notes in pdf, docx
2. Click "generate" to generate the MoM.''')


if st.button('Generate'):
    with st.spinner('please wait...'):
        prompt = f'''
        <Role> You are an expert in writing and formaring minutes of meetings.
        <Goal> Create minutes of meetings from the notes that user has provided.
        <Context> The user has provided some rough notes as text. Here are the notes : {user_text}
        <Format> The output must follow the below format
        * Title: assume title of the meeting.
        * Agenda: Assume agenda of the meeting.
        * Attendees: Name of the attendees (If name of the attendees is not there keep it NaN )
        * Date and Place: date and the place of the meeting (If not provided keep it Online)
        * Body: The body should follow the following sequences of points
            * Key points discussed.
            * Highlight any decision that has been taken.
            * Mention Actionable Items.
            * Mention any deadlines if discussed.
            * Next meeting date of discussed.
            * Add a 2-3 line of summary.
        <Instructions> 
        * Use bullet points and highlight the important keywords by making them bold.
        * Generate the output in docx format'''
        
        response = model.generate_content(prompt)
        st.write(response.text)
        
    if st.download_button(label='DOWNLOAD',
                           data=response.text,
                           file_name='mom_generated.txt',
                           mime='text/plain'):
        st.success('Your File has been downloaded')