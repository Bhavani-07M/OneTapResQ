import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import pandas as pd
from geopy.geocoders import Nominatim
from database import (
    save_mechanic_request,
    get_mechanic_requests,
    save_emergency_alert,
    get_emergency_alerts,
    save_fuel_request,
    get_fuel_requests,
    save_ev_request,
    get_ev_requests,
    create_user,
    login_user
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="OneTapResQ",
    page_icon="🚗",
    layout="wide"
)

# ---------------- SESSION STATE ---------------- #

if "emergency_triggered" not in st.session_state:
    st.session_state.emergency_triggered = False

if "show_mechanics" not in st.session_state:
    st.session_state.show_mechanics = False

if "john_accepted" not in st.session_state:
    st.session_state.john_accepted = False

if "priya_accepted" not in st.session_state:
    st.session_state.priya_accepted = False

if "arjun_accepted" not in st.session_state:
    st.session_state.arjun_accepted = False

if "global_latitude" not in st.session_state:
    st.session_state.global_latitude = None

if "global_longitude" not in st.session_state:
    st.session_state.global_longitude = None

if "current_place" not in st.session_state:
    st.session_state.current_place = "Location Not Detected"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    st.session_state.user_role = ""

if "username" not in st.session_state:
    st.session_state.username = ""


# ---------------- CUSTOM CSS ---------------- #

