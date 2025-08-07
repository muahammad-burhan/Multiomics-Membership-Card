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

# Custom CSS for modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main > div {
        padding-top: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%) !important;
    }

    .main .block-container {
        background: linear-gradient(145deg, #2a2a2a, #343434) !important;
        padding: 3rem;
        border-radius: 24px;
        margin-top: 2rem;
        box-shadow: 
            0 25px 50px -12px rgba(0, 0, 0, 0.8),
            0 0 0 1px rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stApp > header {
        background-color: transparent !important;
    }
    
    .title {
        text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        margin-bottom: 1rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        text-align: center;
        color: #a1a1aa !important;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        font-weight: 400;
        opacity: 0.8;
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
        background: linear-gradient(135deg, #0151ee 0%, #0a4fd8 100%) !important;
        color: white !important;
        border-radius: 16px;
        border: none;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 10px 25px -5px rgba(1, 81, 238, 0.4),
            0 0 0 1px rgba(1, 81, 238, 0.1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ffcf01 0%, #f59e0b 100%) !important;
        transform: translateY(-2px);
        box-shadow: 
            0 20px 40px -5px rgba(255, 207, 1, 0.4),
            0 0 0 1px rgba(255, 207, 1, 0.2);
    }
    
    .download-section {
        margin-top: 2rem;
        padding: 1rem;
        border-radius: 16px;
        background: transparent !important;
        text-align: center;
    }

    /* Modern Download Button */
    .stDownloadButton > button,
    .download-section .stDownloadButton > button,
    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #0151ee 0%, #0a4fd8 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 1rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        box-shadow: 
            0 10px 25px -5px rgba(1, 81, 238, 0.4),
            0 0 0 1px rgba(1, 81, 238, 0.1) !important;
        letter-spacing: 0.01em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 
            0 15px 35px -5px rgba(1, 81, 238, 0.5),
            0 0 0 1px rgba(1, 81, 238, 0.2) !important;
    }

    /* Force override any Streamlit default styles */
    .stDownloadButton button:not(:hover):not(:active):not(:focus) {
        background: linear-gradient(135deg, #0151ee 0%, #0a4fd8 100%) !important;
    }

    /* Modern Input Labels */
    .stTextInput label, .stFileUploader label {
        color: #f4f4f5 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }

    .stTextInput > div > div > label {
        color: #f4f4f5 !important;
        font-weight: 500 !important;
    }

    .stFileUploader > div > div > label {
        color: #f4f4f5 !important;
        font-weight: 500 !important;
    }

    /* Modern Text Input */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput input:focus {
        border: 1px solid #0151ee !important;
        box-shadow: 0 0 0 3px rgba(1, 81, 238, 0.1) !important;
        outline: none !important;
    }

    /* Modern File Upload */
    .stFileUploader > div > div > div {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.08)) !important;
        border: 2px dashed rgba(1, 81, 238, 0.6) !important;
        border-radius: 16px !important;
        padding: 2rem 1rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }

    .stFileUploader > div > div > div:hover {
        border-color: #0151ee !important;
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.1)) !important;
    }

    .stFileUploader > div > div > div > div {
        color: #e4e4e7 !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
    }

    /* Modern Browse Button */
    .stFileUploader button {
        background: linear-gradient(135deg, #374151 0%, #4b5563 100%) !important;
        color: #f9fafb !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        margin-top: 0.75rem !important;
        display: inline-block !important;
        visibility: visible !important;
        transition: all 0.2s ease !important;
        font-size: 0.9rem !important;
    }

    .stFileUploader button:hover {
        background: linear-gradient(135deg, #4b5563 0%, #6b7280 100%) !important;
        transform: translateY(-1px);
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        min-height: 120px !important;
    }

    /* Modern Help Text */
    .stTextInput .help, .stFileUploader .help {
        color: #9ca3af !important;
        font-size: 0.85rem !important;
    }

    /* Modern Placeholder */
    .stTextInput input::placeholder {
        color: #6b7280 !important;
        opacity: 0.8 !important;
    }

    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(90deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%);
        border: 1px solid rgba(34, 197, 94, 0.2);
        border-radius: 12px;
    }

    .stError {
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 12px;
    }

    /* Modern Spinner */
    .stSpinner {
        color: #0151ee !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
        color: #1e293b !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
    }

    .streamlit-expanderContent {
        background: linear-gradient(145deg, #2d3748, #374151) !important;
        color: #f7fafc !important;
        border-radius: 0 0 12px 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Modern HR */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.2) 50%, transparent 100%) !important;
        margin: 2rem 0 !important;
    }

    /* Mobile optimizations */
    @media (max-width: 768px) {
        .title {
            font-size: 2.2rem;
        }
        .subtitle {
            font-size: 1rem;
        }
        
        .main .block-container {
            padding: 2rem 1.5rem;
            border-radius: 20px;
        }
        
        /* Mobile download button */
        .stDownloadButton > button,
        .download-section .stDownloadButton > button,
        div[data-testid="stDownloadButton"] > button {
            background: linear-gradient(135deg, #0151ee 0%, #0a4fd8 100%) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 14px !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            box-shadow: 
                0 8px 20px -5px rgba(1, 81, 238, 0.4),
                0 0 0 1px rgba(1, 81, 238, 0.1) !important;
            min-height: 50px !important;
        }

        /* Mobile file upload improvements */
        .stFileUploader > div > div > div {
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.08)) !important;
            border: 2px dashed rgba(1, 81, 238, 0.6) !important;
            border-radius: 14px !important;
            padding: 1.5rem 1rem !important;
            min-height: 100px !important;
        }

        .stFileUploader button {
            background: linear-gradient(135deg, #374151 0%, #4b5563 100%) !important;
            color: #f9fafb !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 0.7rem 1.2rem !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            margin-top: 0.8rem !important;
            width: auto !important;
            display: block !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        .stFileUploader [data-testid="stFileUploaderDropzone"] {
            min-height: 100px !important;
        }

        .stFileUploader > div > div > div > div {
            color: #e4e4e7 !important;
            font-size: 0.9rem !important;
            line-height: 1.4 !important;
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