import streamlit as st
import random
import time

# --- [1. PAGE CONFIG & MOBILE OPTIMIZATION] ---
st.set_page_config(page_title="SAM.BRAWL - Ultimate Arena", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Mobile and Desktop
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bangers&display=swap');
    
    .stApp { background: #05050a; color: #fff; font-family: 'Segoe UI', sans-serif; }
    
    /* Arena styling */
    .arena-main {
        border: 4px solid #00d2ff;
        border-radius: 25px;
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://www.transparenttextures.com/patterns/dark-matter.png');
        height: 500px;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    /* Red Zone Effect */
    .red-zone {
        position: absolute;
        inset: 0;
        border: 25px solid rgba(255, 0, 0, 0.4);
        box-shadow: inset 0 0 60px #ff0000;
        animation: pulse 1s infinite alternate;
        pointer-events: none;
        z-index: 10;
    }
    @keyframes pulse { from { opacity: 0.4; } to { opacity: 0.9; } }

    /* Cartoon Character Animation */
    .linuz-3d {
        font-size: 100px;
        filter: drop-shadow(0 0 15px #ffae00);
        transition: transform 0.2s;
    }

    /* Mobile Button System (Custom HUD) */
    .controller-btn {
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid #fff;
        border-radius: 50%;
        color: white;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        user-select: none;
    }
</style>
""", unsafe_allow_html=True)

# --- [2. ENGINE: DATABASE & SESSION] ---
if 'db' not in st.session_state:
    st.session_state.db = {
        'user': 'LINUZ_HERO',
        'gold': 1000,
        'trophies': 500,
        'hp': 100,
        'gun': 'Pistolet 🔫',
        'hud_size': 60,  # Default button size
        'hud_pos': 'O\'ngda'
    }
if 'game_state' not in st.session_state:
    st.session_state.game_state = "Lobby"

# --- [3. SIDEBAR: SOZLAMALAR (SETTINGS)] ---
with st.sidebar:
    st.title("⚙️ SAM.BRAWL SETTINGS")
    st.write("---")
    
    # Custom HUD Settings
    st.subheader("HUD Sozlamalari (Telefon uchun)")
    st.session_state.db['hud_size'] = st.slider("Tugma hajmi", 40, 100, st.session_state.db['hud_size'])
    st.session_state.db['hud_pos'] = st.radio("Tugmalar joylashuvi", ["Chapda", "O'ngda"])
    
    st.write("---")
    if st.button("🗑 ACCOUNTNI O'CHIRISH", type="primary"):
        st.session_state.clear()
        st.rerun()

# --- [4. LOBBY: PROFILE & FRIENDS] ---
if st.session_state.game_state == "Lobby":
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        st.markdown(f"### 🏆 {st.session_state.db['trophies']}")
        st.markdown(f"### 💰 {st.session_state.db['gold']}")
        st.write("---")
        st.write("👥 **JO'RALAR (BOTS):**")
        st.caption("🟢 Samarqand_Boy")
        st.caption("🟢 Robot_KGO")
        st.caption("🔴 Hunter_Uz")

    with c2:
        st.markdown(f"<div style='text-align:center;'><div class='linuz-3d'>🦁</div><h1 style='font-family:Bangers; color:#00d2ff; font-size:60px;'>SAM.BRAWL</h1><p>Samarqand Arenasi: Binolar, Qurollar va Zona!</p></div>", unsafe_allow_html=True)
        if st.button("🔥 JANGNI BOSHLASH 🔥", use_container_width=True):
            st.session_state.game_state = "Battle"
            st.session_state.db['hp'] = 100
            st.rerun()

    with c3:
        st.markdown("### 🎒 INVENTAR")
        st.info(f"Qurol: {st.session_state.db['gun']}")
        if st.button("🛒 DO'KON"):
            st.toast("Tez kunda yangi qurollar!")

# --- [5. BATTLE: ARENA, BUILDINGS, ZONE] ---
elif st.session_state.game_state == "Battle":
    arena_ui = st.empty()
    controls = st.empty()
    battle_log = st.empty()
    
    players_left = 10
    zone_timer = 20 # 20 soniyadan keyin zona siqiladi
    
    for frame in range(40):
        time.sleep(0.8)
        
        # Zona Logic
        is_in_danger = frame > 15
        if is_in_danger:
            st.session_state.db['hp'] -= 8
            zone_html = "<div class='red-zone'></div>"
            zone_msg = "🚨 ZONA SIQILMOQDA! JON KAMAYYAPTI!"
        else:
            zone_html = ""
            zone_msg = f"⏱ Zona boshlanishiga: {max(0, 15-frame)}s"

        # Random Battle Events (Binolardan qurol topish)
        event = random.choice(["🏠 Binoga kirdi", "🔫 Avtomat topildi!", "🎯 Snayper!", "💥 Otishma!", "🚶 Sakrash"])
        if "Avtomat" in event: st.session_state.db['gun'] = "Avtomat 🔫🔥"
        if "Snayper" in event: st.session_state.db['gun'] = "Snayper 🔭"
        if "Otishma" in event: players_left -= 1

        # Render Arena
        arena_ui.markdown(f"""
        <div class='arena-main'>
            {zone_html}
            <div style='text-align:center;'>
                <div class='linuz-3d'>🦁</div>
                <h3 style='color:#00ff00;'>HP: {st.session_state.db['hp']}%</h3>
                <p style='color:#ffae00;'>{event}</p>
                <h2 style='color:#00d2ff;'>👥 TIRIKLAR: {players_left}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        battle_log.warning(zone_msg)

        # Custom HUD Buttons (Visual only for simulation)
        h_size = st.session_state.db['hud_size']
        controls.markdown(f"""
        <div style='display:flex; justify-content:space-around; padding:20px;'>
            <div class='controller-btn' style='width:{h_size}px; height:{h_size}px;'>🎯<br>OTISH</div>
            <div class='controller-btn' style='width:{h_size}px; height:{h_size}px;'>⬆️<br>SAKRA</div>
            <div class='controller-btn' style='width:{h_size}px; height:{h_size}px;'>⬇️<br>YOTISH</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.db['hp'] <= 0:
            st.error("💀 ZONADA HALOK BO'LDINGIZ!")
            st.session_state.game_state = "Lobby"
            time.sleep(3)
            st.rerun()
            break
        
        if players_left <= 1:
            st.success("🏆 BOOYAH! SAM.BRAWL CHEMPIONI!")
            st.balloons()
            st.session_state.db['gold'] += 500
            st.session_state.db['trophies'] += 50
            time.sleep(4)
            st.session_state.game_state = "Lobby"
            st.rerun()
            break
