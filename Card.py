import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Membership Card Generator",
    page_icon="Icon.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for center alignment and mobile responsiveness
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stApp {
        background-color: #1a1a1a !important;
    }

    .main .block-container {
        background-color: #2d2d2d !important;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
    }
    .stApp > header {
        background-color: transparent !important;
    }
    
    .title {
        text-align: center;
        color: #ffffff !important;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .subtitle {
        text-align: center;
        color: #b1b5b5 !important;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    
    .center-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .stButton > button {
        width: 100%;
        background-color: #0151ee !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #ffcf01 !important;
    }
    
    .download-section {
        margin-top: 2rem;
        padding: 1rem;
        border-radius: 10px;
        background-color: transparent !important;
        text-align: center;
    }

    /* Simple Download Button - Easy to read on dark background */
    .stDownloadButton > button,
    .download-section .stDownloadButton > button,
    div[data-testid="stDownloadButton"] > button {
        background-color: #0151ee !important;
        background: #0151ee !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(1, 81, 238, 0.3) !important;
        letter-spacing: 0.5px !important;
        min-height: 50px !important;
    }

    /* Force override any Streamlit default styles */
    .stDownloadButton button:not(:hover):not(:active):not(:focus) {
        background-color: #0151ee !important;
        background: #0151ee !important;
    }

    /* Input field labels - WHITE TEXT */
    .stTextInput label, .stFileUploader label {
        color: white !important;
    }

    .stTextInput > div > div > label {
        color: white !important;
    }

    .stFileUploader > div > div > label {
        color: white !important;
    }

    /* Help text under inputs */
    .stTextInput .help, .stFileUploader .help {
        color: #bdc3c7 !important;
    }

    /* Placeholder text */
    .stTextInput input::placeholder {
        color: #95a5a6 !important;
    }

    /* Expander header and content */
    .streamlit-expanderHeader {
        color: black !important;
        background-color: white !important;
    }

    .streamlit-expanderContent {
        color: white !important;
        background-color: #2c3e50 !important;
    }

    .streamlit-expanderContent p, 
    .streamlit-expanderContent li, 
    .streamlit-expanderContent strong {
        color: white !important;
    }

    /* Column content */
    .element-container {
        color: white !important;
    }

    /* General text elements */
    .markdown-text-container {
        color: white !important;
    }

    /* Horizontal line - THICK WHITE LINE */
    hr {
        border: none !important;
        height: 2px !important;
        background-color: #b1b5b5 !important;
        margin: 1rem 0 !important;
    }

    @media (max-width: 768px) {
        .title {
            font-size: 2rem;
        }
        .subtitle {
            font-size: 1rem;
        }
        
        /* Mobile download button - larger and more readable */
        .stDownloadButton > button,
        .download-section .stDownloadButton > button,
        div[data-testid="stDownloadButton"] > button {
            background-color: #0151ee !important;
            background: #0151ee !important;
            color: #ffffff !important;
            border: 2px solid #ffffff !important;
            border-radius: 12px !important;
            padding: 1.2rem 1rem !important;
            font-size: 1.1rem !important;
            font-weight: bold !important;
            letter-spacing: 0.5px !important;
            box-shadow: 0 4px 12px rgba(1, 81, 238, 0.4) !important;
            min-height: 50px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def create_membership_card(name, user_image):
    """
    Create membership card by overlaying user image and name on your template
    """
    try:
        # Load your card template (place your card image in the same folder)
        # Replace 'your_card_template.png' with your actual card file name
        template_path = "Template.jpg"  # Change this to your card image file name
        
        try:
            card = Image.open(template_path)
            card_width, card_height = card.size
        except FileNotFoundError:
            st.error(f"Template not found: {template_path}")
            st.error("Please make sure your card template is in the same folder as this script")
            return None
        
        # ====== ADJUST THESE COORDINATES FOR YOUR CARD ======
        # Photo position - change these values to match your card template
        photo_x = 674     # X position where photo should be placed
        photo_y = 354     # Y position where photo should be placed  
        photo_width = 850 # Width of the photo area
        photo_height = 1118 # Height of the photo area
        
        # Name position - change these values to match your card template
        name_y = 1760      # Y position where name should be placed (only Y needed, X will be auto-centered)
        name_font_size = 250  # Font size for the name
        name_color = "#ffffff"  # Name text color (you can change this)
        # =====================================================
        
        # Resize and position user image
        if user_image:
            # Make photo square and crop if needed
            user_img = user_image.copy()
            
            # Resize user image to fit photo area
            user_img = user_img.resize((photo_width, photo_height), Image.Resampling.LANCZOS)
            card.paste(user_img, (photo_x, photo_y))
        
        # Add name text (center-aligned horizontally)
        draw = ImageDraw.Draw(card)
        
        # Try to load custom font (Zuume or similar)
        try:
            # First try to load Zuume font (place zuume.ttf in same folder)
            name_font = ImageFont.truetype("Zuume SemiBold.ttf", name_font_size)
        except:
            try:
                # Try other common stylish fonts
                name_font = ImageFont.truetype("arial.ttf", name_font_size)
            except:
                try:
                    name_font = ImageFont.truetype("Arial.ttf", name_font_size)
                except:
                    name_font = ImageFont.load_default()
        
        # Calculate text width to center it horizontally
        text_bbox = draw.textbbox((0, 0), name, font=name_font)
        text_width = text_bbox[2] - text_bbox[0]
        
        # Calculate centered X position
        name_x = (card_width - text_width) // 2
        
        # Draw the centered text
        draw.text((name_x, name_y), name, fill=name_color, font=name_font)
        
        return card
        
    except Exception as e:
        st.error(f"Error creating card: {str(e)}")
        return None

def get_download_link(img, filename):
    """Generate download link for the image"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}" class="download-btn">📥 Download Membership Card</a>'
    return href

# Main app
def main():
    # Title and subtitle
    st.markdown('<h1 class="title">Multiomics Membership Card</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Create your personalized membership card</p>', unsafe_allow_html=True)
    
    # Center content container
    with st.container():
        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        
        # Input fields
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Name input
            name = st.text_input(
                "Enter Your Full Name",
                placeholder="Junaid Iqbal",
                
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Image upload
            uploaded_file = st.file_uploader(
                "Upload Your Photo",
                type=['png', 'jpg', 'jpeg'],
                
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Generate button
            if st.button("🎯 Generate Membership Card"):
                if name and uploaded_file:
                    with st.spinner("Creating your membership card..."):
                        # Load user image
                        user_image = Image.open(uploaded_file)
                        
                        # Create the card using your template
                        card = create_membership_card(name, user_image)
                        
                        if card:
                            st.success("✅ Membership card generated successfully!")
                            
                            # Display the card
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.image(card, caption="Your Membership Card", use_container_width=True)
                            
                            # Download section
                            st.markdown('<div class="download-section">', unsafe_allow_html=True)
                            
                            # Convert to bytes for download
                            buffered = io.BytesIO()
                            card.save(buffered, format="PNG")
                            
                            st.download_button(
                                label="📥 Download Membership Card",
                                data=buffered.getvalue(),
                                file_name=f"membership_card_{name.replace(' ', '_')}.png",
                                mime="image/png",
                                use_container_width=True
                            )
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                else:
                    if not name:
                        st.error("❌ Please enter your name")
                    if not uploaded_file:
                        st.error("❌ Please upload your photo")
        
        st.markdown('</div>', unsafe_allow_html=True)
    

    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #b1b5b5; font-size: 0.9rem;"> wemultiomics</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()