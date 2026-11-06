import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import uuid
from io import BytesIO
from datetime import datetime, timedelta
from pandas.errors import EmptyDataError
import joblib

from notifications import send_email

from underground_preprocessing import preprocess_input, predict as underground_predict, load_artifacts
st.markdown("""
<style>

/* Sidebar radio container */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    /*gap: 10px;*/
}

/* Each radio option label */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: #4285F4;
    box-shadow: 10px 10px 10px grey;
    padding: 10px 10px;
    font-size: 1.2em;
    border-radius: 15px;
    color: white;
    margin-bottom: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

/* Hover effect */
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: #FFFFFF;
    color: white;
    box-shadow: 5px 5px 5px #046A38;
}

/* Selected radio option */
section[data-testid="stSidebar"] div[role="radiogroup"] input:checked + div {
    background-color: #FF671F !important;
    color: white !important;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

import feedparser
import urllib.parse

def fetch_mining_news(mine_type):

    if mine_type == "Open Pit Mines":
        query = "India open pit mine accident OR landslide OR rockfall"
    else:
        query = "India underground mine collapse OR tunnel accident OR mine disaster"

    encoded_query = urllib.parse.quote(query)

    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)

    news_list = []

    for entry in feed.entries[:5]:
        news_list.append({
            "title": entry.title,
            "link": entry.link
        })

    return news_list

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas.errors import EmptyDataError

def process_uploaded_file(file):

    try:
        df = pd.read_csv(file)
    except EmptyDataError:
        raise ValueError("Uploaded file is empty.")
    except Exception as e:
        raise ValueError(f"Unable to read CSV file: {e}")

    if len(df) == 0:
        raise ValueError("Uploaded file contains no data rows.")

    stats = {
        'rows_read': len(df),
        'rows_rejected': 0,
        'columns_missing': [],
        'synthetic': False,
    }

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace(r'[^\w\s]', '', regex=True)
    )

    rename_map = {
        'factor_of_safety_fs': 'fs',
        'reinforcement_numeric': 'reinforcement',
    }

    for orig_col in rename_map:
        if orig_col in df.columns:
            df.rename(columns={orig_col: rename_map[orig_col]}, inplace=True)

    required_columns = {'fs', 'reinforcement'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        stats['columns_missing'] = list(missing)
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    rows_before = len(df)

    # Validate numeric columns: coerce to numeric, track rows that become NaN
    for col in ['fs', 'reinforcement']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['fs', 'reinforcement'])

    rows_after = len(df)
    stats['rows_rejected'] = rows_before - rows_after

    if len(df) == 0:
        raise ValueError("All rows were rejected due to missing or invalid numeric values.")

    if 'timestamp' not in df.columns:
        df['timestamp'] = pd.date_range(datetime.now(), periods=len(df), freq='min')

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    df['rockfall_risk'] = ((df['fs'] < 1.4) | (df['reinforcement'] < 0.4)).astype(int)

    return df, stats

def generate_mock_data(n=100):
    np.random.seed(42)
    data = pd.DataFrame({
        'unit_weight_knm3': np.random.uniform(15, 25, n),
        'cohesion_kpa': np.random.uniform(10, 40, n),
        'internal_friction_angle': np.random.uniform(20, 45, n),
        'slope_angle': np.random.uniform(25, 60, n),
        'slope_height_m': np.random.uniform(5, 30, n),
        'pore_water_pressure_ratio': np.random.uniform(0, 1, n),
        'reinforcement_type': np.random.choice(
            ['Drainage', 'Geosynthetics', 'Retaining Wall', 'Soil Nailing'], n),
        'reinforcement': np.random.uniform(0, 5, n),
        'fs': np.random.uniform(1, 3, n),
        'timestamp': pd.date_range(
            datetime.now() - timedelta(minutes=n),
            periods=n,
            freq='min'),
    })

    data['rockfall_risk'] = ((data['fs'] < 1.4) | (data['reinforcement'] < 0.4)).astype(int)

    return data

def process_underground_file(file):

    try:
        df = pd.read_csv(file)
    except EmptyDataError:
        raise ValueError("Uploaded file is empty.")
    except Exception as e:
        raise ValueError(f"Unable to read CSV file: {e}")

    if len(df) == 0:
        raise ValueError("Uploaded file contains no data rows.")

    stats = {
        'rows_read': len(df),
        'rows_rejected': 0,
        'columns_missing': [],
        'synthetic': False,
    }

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace(r'[^\w\s]', '', regex=True)
    )

    required_columns = {
        'seismic', 'seismoacoustic', 'shift',
        'genergy', 'gpuls', 'gdenergy', 'gdpuls',
        'hazard', 'nbumps', 'nbumps2', 'nbumps3',
        'nbumps4', 'nbumps5', 'nbumps6',
        'nbumps7', 'nbumps89',
        'energy', 'maxenergy'
    }

    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        stats['columns_missing'] = list(missing)
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    rows_before = len(df)

    # Validate numeric columns: coerce to numeric, track rows that become NaN
    numeric_cols = [
        'genergy', 'gpuls', 'gdenergy', 'gdpuls',
        'nbumps', 'nbumps2', 'nbumps3', 'nbumps4',
        'nbumps5', 'nbumps6', 'nbumps7', 'nbumps89',
        'energy', 'maxenergy'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna()

    rows_after = len(df)
    stats['rows_rejected'] = rows_before - rows_after

    if len(df) == 0:
        raise ValueError("All rows were rejected due to missing or invalid numeric values.")

    if 'timestamp' not in df.columns:
        df['timestamp'] = pd.date_range(datetime.now(), periods=len(df), freq='min')

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    return df, stats

def generate_underground_mock_data(n=100):

    np.random.seed(42)

    data = pd.DataFrame({
        'seismic': np.random.choice(['a', 'b', 'c'], n),
        'seismoacoustic': np.random.choice(['a', 'b', 'c'], n),
        'shift': np.random.choice(['N', 'W'], n),
        'genergy': np.random.uniform(1000, 30000, n),
        'gpuls': np.random.uniform(10, 200, n),
        'gdenergy': np.random.uniform(-100, 100, n),
        'gdpuls': np.random.uniform(-100, 100, n),
        'hazard': np.random.choice(['a', 'b', 'c'], n),
        'nbumps': np.random.randint(0, 5, n),
        'nbumps2': np.random.randint(0, 5, n),
        'nbumps3': np.random.randint(0, 5, n),
        'nbumps4': np.random.randint(0, 5, n),
        'nbumps5': np.random.randint(0, 5, n),
        'nbumps6': np.random.randint(0, 5, n),
        'nbumps7': np.random.randint(0, 5, n),
        'nbumps89': np.random.randint(0, 5, n),
        'energy': np.random.uniform(0, 10000, n),
        'maxenergy': np.random.uniform(0, 10000, n),
        'timestamp': pd.date_range(
            datetime.now() - timedelta(minutes=n),
            periods=n,
            freq='min'),
    })

    return data

# ---------------------------------------------------------------------------
# Upload directory helpers (Phase 2: keep uploaded data separate from bundled datasets)
# ---------------------------------------------------------------------------
USER_DATA_DIR = "user_data"
OPEN_PIT_UPLOAD_DIR = os.path.join(USER_DATA_DIR, "open_pit_uploads")
UNDERGROUND_UPLOAD_DIR = os.path.join(USER_DATA_DIR, "underground_uploads")

def get_upload_dir(mine_type):
    """Return the upload directory for the selected mine type."""
    if mine_type == "Open Pit Mines":
        return OPEN_PIT_UPLOAD_DIR
    return UNDERGROUND_UPLOAD_DIR

def sanitize_filename(filename):
    """Strip path traversal and unsafe characters from an uploaded filename."""
    basename = os.path.basename(filename or "upload.csv")
    safe = re.sub(r'[^a-zA-Z0-9._-]', '_', basename)
    if not safe or safe in ('.', '..'):
        safe = "upload.csv"
    return safe

def get_unique_filename(upload_dir, original_name):
    """Create a unique, timestamp-prefixed filename inside upload_dir."""
    safe_name = sanitize_filename(original_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(safe_name)
    if not ext:
        ext = ".csv"
    return f"{timestamp}_{name}{ext}"

def save_uploaded_bytes(file_bytes, upload_dir, filename):
    """Save raw uploaded bytes to disk and return the saved file path."""
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, "wb") as f:
        f.write(file_bytes)
    return file_path

# ---------------------------------------------------------------------------
# Help desk attachment security helpers (Phase 4A)
# ---------------------------------------------------------------------------
HELPDESK_ATTACHMENT_DIR = "helpdesk_attachments"
MAX_ATTACHMENT_SIZE_MB = 10
MAX_ATTACHMENT_SIZE_BYTES = MAX_ATTACHMENT_SIZE_MB * 1024 * 1024
ALLOWED_ATTACHMENT_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.csv', '.pdf'}

def secure_attachment_filename(original_filename):
    """Strip path components and validate extension from an uploaded filename.

    Returns (safe_basename, error_message). On success, error_message is None.
    On failure, safe_basename is None and error_message describes the problem.
    """
    if not original_filename or not str(original_filename).strip():
        return None, "No filename provided."

    raw = str(original_filename).strip()

    # Reject path traversal and separator patterns in the raw filename
    # BEFORE basename strips them, so we can report the correct error.
    if '..' in raw or '/' in raw or '\\' in raw:
        return None, "Filename contains invalid path characters."

    basename = os.path.basename(raw)

    # Reject empty basename after stripping
    if not basename or basename in ('.', '..'):
        return None, "Invalid filename."

    # Validate file extension against allowed types
    _, ext = os.path.splitext(basename)
    ext = ext.lower()
    if ext not in ALLOWED_ATTACHMENT_EXTENSIONS:
        return None, f"File type '{ext}' is not allowed. Allowed: {', '.join(sorted(ALLOWED_ATTACHMENT_EXTENSIONS))}."

    return basename, None

def save_helpdesk_attachment(file_bytes, original_filename):
    """Save an uploaded help desk attachment securely.

    The file is written under HELPDESK_ATTACHMENT_DIR using a UUID-based
    server-side filename (with the original extension preserved). The original
    filename is returned separately for display purposes.

    Returns (server_path, original_display_name, error_message).
    On success, error_message is None. On failure, the first two values are None.
    """
    if not file_bytes:
        return None, None, "Empty file uploaded."

    if len(file_bytes) > MAX_ATTACHMENT_SIZE_BYTES:
        return None, None, f"File exceeds {MAX_ATTACHMENT_SIZE_MB} MB size limit."

    basename, err = secure_attachment_filename(original_filename)
    if err:
        return None, None, err

    # Generate UUID-based server-side filename preserving the original extension
    _, ext = os.path.splitext(basename)
    server_filename = f"{uuid.uuid4().hex}{ext}"

    # Resolve the target directory and verify confinement before writing
    os.makedirs(HELPDESK_ATTACHMENT_DIR, exist_ok=True)
    target_dir = os.path.abspath(HELPDESK_ATTACHMENT_DIR)
    target_path = os.path.abspath(os.path.join(target_dir, server_filename))

    if not (target_path == target_dir or target_path.startswith(target_dir + os.sep)):
        return None, None, "Unsafe file path detected."

    # Avoid overwriting on collision (extremely unlikely with UUID, but defensive)
    if os.path.exists(target_path):
        return None, None, "Attachment name collision. Please try again."

    try:
        with open(target_path, "wb") as f:
            f.write(file_bytes)
    except OSError:
        return None, None, "Failed to save attachment."

    return target_path, basename, None

st.sidebar.title("MineSafe Navigation")

mine_type = st.sidebar.radio(
    "Select Mine Type:",
    ["Open Pit Mines", "Underground Pit Mines"]
)

uploaded_file = st.sidebar.file_uploader(
    f"Upload {mine_type} CSV",
    type="csv"
)

if uploaded_file:
    try:
        # Save raw uploaded bytes to user_data directory (Phase 2: never overwrite bundled datasets)
        file_bytes = uploaded_file.getvalue()
        upload_dir = get_upload_dir(mine_type)
        saved_name = get_unique_filename(upload_dir, uploaded_file.name)
        saved_path = save_uploaded_bytes(file_bytes, upload_dir, saved_name)

        # Process from in-memory bytes so the file pointer starts at the beginning
        file_obj = BytesIO(file_bytes)

        if mine_type == "Open Pit Mines":
            data, stats = process_uploaded_file(file_obj)
        else:
            data, stats = process_underground_file(file_obj)

        # Show upload stats
        st.sidebar.success(f"File uploaded and processed! Saved to: {saved_path}")
        if stats['rows_rejected'] > 0:
            st.sidebar.info(f"{stats['rows_rejected']} row(s) rejected due to missing/invalid values ({stats['rows_read'] - stats['rows_rejected']} kept).")

    except Exception as e:
        st.sidebar.error(f"Error processing file: {e}")

        if mine_type == "Open Pit Mines":
            data = generate_mock_data()
        else:
            data = generate_underground_mock_data()

        st.sidebar.warning("Using synthetic/demo data instead of the invalid upload.")

else:
    try:
        if mine_type == "Open Pit Mines":
            data = pd.read_csv("slope_stability_dataset.csv")
        else:
            data = pd.read_csv("underground_dataset.csv")

        if 'timestamp' not in data.columns:
            data['timestamp'] = pd.date_range(datetime.now(), periods=len(data), freq='min')
        else:
            data['timestamp'] = pd.to_datetime(data['timestamp'])

        st.sidebar.info("Loaded existing processed data.")

    except (FileNotFoundError, EmptyDataError, ValueError):

        if mine_type == "Open Pit Mines":
            data = generate_mock_data()
        else:
            data = generate_underground_mock_data()

        st.sidebar.warning("No valid uploaded data found. Using synthetic/demo data.")

import streamlit as st

st.markdown(
    """
    <style>
        /* This targets the main content area in Streamlit */
        .main .block-container {
            padding-top: 2em;
        }

        /* The sticky container for the title */
        .sticky-title {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height:15%;
            padding: 30px 30px;
            z-index: 999;
            text-align: center;
            margin: 0;
            font-size: 30px; /* Slightly reduced as requested */
            color: #06038D;
            font-weight: bold;
            text-align: center;
            position: fixed;
            background-color: #f0f2f6;
        }
        
        /* Adjusting the rest of the content so it doesn't get hidden under the title */
        .content-spacer {
            margin-top: 0px;
        }
    </style>

    <div class="sticky-title">
        <h1 style="margin:0;">
            AI-Based Rockfall Prediction & Alert System
        </h1>
    </div>

    
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
section[data-testid="stSidebar"] label[data-baseweb="radio"] {
    background-color: #f0f8ff; color: #003366;
    padding: 10px 16px; border-radius: 8px;
    border: 1px solid #cce0ff; margin-bottom: 6px;
    font-size: 18px; font-weight: 600;
}
section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
    background-color: #cce6ff; border-color: #3399ff;
}
section[data-testid="stSidebar"] label[data-baseweb="radio"][aria-checked="true"] {
    background-color: #007bff; color: white !important; border-color: #0056b3;
}
</style>
""", unsafe_allow_html=True)

section = st.sidebar.radio("Navigate to:", [
    "Dashboard", "Prediction", "Alerts", "Upload Data", "Results", "AI Assistant" , "Help Desk"
])

def metric_card(title, value, status):
    colors = {
        "success": "#28a745",
        "error": "#dc3545",
        "warning": "#ffc107"
    }

    color = colors.get(status, "black")

    st.markdown(f"""
     <div style="
         border-radius:10px;
         padding:15px;
         background-color:#d3d3d3;
         text-align:center;
         box-shadow:2px 2px 5px rgba(0,0,0,0.1);
     ">
         <h5>{title}</h5>
         <p style="font-size:24px; font-weight:bold; color:{color}; margin:0;">
             {value}
         </p>
     </div>
     """, unsafe_allow_html=True)

if section == "Dashboard":

    st.markdown(f"### {mine_type} Monitoring Dashboard")

    if mine_type == "Open Pit Mines":
        latest = data.iloc[-1]
        current_risk = "HIGH RISK" if latest['rockfall_risk'] == 1 else "Safe"
        active_alerts = int(data['rockfall_risk'].sum())

    else:

        if 'energy' in data.columns and 'maxenergy' in data.columns:
            data['rockfall_risk'] = (
                (data['energy'] > data['energy'].quantile(0.75)) |
                (data['maxenergy'] > data['maxenergy'].quantile(0.75))
            ).astype(int)
        else:
            data['rockfall_risk'] = 0

        latest = data.iloc[-1]
        current_risk = "HIGH RISK" if latest['rockfall_risk'] == 1 else "Safe"
        active_alerts = int(data['rockfall_risk'].sum())

    system_status = "Operational" if active_alerts < 5 else "High Alerts"
    status_color = "success" if active_alerts < 5 else "warning"

    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

    with col1:
        metric_card(
            "Current Risk",
            current_risk,
            "error" if current_risk == "HIGH RISK" else "success"
        )

    with col2:
        metric_card(
            "Active Alerts",
            active_alerts,
            "error" if active_alerts > 0 else "success"
        )

    with col3:
        metric_card(
            "System Status",
            system_status,
            status_color
        )

    with col4:
        st.info("Recent Activity")
        st.dataframe(
            data.tail(5).set_index('timestamp'),
            use_container_width=True
        )

    st.divider()

    if mine_type == "Open Pit Mines":

        st.subheader("Open Pit Stability Trends")

        col5, col6 = st.columns(2)

        with col5:
            st.line_chart(
                data.set_index('timestamp')['fs'],
                use_container_width=True
            )

        with col6:
            st.line_chart(
                data.set_index('timestamp')['reinforcement'],
                use_container_width=True
            )

        avg_fs = round(data['fs'].mean(), 2)
        min_fs = round(data['fs'].min(), 2)

        st.metric("Average Factor of Safety", avg_fs)
        st.metric("Minimum Factor of Safety", min_fs)

    else:

        st.subheader("Underground Seismic & Stress Monitoring")

        col7, col8 = st.columns(2)

        with col7:
            if 'energy' in data.columns:
                st.line_chart(
                    data.set_index('timestamp')['energy'],
                    use_container_width=True
                )

        with col8:
            if 'maxenergy' in data.columns:
                st.line_chart(
                    data.set_index('timestamp')['maxenergy'],
                    use_container_width=True
                )

        col9, col10 = st.columns(2)

        with col9:
            if 'genergy' in data.columns:
                st.line_chart(
                    data.set_index('timestamp')['genergy'],
                    use_container_width=True
                )

        with col10:
            if 'gpuls' in data.columns:
                st.line_chart(
                    data.set_index('timestamp')['gpuls'],
                    use_container_width=True
                )

        if 'energy' in data.columns:
            st.metric(
                "Average Energy Level",
                round(data['energy'].mean(), 2)
            )

        if 'maxenergy' in data.columns:
            st.metric(
                "Maximum Recorded Energy",
                round(data['maxenergy'].max(), 2)
            )

    st.divider()

    st.subheader("Site Monitoring Image")

    if mine_type == "Open Pit Mines":
        st.image(
            "mine.png",
            caption="Open Pit Mining Area",
            use_container_width=True
        )
    else:
        st.image(
            "underground_mine.png",
            caption="Underground Tunnel Monitoring",
            use_container_width=True
        )

elif section == "Prediction":

    st.markdown("### Rockfall Prediction")

    import os
    import joblib
    import plotly.express as px

    latest = data.iloc[-1]
    prediction = 0
    model_used = False

    if mine_type == "Open Pit Mines":
        model_path = "rockfall_model_fs_reinforcement.pkl"
    else:
        model_path = "underground_rockfall_model.pkl"

    if os.path.exists(model_path):

        try:
            model = joblib.load(model_path)

            if mine_type == "Open Pit Mines":

                input_df = pd.DataFrame({
                    "fs": [latest["fs"]],
                    "reinforcement": [latest["reinforcement"]]
                })

                prediction = model.predict(input_df)[0]
                model_used = True

            else:

                # Build a single-row DataFrame from the latest record.
                input_df = latest.to_frame().T.copy()

                try:
                    prediction = int(underground_predict(input_df)[0])
                    model_used = True
                except ValueError as ve:
                    # Preprocessing errors (missing features, unseen categories,
                    # missing artifacts) are surfaced clearly to the user.
                    st.error(f"Underground prediction error: {ve}")
                    prediction = 0
                    model_used = False
                except Exception as e:
                    # Any other unexpected error during preprocessing/prediction.
                    st.error(f"Underground prediction error: {e}")
                    prediction = 0
                    model_used = False

        except Exception as e:
            st.error(f"Model error: {e}")
            prediction = 0
            model_used = False

    else:

        st.warning("Model file not found. Using rule-based fallback.")

        if mine_type == "Open Pit Mines":

            prediction = 1 if (
                latest['fs'] < 1.4 or
                latest['reinforcement'] < 0.4
            ) else 0

        else:

            if 'energy' in data.columns and 'maxenergy' in data.columns:

                prediction = 1 if (
                    latest['energy'] > data['energy'].quantile(0.75) or
                    latest['maxenergy'] > data['maxenergy'].quantile(0.75)
                ) else 0
            else:
                prediction = 0

        model_used = False

    prediction_label = "HIGH RISK" if prediction == 1 else "Safe"
    prediction_color = "#dc3545" if prediction == 1 else "#28a745"

    st.markdown(f"""
    <div style="padding:20px; border-radius:10px; background-color:#f9f9f9;
                border-left:10px solid {prediction_color};">
        <h2 style="color:{prediction_color}; margin-bottom:5px;">
        Prediction Status: {prediction_label}</h2>
        <p style="color:#666;">
        Based on latest monitoring parameters ({mine_type})
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    if mine_type == "Open Pit Mines":

        with col1:
            st.metric("Factor of Safety", f"{latest['fs']:.2f}")

        with col2:
            st.metric("Reinforcement", f"{latest['reinforcement']:.2f}")

    else:

        with col1:
            st.metric(
                "Total Seismic Energy (J)",
                f"{latest.get('energy', 0):,.2f} J"
            )

        with col2:
            st.metric(
                "Peak Seismic Event Energy (J)",
                f"{latest.get('maxenergy', 0):,.2f} J"
            )

    with col3:
        st.metric("Model Used", "Yes" if model_used else "No")

    with st.expander("View Detailed Input Data"):

        if mine_type == "Open Pit Mines":

            st.json({
                "Timestamp": str(latest['timestamp']),
                "Mine Type": mine_type,
                "Factor of Safety": round(latest['fs'], 3),
                "Reinforcement": round(latest['reinforcement'], 3),
            })

        else:

            st.json({
                "Timestamp": str(latest['timestamp']),
                "Mine Type": mine_type,
                "Energy": round(latest.get('energy', 0), 3),
                "Max Energy": round(latest.get('maxenergy', 0), 3),
                "General Energy": round(latest.get('genergy', 0), 3),
                "Pulse Count": round(latest.get('gpuls', 0), 3)
            })

    st.markdown("### Rockfall Risk Trend")

    if 'rockfall_risk' not in data.columns:
        data['rockfall_risk'] = 0

    risk_chart_data = data[['timestamp', 'rockfall_risk']].copy()
    risk_chart_data['Risk Label'] = risk_chart_data[
        'rockfall_risk'
    ].map({1: 'High Risk', 0: 'Safe'})

    fig = px.area(
        risk_chart_data,
        x='timestamp',
        y='rockfall_risk',
        color='Risk Label',
        title='Rockfall Risk Over Time',
        color_discrete_map={
            'High Risk': '#dc3545',
            'Safe': '#28a745'
        }
    )

    fig.update_layout(
        height=400,
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="#ffffff"
    )

    st.plotly_chart(fig, use_container_width=True)