st.markdown(
    """
    <style>

    .main {

    background: linear-gradient(
        135deg,
        #030712,
        #111827,
        #1f2937
    );

    color: white;
   }
   .stApp {

    background: linear-gradient(
        135deg,
        #030712,
        #111827,
        #1f2937
    );
    }

    .welcome-box {

    background: linear-gradient(
        145deg,
        #111827,
        #1f2937
    );

    color: white;

    padding: 30px;

    border-radius: 20px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0px 6px 18px rgba(0,0,0,0.35);

    margin-bottom: 25px;
    }

    .feature-card {

    background: linear-gradient(
        145deg,
        #111827,
        #1f2937
    );

    color: white;

    padding: 25px;

    border-radius: 20px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0px 6px 18px rgba(0,0,0,0.35);

    text-align: center;

    margin-bottom: 20px;

    height: 260px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    transition: 0.3s ease-in-out;
   }

   .feature-card:hover {

    transform: translateY(-5px);

    box-shadow:
        0px 10px 25px rgba(0,0,0,0.45);
    }

    /* EMERGENCY BUTTON */

    .emergency-btn-container {

        position: fixed;

        bottom: 20px;

        left: 50%;

        transform: translateX(-50%);

        z-index: 9999;
    }

    div.stButton > button[kind="primary"] {

        background: linear-gradient(
            90deg,
            #ff0000,
            #ff3b3b
        ) !important;

        color: white !important;

        border-radius: 18px !important;

        height: 70px !important;

        width: 370px !important;

        font-size: 24px !important;

        font-weight: 900 !important;

        border: 3px solid white !important;

        box-shadow:
            0px 0px 20px rgba(255,0,0,0.9),
            0px 4px 15px rgba(0,0,0,0.35) !important;

        animation: emergencyPulse 1s infinite;
    }

    @keyframes emergencyPulse {

        0% {
            transform: scale(1);
        }

        50% {
            transform: scale(1.05);
        }

        100% {
            transform: scale(1);
        }
    }
    /* SIDEBAR */

    section[data-testid="stSidebar"] {

      background: linear-gradient(
         145deg,
         #111827,
         #1f2937
      );
   
     border-right: 1px solid rgba(255,255,255,0.08);
     }

     section[data-testid="stSidebar"] * {

     color: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# =========================================================
# LOGIN / SIGNUP SYSTEM
# =========================================================

if not st.session_state.logged_in:

    st.title("🔐 OneTapResQ Authentication")

    auth_option = st.selectbox(
        "Choose Option",
        [
            "Login",
            "Signup"
        ]
    )

    # =====================================================
    # SIGNUP
    # =====================================================

    if auth_option == "Signup":

        st.subheader("📝 Create Account")

        new_username = st.text_input(
            "👤 Username"
        )

        new_password = st.text_input(
            "🔑 Password",
            type="password"
        )

        phone = st.text_input(
            "📞 Phone Number"
        )

        role = st.selectbox(
            "Select Role",
            [
                "user",
                "admin"
            ]
        )

        if st.button("✅ Create Account"):

            # =============================================
            # PHONE VALIDATION
            # =============================================

            if not phone:

                st.error(
                    "⚠ Phone Number is required"
                )

            elif len(phone) != 10 or not phone.isdigit():

                st.error(
                    "⚠ Enter valid 10-digit phone number"
                )

            else:

                user_created = create_user(
                    new_username,
                    new_password,
                    phone,
                    role
                )

                if user_created:

                    st.success(
                        "Account Created Successfully🥳"
                        ", now switch to login and signin"
                    )

                else:

                    st.error(
                        "⚠ Username already exists"
                    )

    # =====================================================
    # LOGIN
    # =====================================================

    else:

        st.subheader("🔑 Login")

        username = st.text_input(
            "👤 Username"
        )

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        if st.button("🚀 Login"):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.username = user[1]

                st.session_state.user_role = user[4]

                st.success(
                    f"Welcome {user[1]}"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

    st.stop()
# =========================================================
# SHARED LIVE LOCATION
# =========================================================

st.markdown(
    "##### 📍 Tap here to detect live location  and proceed with our services"
)
live_location = streamlit_geolocation()

if live_location is not None:

    latitude = live_location.get("latitude")

    longitude = live_location.get("longitude")

    if latitude and longitude:

        st.session_state.global_latitude = latitude

        st.session_state.global_longitude = longitude

        geolocator = Nominatim(
            user_agent="onetapresq"
        )

        location_name = geolocator.reverse(
            f"{latitude}, {longitude}"
        )

        if location_name:

            st.session_state.current_place = (
                location_name.address
            )

        else:

            st.session_state.current_place = (
                "Location Not Found"
            )    


# =========================================================
# EMERGENCY SAFEGUARD
# =========================================================

st.markdown(
    '<div class="emergency-btn-container">',
    unsafe_allow_html=True
)

if st.button(
    "🚨 EMERGENCY SAFEGUARD",
    key="emergency_main_btn",
    type="primary"
):

    st.session_state.emergency_triggered = True

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# EMERGENCY WORKFLOW
# =========================================================

if st.session_state.emergency_triggered:


    st.error("🚨 EMERGENCY ALERT ACTIVATED")
    save_emergency_alert(
    st.session_state.current_place
)

    st.success(
        "✅ Nearby police stations and emergency "
        "response teams have been notified."
    )

    st.warning(
        "🚔 Your live location and emergency "
        "details were shared successfully."
    )

    st.markdown(
        "## 🛡️ Emergency Response Activated"
    )

    if (
        st.session_state.global_latitude
        and
        st.session_state.global_longitude
    ):

        st.success(
            f"📍 Current Location: "
            f"{st.session_state.current_place}"
        )

        emergency_map = pd.DataFrame(
            {
                "lat": [
                    st.session_state.global_latitude
                ],
                "lon": [
                    st.session_state.global_longitude
                ]
            }
        )

        st.map(emergency_map)

        st.markdown(
            "### 🚔 Nearby Emergency Teams"
        )

        st.info(
            '''
            👮 Madhapur Police Station — 1.5 km away

            🚑 Apollo Emergency Response — 2.1 km away

            🚓 Highway Patrol Team — 3 mins ETA
            '''
        )

    else:

        st.warning(
            "⚠ Please allow browser location access"
        )    
# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🚗 OneTapResQ")

st.sidebar.write(
    f"Welcome, {st.session_state.username}"
)

st.sidebar.markdown("---")

# =====================================================
# USER ROLE BASED MENU
# =====================================================

if st.session_state.user_role == "admin":

    menu_options = [
        "🏠 Home",
        "⛽ Community Fuel Share",
        "🔧 Mechanic Service",
        "⚡ EV Charging Service",
        "🛠 Admin Dashboard"
    ]

else:

    menu_options = [
        "🏠 Home",
        "⛽ Community Fuel Share",
        "🔧 Mechanic Service",
        "⚡ EV Charging Service"
    ]

service_option = st.sidebar.radio(
    "Choose Service",
    menu_options
)

st.sidebar.markdown("---")

st.sidebar.success("Live Support Active")

# =====================================================
# LOGOUT BUTTON
# =====================================================

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False

    st.session_state.username = ""

    st.session_state.user_role = ""

    st.rerun()

# =========================================================
# HOME PAGE
# =========================================================

if service_option == "🏠 Home":

    st.title("🚨 Welcome to OneTapResQ")

    st.subheader(
        "One Click Vehicle Emergency & Safety Assistance"
    )

    st.caption(
        "Smart roadside assistance with fuel sharing, "
        "mechanic support, live location tracking, "
        "and safety features."
    )

    st.markdown(
        """
        <div class="welcome-box">

        <h2>Why OneTapResQ?</h2>

        <ul>
            <li>⛽ Fuel shortages</li>
            <li>🔧 Vehicle breakdowns</li>
            <li>🛞 Flat tires</li>
            <li>🔋 Battery issues</li>
            <li>🚗 Roadside assistance</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            """
            <div class="feature-card">
                <h2>⛽</h2>
                <h3>Fuel Sharing</h3>
                <p>Get help from nearby users.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="feature-card">
                <h2>🔧</h2>
                <h3>Mechanic Support</h3>
                <p>Connect with nearby mechanics instantly.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            """
            <div class="feature-card">
                <h2>⚡</h2>
                <h3>EV Charging Analyzer</h3>
                <p>Analyze battery range and find nearby charging stations.</p>
            </div>
            """,
            unsafe_allow_html=True
         )

    st.markdown("---")

    img1, img2 = st.columns(2)

    with img1:

       st.image(
          "fuel_help.png",
          caption="⛽ Community Fuel Assistance",
          width=330
          )

    with img2:

       st.image(
          "mechanic_help.png",
          caption="🔧 Nearby Mechanic Support",
          width=330
           )

    img3, img4 = st.columns(2)

    with img3:

      st.image(
         "EV_charging_station.png",
         caption="⚡ EV Charging Assistance",
         width=330
    )

    with img4:

      st.image(
          "Rescue_team.png",
           caption="🚨 Emergency Rescue Team",
           width=330
    )  

# =========================================================
# COMMUNITY FUEL SHARE
# =========================================================

elif service_option == "⛽ Community Fuel Share":

    import time

    st.title("⛽ Community Fuel Share")

    st.subheader(
        "Find nearby users who can help you"
    )

    st.markdown("---")

    users = [
        {
            "name": "John",
            "distance": "1.2 km away",
            "phone": "9876543210",
            "place": "Madhapur, Hyderabad",
            "lat": 17.3850,
            "lon": 78.4867
        },
        {
            "name": "Priya",
            "distance": "1.8 km away",
            "phone": "9123456780",
            "place": "Gachibowli, Hyderabad",
            "lat": 17.3925,
            "lon": 78.4812
        },
        {
            "name": "Arjun",
            "distance": "2.5 km away",
            "phone": "9012345678",
            "place": "Kukatpally, Hyderabad",
            "lat": 17.4018,
            "lon": 78.4920
        }
    ]

    for user in users:

        col1, col2 = st.columns([5,2])

        with col1:

            st.markdown(
                f"""
                ### 👤 {user['name']}

                📍 {user['distance']}
                """
            )

        with col2:

            request_key = f"{user['name']}_request"

            accept_key = f"{user['name']}_accept"

            if request_key not in st.session_state:
                st.session_state[request_key] = False

            if accept_key not in st.session_state:
                st.session_state[accept_key] = False

            request_clicked = st.button(
                "Request",
                key=f"{request_key}_btn"
            )

            if request_clicked:

                with st.spinner(
                    "🔍 Searching nearby helpers..."
                ):

                    time.sleep(3)

                st.session_state[request_key] = True

            # =====================================================
            # AFTER REQUEST ACCEPTED
            # =====================================================

            if st.session_state.get(request_key, False):

                st.success(
                    f"✅ {user['name']} accepted your request"
                )

                accept_clicked = st.button(
                    f"Simulate {user['name']} Acceptance",
                    key=f"{accept_key}_btn"
                )

                if accept_clicked:

                    st.session_state[accept_key] = True

            # =====================================================
            # SHOW HELPER DETAILS
            # =====================================================

            if st.session_state.get(accept_key, False):

                st.success(
                    f"🚗 {user['name']} is on the way"
                )

                save_fuel_request(
                    user["name"],
                    user["phone"],
                    user["place"]
                )

                st.write(
                    f"📞 Phone: {user['phone']}"
                )

                st.write(
                    f"📍 {user['place']}"
                )

                helper_map = pd.DataFrame(
                    {
                        "lat": [user["lat"]],
                        "lon": [user["lon"]]
                    }
                )

                st.markdown(
                    "### 📍 Live Helper Location"
                )

                st.map(helper_map)

        st.markdown("---")
# =========================================================
# MECHANIC SERVICE
# =========================================================

elif service_option == "🔧 Mechanic Service":

    st.title("🔧 Mechanic Assistance")

    st.subheader(
        "Get instant roadside mechanic support"
    )

    st.markdown("---")

    st.markdown("## 🚗 Request Assistance")

    name = st.text_input("👤 Your Name")

    phone = st.text_input("📞 Phone Number")

    vehicle = st.selectbox(
        "🚘 Vehicle Type",
        ["Bike", "Car", "Truck", "Auto", "Scooty"]
    )

    issue = st.selectbox(
        "🛠 Emergency Issue",
        [
            "Fuel Delivery",
            "Flat Tire",
            "Battery Problem",
            "Mechanical Breakdown",
            "Engine Overheating"
        ]
    )

    help_type = st.radio(
        "🙋 Who Needs Help?",
        ["Me", "Someone Else"]
    )

    final_location = "Not Available"

    # =====================================================
    # LOCATION SECTION
    # =====================================================

    if help_type == "Me":

        st.markdown("### 📍 Current Live Location")

        if (
            st.session_state.global_latitude
            and
            st.session_state.global_longitude
        ):

            st.success(
                f"📍 Current Location: "
                f"{st.session_state.current_place}"
            )

            map_data = pd.DataFrame(
                {
                    "lat": [
                        st.session_state.global_latitude
                    ],
                    "lon": [
                        st.session_state.global_longitude
                    ]
                }
            )

            st.map(map_data)

        else:

            st.warning(
                "⚠ Please allow browser "
                "location access"
            )

    else:

        final_location = st.text_input(
            "📍 Paste Google Maps Location Link"
        )

    st.markdown("---")

    # =====================================================
    # SUBMIT DETAILS
    # =====================================================

    if st.button("✅ Submit Details"):

        st.success(
            "Details Submitted Successfully"
        )

        save_mechanic_request(
           name,
           phone,
           vehicle,
           issue,
           help_type,
           st.session_state.current_place
         )

        st.markdown("## 📋 Submitted Details")

        st.write("👤 Name:", name)

        st.write("📞 Phone:", phone)

        st.write("🚘 Vehicle:", vehicle)

        st.write("🛠 Issue:", issue)

        st.write("🙋 Help Type:", help_type)

        if help_type == "Me":

            st.write(
                "📍 Current Location:",
                st.session_state.current_place
            )

            if (
                st.session_state.global_latitude
                and
                st.session_state.global_longitude
            ):

                submitted_map = pd.DataFrame(
                    {
                        "lat": [
                            st.session_state.global_latitude
                        ],
                        "lon": [
                            st.session_state.global_longitude
                        ]
                    }
                )

                st.map(submitted_map)

        else:

            st.write(
                "📍 Shared Location:",
                final_location
            )

        st.session_state.show_mechanics = True

    # =====================================================
    # SHOW MECHANICS
    # =====================================================

    if st.session_state.show_mechanics:

        st.markdown("## 🔧 Nearby Mechanics")

        mech1_col1, mech1_col2 = st.columns([5, 2])

        with mech1_col1:

            st.markdown(
                """
                ### 👨‍🔧 Ramesh Auto Garage

                ⭐ 4.8 • 📍 1.2 km away • ⏱ 8 mins ETA
                """
            )

        with mech1_col2:

            if st.button(
                "Request",
                key="m1"
            ):

                st.session_state.m1_requested = True

            if st.session_state.get(
                "m1_requested",
                False
            ):

                st.warning("⏳ Request Pending")

                st.info(
                    "Waiting for mechanic approval..."
                )

                if st.button(
                    "Simulate Mechanic Accept",
                    key="m1_accept"
                ):

                    st.session_state.m1_accepted = True

            if st.session_state.get(
                "m1_accepted",
                False
            ):

                st.success(
                    "✅ Mechanic Accepted "
                    "Your Request"
                )

                st.write(
                    "📞 Phone: 9876501234"
                )

                st.write(
                    "📍 Madhapur, Hyderabad"
                )

                st.write(
                    "🚘 Mechanic On The Way"
                )

                mechanic_live_map = pd.DataFrame(
                    {
                        "lat": [17.3855],
                        "lon": [78.4875]
                    }
                )

                st.markdown(
                    "### 📍 Live Mechanic Location"
                )

                st.map(mechanic_live_map)
# =========================================================
# EV CHARGING SERVICE
# =========================================================

elif service_option == "⚡ EV Charging Service":

    st.title("⚡ EV Charging Assistance")

    st.subheader(
        "Smart EV Support & Charging Assistance"
    )

    st.markdown("---")

    # =====================================================
    # VEHICLE TYPE
    # =====================================================

    ev_vehicle = st.selectbox(
        "🚘 Select EV Vehicle Type",
        [
            "Electric Car",
            "Electric Bike",
            "Electric Scooty",
            "Electric Auto",
            "Electric Truck"
        ]
    )

    st.success(
        f"✅ Selected Vehicle: {ev_vehicle}"
    )

    st.markdown("---")

    # =====================================================
    # BATTERY PERCENTAGE
    # =====================================================

    battery_percentage = st.slider(
        "🔋 Current Battery Percentage",
        0,
        100,
        50
    )

    st.write(
        f"🔋 Battery Level: "
        f"{battery_percentage}%"
    )

    st.markdown("---")

    # =====================================================
    # ESTIMATED RANGE
    # =====================================================

    if ev_vehicle == "Electric Car":

        estimated_range = battery_percentage * 5

    elif ev_vehicle == "Electric Bike":

        estimated_range = battery_percentage * 2

    elif ev_vehicle == "Electric Scooty":

        estimated_range = battery_percentage * 1.5

    elif ev_vehicle == "Electric Auto":

        estimated_range = battery_percentage * 3

    else:

        estimated_range = battery_percentage * 4

    st.success(
        f"🚘 Estimated Travel Range: "
        f"{estimated_range} km"
    )
    if st.button("💾 Save EV Request"):

      save_ev_request(
        ev_vehicle,
        battery_percentage,
        estimated_range
      )

      st.success(
        "✅ EV Request Saved Successfully"
      )

    st.markdown("---")

    # =====================================================
    # LOW BATTERY ALERT
    # =====================================================

    if battery_percentage <= 20:

        st.error(
            "⚠ Battery Low! "
            "Charging Recommended."
        )

        st.info(
            "📍 Suggested Nearby Charging Station:"
        )

        st.success(
            "⚡ ChargePoint EV Hub "
            "- Madhapur, Hyderabad"
        )

        charging_map = pd.DataFrame(
            {
                "lat": [17.3858],
                "lon": [78.4869]
            }
        )

        st.map(charging_map)

        st.write(
            "⚡ Suggested because it is "
            "nearest to your current location."
        )

    else:

        st.success(
            "✅ Battery level sufficient "
            "for travel."
        )     
# =========================================================
# ADMIN DASHBOARD
# =========================================================

elif service_option == "🛠 Admin Dashboard":

    st.title("🛠 Admin Dashboard")

    st.subheader(
        "Monitor All Service Requests"
    )

    st.markdown("---")

    # =====================================================
    # FETCH DATABASE DATA
    # =====================================================

    all_requests = get_mechanic_requests()

    emergency_alerts = get_emergency_alerts()

    fuel_requests = get_fuel_requests()

    ev_requests = get_ev_requests()

    # =====================================================
    # MECHANIC REQUESTS
    # =====================================================

    st.markdown("## 🔧 Mechanic Requests")

    if all_requests:

        for request in all_requests:

            st.markdown(
                f"""
                ### 🚗 Request ID: {request[0]}

                👤 Name: {request[1]}

                📞 Phone: {request[2]}

                🚘 Vehicle: {request[3]}

                🛠 Issue: {request[4]}

                🙋 Help Type: {request[5]}

                📍 Location: {request[6]}
                """
            )

            st.markdown("---")

    else:

        st.warning(
            "No mechanic requests available"
        )

    # =====================================================
    # EMERGENCY ALERTS
    # =====================================================

    st.markdown("## 🚨 Emergency Alerts")

    if emergency_alerts:

        for alert in emergency_alerts:

            st.error(
                f"""
                🚨 Alert ID: {alert[0]}

                📍 Location: {alert[1]}
                """
            )

    else:

        st.info(
            "No emergency alerts available"
        )

    # =====================================================
    # FUEL SHARE REQUESTS
    # =====================================================

    st.markdown("## ⛽ Fuel Share Requests")

    if fuel_requests:

        for fuel in fuel_requests:

            st.success(
                f"""
                ⛽ Request ID: {fuel[0]}

                👤 Helper Name: {fuel[1]}

                📞 Phone: {fuel[2]}

                📍 Location: {fuel[3]}
                """
            )

    else:

        st.info(
            "No fuel share requests available"
        )

    # =====================================================
    # EV REQUESTS
    # =====================================================

    st.markdown("## ⚡ EV Requests")

    if ev_requests:

        for ev in ev_requests:

            st.info(
                f"""
                ⚡ Request ID: {ev[0]}

                🚘 Vehicle Type: {ev[1]}

                🔋 Battery Percentage: {ev[2]}%

                🛣 Estimated Range: {ev[3]} km
                """
            )

    else:

        st.info(
            "No EV requests available"
        )