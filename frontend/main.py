import streamlit as st
import requests
import re

# Set wide layout to comfortably accommodate side-by-side city feed columns
st.set_page_config(page_title="Emergency Text Routing Network", layout="wide")

BACKEND_URL = "http://live-pipeline-engine:5000"

def strip_emojis(text):
    """Removes emojis from backend strings to maintain a completely clean, text-only profile."""
    return re.sub(r'[^\x00-\x7F]+', '', text).strip()

def render_tweet_card(text, classification):
    """Renders a structural, rectangular card with conditional coloring based on safety status."""
    if classification == "ALERT":
        # Crimson red border and soft pink background for immediate emergency visibility
        bg_color = "#FFEBEE"
        border_color = "#D32F2F"
        text_color = "#B71C1C"
        badge_html = f"<span style='color: white; background-color: #D32F2F; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;'>ALERT</span>"
    else:
        # Subtle charcoal text and clean gray borders for standard messages
        bg_color = "#F8F9FA"
        border_color = "#E0E0E0"
        text_color = "#212121"
        badge_html = f"<span style='color: #616161; background-color: #E0E0E0; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;'>NON-ALERT</span>"

    card_html = f"""
    <div style="
        background-color: {bg_color};
        border-left: 5px solid {border_color};
        border-top: 1px solid {border_color};
        border-right: 1px solid {border_color};
        border-bottom: 1px solid {border_color};
        padding: 14px;
        border-radius: 6px;
        margin-bottom: 14px;
        color: {text_color};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    ">
        <p style="margin: 0 0 10px 0; font-size: 14px; line-height: 1.5; font-weight: 500;">{text}</p>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 11px; color: #757575; text-transform: uppercase; letter-spacing: 0.5px;">Classification Sequence</span>
            {badge_html}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


# --- UI HEADERS ---
st.title("Live Text Routing and Analysis Console")
st.markdown("---")

# --- LEFT COLUMN: INPUT & STAGE PIPELINE ---
# --- RIGHT COLUMN: LIVE RECTANGULAR CITY FEEDS ---
col_input, col_feeds = st.columns([1, 2])

with col_input:
    st.markdown("### Data Ingestion Gateway")
    
    # Text Stream Ingestion Panel
    tweet_input = st.text_area("Textual Sequence:", height=120, placeholder="Type message here...")
    
    # Target City Router Selection
    target_city = st.selectbox(
        "Select target distribution region:",
        ["Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad"]
    )
    
    submit_btn = st.button("Route and Process Text Pipeline", use_container_width=True)
    
    # Pipeline Logging Console (Maintains stage-by-stage visual tracking)
    if submit_btn and tweet_input.strip():
        st.markdown("---")
        st.markdown("### Stage Processing Logs")
        
        payload = {"text": tweet_input, "location": target_city}
        
        try:
            with st.spinner("Executing sequence calculations..."):
                response = requests.post(f"{BACKEND_URL}/submit_tweet", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                # Render each processing step tracking metric cleanly without emojis
                for log_step in result.get("logs", []):
                    clean_log = strip_emojis(log_step)
                    if "Error" in clean_log or "Failure" in clean_log:
                        st.error(clean_log)
                    elif "Warning" in clean_log:
                        st.warning(clean_log)
                    elif "complete" in clean_log.lower() or "locked" in clean_log.lower():
                        st.success(clean_log)
                    else:
                        st.text(clean_log)
                        
            else:
                st.error(f"Pipeline error encountered. Status Code: {response.status_code}")
        except Exception as e:
            st.error(f"Unable to establish gateway connection to routing engine. Details: {str(e)}")


with col_feeds:
    st.markdown("### Regional Live Feed Modules")
    
    # Establish regional layout blocks side-by-side using Streamlit columns
    city_list = ["Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad"]
    feed_cols = st.columns(len(city_list))
    
    # Create a mapping container to keep UI clean and maintain state organization
    city_containers = {}
    for i, city in enumerate(city_list):
        with feed_cols[i]:
            st.markdown(f"<h4 style='text-align: center; color: #424242; border-bottom: 2px solid #E0E0E0; padding-bottom: 5px;'>{city}</h4>", unsafe_allow_html=True)
            # Create a dedicated column space for each specific city's cards
            city_containers[city] = st.container()

    # Fetch total structured timeline historical rows straight from PostgreSQL cluster via Flask
    try:
        feed_response = requests.get(f"{BACKEND_URL}/get_feeds")
        if feed_response.status_code == 200:
            tweets_data = feed_response.json()
            
            # Counter tracking map to verify if a city's feed box remains completely clear
            items_routed_to_city = {city: 0 for city in city_list}
            
            # Iterate through data payloads and route them into their target city's container
            for tweet in tweets_data:
                location = tweet.get("location", "Bangalore")
                text = tweet.get("text", "")
                classification = tweet.get("classification", "NON-ALERT")
                
                if location in city_containers:
                    items_routed_to_city[location] += 1
                    with city_containers[location]:
                        render_tweet_card(text, classification)
            
            # Fallback text placeholder if a structural rectangular column block has no incoming text metrics yet
            for city in city_list:
                if items_routed_to_city[city] == 0:
                    with city_containers[city]:
                        st.markdown("<p style='color: #9E9E9E; font-size: 12px; text-align: center; font-style: italic; margin-top: 20px;'>No active traffic logs</p>", unsafe_allow_html=True)
                        
    except Exception as e:
        st.info("Awaiting initial database sync or pipeline transaction records...")