elif section == "Alerts":
    st.markdown(f"### {mine_type} - Real-Time Alerts Dashboard")
    st.markdown('Monitor high-risk stability events with intelligent filtering and classification.')
    import pandas as pd
    import plotly.express as px

    alerts = data.copy()
    alerts['DateTime'] = pd.to_datetime(alerts['timestamp'])

    # Severity mapping from alert types
    severity_map = {
        'Critical': 'Critical',
        'FS Alert': 'High',
        'Moderate Alert': 'Moderate',
        'Info Alert': 'Info',
    }
    alerts['Severity'] = alerts['type'].map(severity_map).fillna('Info')
# Summary metrics row
    total_alerts = len(filtered_alerts)
    critical_count = len(filtered_alerts[filtered_alerts['Severity'] == 'Critical'])
    high_count = len(filtered_alerts[filtered_alerts['Severity'] == 'High'])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total Alerts', total_alerts)
    with col2:
        st.metric('Critical', critical_count)
    with col3:
        st.metric('High Severity', high_count)

    # Plotly pie chart for severity distribution
    severity_counts = filtered_alerts['Severity'].value_counts()
    if len(severity_counts) > 0:
        fig = px.pie(
            values=severity_counts.values,
            names=severity_counts.index,
            title='Severity Distribution',
        )
        st.plotly_chart(fig, use_container_width=True)

    # Top Critical Alerts section
    st.markdown('### Top Critical Alerts')
    critical_alerts = filtered_alerts[filtered_alerts['Severity'] == 'Critical'].head(5)
    if len(critical_alerts) > 0:
        for _, alert in critical_alerts.iterrows():
            st.markdown(f"- **{alert.get('location', 'Unknown')}** - {alert.get('timestamp', 'N/A')} - {alert.get('type', 'Unknown Type')} - Critical")
    else:
        st.info('No critical alerts at this time.')

    # Alert log with severity color coding
    st.markdown('### Alert Log')
    for _, alert in filtered_alerts.iterrows():
        severity = alert['Severity']
        if severity == 'Critical':
            border_color = 'red'
            bg_color = 'rgba(255, 0, 0, 0.1)'
        elif severity == 'High':
            border_color = 'orange'
            bg_color = 'rgba(255, 165, 0, 0.1)'
        elif severity == 'Moderate':
            border_color = 'orange'
            bg_color = 'rgba(255, 165, 0, 0.05)'
        else:
            border_color = 'blue'
            bg_color = 'rgba(0, 0, 255, 0.05)'

        st.markdown(
            f"""
            <div style='padding: 8px 12px; background-color: {bg_color}; border-left: 4px solid {border_color}; margin: 4px 0; border-radius: 4px; font-size: 0.9em;'>
                <strong>{alert.get('location', 'Unknown Location')}</strong> - {pd.to_datetime(alert['timestamp']).strftime('%m/%d %H:%M')} - {alert.get('type', 'Unknown Type')} - {severity}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Notification form wrapped in st.form
    st.markdown('### Send Notification')
    with st.form(key='notification_form'):
        recipient = st.text_input(
            'Recipient Email(s)',
            help='Enter email addresses separated by commas. Configure SMTP in Streamlit secrets or environment variables.',
        )
        subject = st.text_input('Subject')
        message = st.text_area('Message')
        form_submit = st.form_submit_button('Send')

        if form_submit and recipient:
            from notifications import send_email
            send_email(recipient, subject, message)
            st.success('Notification sent!')

    # Filters row: severity, type, notification
    c1, c2, c3 = st.columns(3)
    with c1:
        severity_filter = st.selectbox(
            'Severity Filter',
            ['All', 'Critical', 'High', 'Moderate', 'Info'],
            index=0,
        )

    with c2:
        type_filter = st.multiselect(
            'Type Filter',
            ['All'] + list(alerts['type'].unique()) if len(alerts) > 0 else ['All'],
            default=['Critical'] if len(alerts) > 0 else [],
        )

    with c3:
        notification_method = st.selectbox(
            'Notification Method',
            ['Email', 'SMS', 'App Notification', 'None'],
        )

    # Apply filters
    filtered_alerts = alerts.copy()
    if severity_filter != 'All':
        filtered_alerts = filtered_alerts[filtered_alerts['Severity'] == severity_filter]
    if 'All' not in type_filter:
        filtered_alerts = filtered_alerts[filtered_alerts['type'].isin(type_filter)]

    st.markdown(f"### {mine_type} - Real-Time Alerts Dashboard")
    st.markdown("Monitor high-risk stability events with intelligent filtering and classification.")

    import pandas as pd

    alerts = data.copy()
    alerts['DateTime'] = pd.to_datetime(alerts['timestamp'])

    total_records = len(data)
    analysis_date = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    available_cols = set(alerts.columns)

    is_open_pit_data = {'fs', 'reinforcement'}.issubset(available_cols)
    is_underground_data = {'energy', 'maxenergy'}.issubset(available_cols)

    col1, col2, col3 = st.columns(3)

    with col1:

        notification_method = st.selectbox(
            "Notification Method",
            ["Email", "SMS", "App Notification", "None"]
        )

        recipient_emails = st.text_input(
            "Recipient Email(s) (comma-separated)",
            placeholder="e.g. safety@mine.com, engineer@mine.com",
            help="Enter one or more email addresses separated by commas. Configure SMTP in Streamlit secrets or environment variables.",
        )


if mine_type == "Underground Pit Mines":

        target_col = 'class' if 'class' in data.columns else 'hazard'

        total_alerts = int(data[target_col].sum())
        risk_percent = (data[target_col].mean()) * 100

        avg_energy = data['energy'].mean() if 'energy' in data.columns else 0
        max_energy = data['maxenergy'].max() if 'maxenergy' in data.columns else 0
        total_bumps = data[['nbumps2', 'nbumps3', 'nbumps4', 'nbumps5']].sum().sum()

        if risk_percent > 30 or total_bumps > 10:
            overall_risk = "High"
            risk_color = "error"
        elif risk_percent > 10:
            overall_risk = "Moderate"
            risk_color = "warning"
        else:
            overall_risk = "Low"
            risk_color = "success"

        col1, col2, col3 = st.columns(3)
        with col1:
            metric_card("Total Shifts Analyzed", f"{total_records}", "success")
        with col2:
            metric_card("Seismic Hazards", f"{total_alerts}", "error" if total_alerts > 0 else "success")
        with col3:
            metric_card("Avg Energy (J)", f"{avg_energy:.1f}", "warning" if avg_energy > 5000 else "success")

        col4, col5, col6 = st.columns(3)
        with col4:
            metric_card("Max Energy Recorded", f"{max_energy:.0f}", "error" if max_energy > 50000 else "warning")
        with col5:
            metric_card("Seismic Risk Level", overall_risk, risk_color)
        with col6:
            metric_card("Last Analyzed", analysis_date, "success")

        st.markdown("### Seismic Activity Breakdown")
        col7, col8 = st.columns(2)
        with col7:

            if 'genergy' in data.columns and 'gpuls' in data.columns:
                hazard_idx = (data['genergy'] / data['gpuls'].replace(0, 1)).mean()
                metric_card("Energy/Pulse Index", f"{hazard_idx:.2f}", "warning" if hazard_idx > 100 else "success")
        with col8:
            metric_card("Total Multi-magnitude Bumps", f"{int(total_bumps)}", "error" if total_bumps > 5 else "success")

else:
        total_alerts = int(data['rockfall_risk'].sum())
        avg_fs = data['fs'].mean()
        avg_reinf = data['reinforcement'].mean()
        risk_percent = (data['rockfall_risk'].mean()) * 100

        if risk_percent > 50:
            overall_risk = "High"
            risk_color = "error"
        elif risk_percent > 20:
            overall_risk = "Moderate"
            risk_color = "warning"
        else:
            overall_risk = "Low"
            risk_color = "success"

        col1, col2, col3 = st.columns(3)
        with col1:
            metric_card("Total Records", f"{total_records}", "success")
        with col2:
            metric_card("Total Alerts", f"{total_alerts}", "error" if total_alerts > 0 else "success")
        with col3:
            metric_card("Average FS", f"{avg_fs:.3f}", "success" if avg_fs > 1.4 else "warning")

        col4, col5, col6 = st.columns(3)
        with col4:
            metric_card("Avg Reinforcement", f"{avg_reinf:.3f}", "success" if avg_reinf > 0.4 else "warning")
        with col5:
            metric_card("Overall Risk Level", overall_risk, risk_color)
        with col6:
            metric_card("Last Analyzed", analysis_date, "success")

st.markdown("### Risk Proportion")
st.progress(min(int(risk_percent), 100), text=f"{risk_percent:.2f}% of data indicates high risk")
st.markdown("### Distribution Breakdown")

label_map = {0: "Safe", 1: "Seismic Hazard"} if mine_type == "Underground Pit Mines" else {0: "Stable",
                                                                                            1: "Rockfall Risk"}
target_series = data['class'] if mine_type == "Underground Pit Mines" else data['rockfall_risk']

fig, ax = plt.subplots()
ax.pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%', startangle=90, colors=['#2ecc71', '#e74c3c'])
ax.axis("equal")
st.pyplot(fig)

st.subheader("Real-Time Indian Mining News")

target_series = data['class'] if mine_type == "Underground Pit Mines" else data['rockfall_risk']

risk_counts = target_series.value_counts().rename(label_map)

fig, ax = plt.subplots()


    if news_items:
        for item in news_items:
            title_lower = item["title"].lower()
            if any(word in title_lower for word in risk_keywords):
                st.error(f"{item['title']}")
                news_risk_score += 1
            else:
                st.info(f"{item['title']}")
            st.markdown(f"[Read more]({item['link']})")
    else:
        st.info("No recent mining news found.")

    adjusted_risk_percent = min(risk_percent + (news_risk_score * 3), 100)
    st.markdown("### Final Adjusted Risk Index (Local + National Context)")
    st.progress(int(adjusted_risk_percent), text=f"{adjusted_risk_percent:.2f}% adjusted risk")

elif section == "AI Assistant":

    import pandas as pd

    st.markdown(f"### {mine_type} - Prediction Results Summary")

    st.markdown(
        "Ask about rockfall risk, slope stability, underground stress, RMR, or safety recommendations."
    )

    prompt = st.text_area(
        "Ask your question:",
        placeholder="Example: What is the current risk level?"
    )

    if st.button("Get Response"):

        if not prompt.strip():
            st.warning("Please enter a question.")
            st.stop()

        question = prompt.lower()
        risk_percent = 100 * data['rockfall_risk'].mean()
        avg_fs = data['fs'].mean()
        avg_reinf = data['reinforcement'].mean()

        latest = data.iloc[-1]
        if mine_type == "Underground Pit Mines":
            try:
                data['stress_mpa'] = (
                    data['slope_height_m'] *
                    data['unit_weight_knm']
                ) / 1000

                data['rmr'] = (
                    data['cohesion_kpa'] / 2.5
                ) + (
                    data['internal_friction_angle_'] * 1.2
                )

                data['rmr'] = data['rmr'].clip(20, 90)

                avg_stress = data['stress_mpa'].mean()
                avg_rmr = data['rmr'].mean()

            except:
                avg_stress = None
                avg_rmr = None

        if "risk" in question:
            st.write(
                f"Approximately **{risk_percent:.1f}%** of monitored slopes show high rockfall risk."
            )
        elif "factor of safety" in question or "fs" in question:
            st.write(
                f"The average Factor of Safety is **{avg_fs:.2f}**."
            )

            if avg_fs < 1.4:
                st.warning("The FS is below recommended safe design levels.")
        elif "reinforcement" in question:
            st.write(
                f"The average reinforcement value is **{avg_reinf:.2f}**."
            )
        elif mine_type == "Underground Pit Mines" and "stress" in question:
            if avg_stress is not None:
                st.write(
                    f"The average underground induced stress is **{avg_stress:.2f} MPa**."
                )
            else:
                st.warning("Stress data not available.")

        elif mine_type == "Underground Pit Mines" and "rmr" in question:
            if avg_rmr is not None:
                st.write(
                    f"The average Rock Mass Rating (RMR) is **{avg_rmr:.2f}**."
                )

                if avg_rmr < 40:
                    st.error("Rock mass quality is poor. Additional support recommended.")
            else:
                st.warning("RMR data not available.")
        elif "reduce" in question and "rockfall" in question:
            if mine_type == "Open Pit Mines":
                st.markdown("""
                **To reduce rockfall risk in Open Pit Mines:**
                - Install rock bolts and mesh.
                - Improve slope geometry.
                - Control blasting vibrations.
                - Ensure proper drainage.
                - Use real-time slope monitoring systems.
                """)
            else:
                st.markdown("""
                **To reduce rockfall risk in Underground Mines:**
                - Increase rock bolting density.
                - Apply shotcrete lining.
                - Monitor stress concentrations.
                - Improve tunnel reinforcement systems.
                - Conduct regular geotechnical inspections.
                """)
        elif "safe" in question and ("worker" in question or "workers" in question):
            st.markdown("""
            **Worker Safety Recommendations:**
            - Restrict access to unstable zones.
            - Install protective barriers.
            - Use helmets and PPE.
            - Implement alarm systems.
            - Conduct emergency drills regularly.
            """)

        elif "current" in question or "latest" in question:
            st.markdown(f"""
            **Latest Monitoring Snapshot:**
            - FS: **{latest['fs']:.2f}**
            - Reinforcement: **{latest['reinforcement']:.2f}**
            - Risk Status: **{"HIGH RISK" if latest['rockfall_risk'] == 1 else "Safe"}**
            """)
        elif "help" in question:
            st.markdown("""
            You can ask about:
            - Current risk
            - Factor of Safety
            - Reinforcement
            - Stress (Underground)
            - RMR (Underground)
            - Safety recommendations
            - How to reduce rockfall
            """)
        elif "news" in question:
            news_items = fetch_mining_news(mine_type)
            for item in news_items:
                st.write(f"- {item['title']}")
        else:
            st.info(
                "I can answer questions about risk, FS, reinforcement, underground stress, RMR, and safety measures."
            )

elif section == "Help Desk":
    import os
    import pandas as pd
    from datetime import datetime
    import uuid
    import streamlit as st

    st.markdown("### MineSafe Command & Support Center")

    st.markdown("""
    This help desk allows engineers, supervisors, and safety officers
    to report seismic hazards, underground collapses, system errors, or real
    mine incidents.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Project Manager
        **Name:** Er. Rajesh Verma
        **Designation:** Mine Safety & Operations Manager
        **Phone:** +91-98765-43210
        **Email:** manager@minesafety.com
        """)

        st.markdown("""
        ### Technical Support Lead
        **Name:** Eng. Priya Sharma
        **Designation:** AI Systems Engineer
        **Phone:** +91-91234-56789
        **Email:** support@minesafety.com
        """)

    with col2:
        st.markdown("""
        ### Emergency Control Room
        **24/7 Helpline:** +91-90000-11111
        **Emergency Email:** emergency@minesafety.com
        """)

        st.markdown("""
        ### Office Address
        Mine Safety Control Center
        Sector 12, Industrial Area
        Lucknow, Uttar Pradesh, India
        PIN: 226010
        """)

    st.divider()

    st.subheader("Working Hours")

    st.markdown("""
    **Monday – Friday:** 9:00 AM – 6:00 PM
    **Saturday:** 9:00 AM – 2:00 PM
    **Sunday:** Closed
    """)

    st.divider()

    st.subheader("Current System Context")

    if 'data' in globals() and data is not None:
        if mine_type == "Underground Pit Mines":

            target_col = 'class' if 'class' in data.columns else 'hazard'
            risk_percent = 100 * data[target_col].mean() if target_col in data.columns else 0

            avg_val = data['energy'].mean() if 'energy' in data.columns else 0
            total_alerts = int(data[target_col].sum()) if target_col in data.columns else 0

            label_avg = "Avg Energy (J)"
            label_risk = "Seismic Risk %"
        else:

            risk_percent = 100 * data['rockfall_risk'].mean() if 'rockfall_risk' in data.columns else 0
            avg_val = data['fs'].mean() if 'fs' in data.columns else 0
            total_alerts = int(data['rockfall_risk'].sum()) if 'rockfall_risk' in data.columns else 0

            label_avg = "Avg FS"
            label_risk = "Rockfall Risk %"

        col1, col2, col3 = st.columns(3)
        col1.metric(label_risk, f"{risk_percent:.2f}%")
        col2.metric(label_avg, f"{avg_val:.2f}")
        col3.metric("Active Alerts", total_alerts)
    else:
        st.info("No dataset loaded yet. Please upload seismic-bumps.csv or slope_stability_datasets.csv.")

    st.divider()

    st.subheader("Report Mining Incident / Issue")

    with st.form("helpdesk_form"):
        name = st.text_input("Officer / Engineer Name")
        designation = st.selectbox(
            "Designation",
            ["Site Engineer", "Geotechnical Engineer", "Seismologist", "Safety Officer",
             "Mine Manager", "Supervisor", "Other"]
        )

        contact = st.text_input("Contact Number / Email")

        incident_categories = [
            "Seismic Bump Event",
            "Underground Collapse",
            "Abnormal Energy Spike",
            "Gas Leakage / Ventilation",
            "Rockburst Occurrence",
            "Sensor Failure",
            "False Hazard Prediction",
            "System Bug",
            "Other"
        ] if mine_type == "Underground Pit Mines" else [
            "Rockfall Event", "Slope Instability", "Blasting Vibration Issue",
            "Sensor Failure", "False Prediction", "System Bug", "Other"
        ]

        incident_type = st.selectbox("Incident Category", incident_categories)

        hazard_level = st.selectbox(
            "Hazard Severity",
            ["Low", "Moderate", "High", "Critical"]
        )

        location = st.text_input("Mine Section / Level / Tunnel ID")
        description = st.text_area("Detailed Description (e.g., Magnitude of bump, depth, etc.)")

        uploaded_file = st.file_uploader(
            "Upload Evidence (Seismic Log/Image/Report)",
            type=["png", "jpg", "jpeg", "csv", "pdf"]
        )

        submitted = st.form_submit_button("Submit Incident Report", type="primary", use_container_width=True)

    if submitted:
        if not name or not contact or not description:
            st.error("Please fill all mandatory fields.")
        else:
            ticket_id = "MS-" + str(uuid.uuid4())[:8].upper()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            attachment_path = None
            attachment_display = None
            if uploaded_file is not None:
                file_bytes = uploaded_file.getbuffer()
                attachment_path, attachment_display, attach_err = save_helpdesk_attachment(
                    file_bytes, uploaded_file.name
                )
                if attach_err:
                    st.error(attach_err)
                    attachment_path = None
                    attachment_display = None

            ticket_data = {
                "Ticket ID": ticket_id,
                "Timestamp": timestamp,
                "Mine Type": mine_type,
                "Name": name,
                "Designation": designation,
                "Contact": contact,
                "Incident Type": incident_type,
                "Hazard Level": hazard_level,
                "Location": location,
                "Description": description,
                "Attachment": attachment_path,
                "Attachment_Display": attachment_display,
                "Status": "Open"
            }

            file_path = "minesafe_helpdesk_database.csv"

            if os.path.exists(file_path):
                existing = pd.read_csv(file_path)
                updated = pd.concat([existing, pd.DataFrame([ticket_data])], ignore_index=True)
            else:
                updated = pd.DataFrame([ticket_data])

            updated.to_csv(file_path, index=False)

            if hazard_level == "Critical":
                st.error(f"CRITICAL INCIDENT REPORTED! Ticket ID: {ticket_id}")
                st.warning("Immediate underground evacuation and safety team dispatch recommended.")
            elif hazard_level == "High":
                st.warning(f"High Priority Ticket Created: {ticket_id}")
            else:
                st.success(f"Ticket Submitted Successfully! ID: {ticket_id}")

    st.divider()
    st.subheader("Incident Tracking Dashboard")

    if os.path.exists("minesafe_helpdesk_database.csv"):
        tickets = pd.read_csv("minesafe_helpdesk_database.csv")

        filter_status = st.selectbox("Filter by Status", ["All", "Open", "In Review", "Resolved"])
        if filter_status != "All":
            tickets = tickets[tickets["Status"] == filter_status]

        st.dataframe(tickets, use_container_width=True)

        st.markdown("### Update Ticket Status")
        col_id, col_stat, col_btn = st.columns([2, 2, 1])

        ticket_to_update = col_id.text_input("Enter Ticket ID to Update")
        new_status = col_stat.selectbox("Change Status To", ["Open", "In Review", "Resolved"])

        if col_btn.button("Update Status"):
            df = pd.read_csv("minesafe_helpdesk_database.csv")
            if ticket_to_update in df["Ticket ID"].values:
                df.loc[df["Ticket ID"] == ticket_to_update, "Status"] = new_status
                df.to_csv("minesafe_helpdesk_database.csv", index=False)
                st.success("Ticket status updated.")
                st.rerun()
            else:
                st.error("Invalid Ticket ID.")
    else:
        st.info("No incidents reported yet.")

