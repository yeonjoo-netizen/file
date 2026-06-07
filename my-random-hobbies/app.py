import streamlit as st
import json
import random
import time
import os
from datetime import date

DATA_FILE = "data.json"

st.set_page_config(page_title="나의 랜덤 취미(관심영역)", page_icon="🎲", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "홈"
if "theme" not in st.session_state:
    st.session_state.theme = "블랙 (다크모드)"

def change_page(page_name):
    st.session_state.page = page_name
    st.rerun()

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "daily_reviews" not in data:
                data["daily_reviews"] = []
            return data
    return {"book_reviews": [], "food_reviews": [], "custom_games": {"PC": [], "Mobile": [], "Nintendo": []}, "daily_reviews": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def inject_theme(theme_name):
    if theme_name == "화이트 (라이트모드)":
        css = """
        <style>
        .stApp { background-color: #FFFFFF; }
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdownContainer p, span, li { 
            color: #000000 !important; 
        }
        input, textarea, div[data-baseweb="select"] > div, div[data-baseweb="popover"], .stButton > button, div[data-baseweb="calendar"], div[data-baseweb="calendar"] * {
            background-color: #F0F2F6 !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }
        /* 드롭다운 리스트(테마 고를 때 뜨는 창) 보정 */
        ul[role="listbox"], li[role="option"] {
            background-color: #F0F2F6 !important;
            color: #000000 !important;
        }
        li[role="option"]:hover { background-color: #DDDDDD !important; }
        button[data-testid="baseButton-primary"] p { color: white !important; }
        </style>
        """
    else: # 블랙 (다크)
        css = """
        <style>
        .stApp { background-color: #121212; }
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdownContainer p, span, li { 
            color: #FFFFFF !important; 
        }
        input, textarea, div[data-baseweb="select"] > div, div[data-baseweb="popover"], .stButton > button, div[data-baseweb="calendar"], div[data-baseweb="calendar"] * {
            background-color: #2B2B2B !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border-color: #444444 !important;
        }
        /* 드롭다운 리스트(테마 고를 때 뜨는 창) 보정 */
        ul[role="listbox"], li[role="option"] {
            background-color: #2B2B2B !important;
            color: #FFFFFF !important;
        }
        li[role="option"]:hover { background-color: #444444 !important; }
        .stTabs [data-baseweb="tab"] p { color: #FFFFFF !important; }
        </style>
        """
    
    # Red button CSS for primary buttons (Emoji button)
    css += """
    <style>
    button[data-testid="baseButton-primary"] {
        background-color: #FF3333 !important;
        border: 2px solid #CC0000 !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }
    button[data-testid="baseButton-primary"] p {
        font-size: 80px !important;
        color: white !important;
        margin: 0 !important;
        -webkit-text-fill-color: white !important;
    }
    button[data-testid="baseButton-primary"]:hover {
        background-color: #FF5555 !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def slot_machine_effect(placeholder, emojis, final_result, duration=1.5):
    end_time = time.time() + duration
    while time.time() < end_time:
        placeholder.markdown(f"<h1 style='text-align: center; font-size: 150px;'>{random.choice(emojis)}</h1>", unsafe_allow_html=True)
        time.sleep(0.1)
    placeholder.markdown(f"<h1 style='text-align: center; font-size: 150px;'>{final_result}</h1>", unsafe_allow_html=True)

def render_grid_roulette(placeholder, highlight_idx):
    html = "<table style='margin: auto; border-collapse: separate; border-spacing: 10px;'>"
    for r in range(4):
        html += "<tr>"
        for c in range(4):
            idx = r * 4 + c + 1
            bg_color = "#FF4B4B" if idx == highlight_idx else "#333333"
            html += f"<td style='width: 80px; height: 80px; background-color: {bg_color}; border-radius: 10px; text-align: center; vertical-align: middle; font-size: 24px; font-weight: bold; color: white !important;'>{idx}</td>"
        html += "</tr>"
    html += "</table>"
    placeholder.markdown(html, unsafe_allow_html=True)

def render_navigation():
    st.write("---")
    st.markdown("<h3 style='text-align: center;'>네비게이션 메뉴</h3>", unsafe_allow_html=True)
    # 후기를 랜덤(네비게이션) 메뉴에서 빼고 4개로 원복
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("🏠 홈", use_container_width=True): change_page("홈")
    if col2.button("📚 도서", use_container_width=True): change_page("도서 📚")
    if col3.button("🎮 게임", use_container_width=True): change_page("게임 🎮")
    if col4.button("🍔 음식", use_container_width=True): change_page("음식 🍔")
    
    st.write("---")
    new_theme = st.selectbox(
        "테마 설정", 
        ["블랙 (다크)", "화이트 (라이트)"], 
        index=["블랙 (다크)", "화이트 (라이트)"].index(st.session_state.theme) if st.session_state.theme in ["블랙 (다크)", "화이트 (라이트)"] else 0
    )
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

def main():
    inject_theme(st.session_state.theme)
    data = load_data()
    
    if st.session_state.page == "홈":
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 70px;'>나의 랜덤 취미 🎲</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #AAAAAA;'>오늘은 무엇을 랜덤으로 할까?</h2>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        
        # 왼쪽에 공간을 두어 랜덤 뽑기와 완전히 분리된 느낌을 줌
        col_review, col_gap, col_main, col_right = st.columns([1, 1, 4, 2])
        
        with col_review:
            st.markdown("<h4 style='text-align: center;'>후기</h4>", unsafe_allow_html=True)
            if st.button("📝", key="go_review_home", use_container_width=True):
                change_page("후기 📝")
                
        with col_main:
            st.markdown("<br>", unsafe_allow_html=True) # 줄맞춤용
            if st.button("🎲 당첨 뽑기 시작!", use_container_width=True):
                st.session_state.home_result = random.choice([("도서 📚", "📚"), ("게임 🎮", "🎮"), ("음식 🍔", "🍔")])
                st.session_state.slot_done = False
                
        if "home_result" in st.session_state:
            placeholder = st.empty()
            chosen = st.session_state.home_result
            
            if not st.session_state.get("slot_done", False):
                slot_machine_effect(placeholder, ["📚", "🎮", "🍔", "🎲", "🎯"], chosen[1])
                st.session_state.slot_done = True
            else:
                placeholder.markdown(f"<h1 style='text-align: center; font-size: 150px;'>{chosen[1]}</h1>", unsafe_allow_html=True)
            
            st.markdown(f"<h2 style='text-align: center;'>축하합니다! 오늘은 **{chosen[0]}** 당첨!</h2>", unsafe_allow_html=True)
            
            # 당첨 후 아래에 뜨는 이모지 바로가기 버튼과 다시 뽑기 버튼
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col2:
                if st.button(chosen[1], key="goto_btn", type="primary", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        if key.startswith("book_") or key.startswith("game_") or key.startswith("food_"):
                            del st.session_state[key]
                    change_page(chosen[0])
            with col3:
                if st.button("🔄", key="home_reroll", type="primary", use_container_width=True):
                    st.session_state.home_result = random.choice([("도서 📚", "📚"), ("게임 🎮", "🎮"), ("음식 🍔", "🍔")])
                    st.session_state.slot_done = False
                    st.rerun()

    elif st.session_state.page == "도서 📚":
        st.markdown("<h1 style='text-align: center; font-size: 90px;'>도서 카테고리 📚</h1>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["랜덤 추천 🎰", "리뷰 작성 ✍️", "리뷰 목록 📖"])
        with tab1:
            st.markdown("<h3 style='text-align: center;'>어디에서 책을 고를까요?</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🏛️ 도서관 바로가기", use_container_width=True):
                    st.session_state.book_place = ("도서관 🏛️", "🏛️")
                    st.session_state.book_drawer = None
                    st.session_state.book_book_idx = None
                    st.session_state.book_place_anim_done = True
            with col2:
                if st.button("📚 내 서재 바로가기", use_container_width=True):
                    st.session_state.book_place = ("서재 📚", "📚")
                    st.session_state.book_drawer = None
                    st.session_state.book_book_idx = None
                    st.session_state.book_place_anim_done = True
            with col3:
                if st.button("🎲 장소 무작위 뽑기!", use_container_width=True):
                    st.session_state.book_place = random.choice([("도서관 🏛️", "🏛️"), ("서재 📚", "📚")])
                    st.session_state.book_drawer = None
                    st.session_state.book_book_idx = None
                    st.session_state.book_place_anim_done = False
            
            if "book_place" in st.session_state:
                place, emoji = st.session_state.book_place
                
                if not st.session_state.get("book_place_anim_done", True):
                    placeholder = st.empty()
                    slot_machine_effect(placeholder, ["🏛️", "📚", "📖", "🏫", "🎲"], emoji)
                    st.session_state.book_place_anim_done = True
                    placeholder.empty()
                    
                st.markdown(f"<h2 style='text-align: center;'>👉 **{place}**</h2>", unsafe_allow_html=True)
                
                if place == "서재 📚":
                    st.write("---")
                    st.markdown("<h3 style='text-align: center;'>내 서재에서 무작위 칸 고르기</h3>", unsafe_allow_html=True)
                    
                    grid_placeholder = st.empty()
                    
                    if st.button("서재 4x4 룰렛 돌리기 🎰", use_container_width=True):
                        st.session_state.book_drawer = None
                        st.session_state.book_book_idx = None
                        
                        for _ in range(20):
                            highlight = random.randint(1, 16)
                            render_grid_roulette(grid_placeholder, highlight)
                            time.sleep(0.1)
                        final_drawer = random.randint(1, 16)
                        st.session_state.book_drawer = final_drawer
                    
                    if st.session_state.get("book_drawer") is not None:
                        drawer = st.session_state.book_drawer
                        render_grid_roulette(grid_placeholder, drawer)
                        
                        st.success(f"당첨! **{drawer}번 서랍**이 선택되었습니다.")
                        
                        st.markdown("<br><h3>선택된 칸에는 총 몇 권의 책이 있습니까?</h3>", unsafe_allow_html=True)
                        book_count = st.number_input("책 개수", min_value=1, value=1, step=1)
                        
                        if st.button("이 서랍에서 책 뽑기 🎲", use_container_width=True):
                            idx_ph = st.empty()
                            for _ in range(15):
                                idx_ph.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{random.randint(1, book_count)}</h1>", unsafe_allow_html=True)
                                time.sleep(0.1)
                            final_book = random.randint(1, book_count)
                            idx_ph.markdown(f"<h1 style='text-align: center; font-size: 80px; color: #FF4B4B;'>{final_book}</h1>", unsafe_allow_html=True)
                            st.session_state.book_book_idx = final_book
                        
                        if st.session_state.get("book_book_idx") is not None:
                            st.success(f"최종 당첨! **{drawer}번 서랍의 {st.session_state.book_book_idx}번째 책**을 읽으세요!")
                            col_a, col_b, col_c = st.columns([1,1,1])
                            with col_b:
                                if st.button("🔄", key="study_reroll", type="primary", use_container_width=True):
                                    st.session_state.book_book_idx = random.randint(1, book_count)
                                    st.rerun()

                elif place == "도서관 🏛️":
                    st.write("---")
                    st.markdown("<h3 style='text-align: center;'>도서관에서 책 빌리기</h3>", unsafe_allow_html=True)
                    genre = st.selectbox("장르 선택", ["소설", "비문학", "만화/웹툰", "자기계발", "무작위"])
                    books_db = {
                        "소설": ["불편한 편의점", "달러구트 꿈 백화점", "아몬드"],
                        "비문학": ["사피엔스", "이기적 유전자", "코스모스"],
                        "만화/웹툰": ["나 혼자만 레벨업", "전지적 독자 시점", "화산귀환"],
                        "자기계발": ["역행자", "타이탄의 도구들", "아토믹 해빗"]
                    }
                    if st.button("도서관에서 책 추천받기 🎰", use_container_width=True):
                        g = random.choice(list(books_db.keys())) if genre == "무작위" else genre
                        st.session_state.lib_book = random.choice(books_db[g])
                        st.session_state.lib_genre = g
                        st.session_state.lib_anim_done = False
                        
                    if "lib_book" in st.session_state:
                        placeholder = st.empty()
                        if not st.session_state.get("lib_anim_done"):
                            slot_machine_effect(placeholder, ["📚", "📖", "📓", "📔", "📕", "📗"], "📚")
                            st.session_state.lib_anim_done = True
                        else:
                            placeholder.markdown("<h1 style='text-align: center; font-size: 150px;'>📚</h1>", unsafe_allow_html=True)
                        st.success(f"당첨! 추천 도서는 **[{st.session_state.lib_book}]** 입니다!")
                        col_a, col_b, col_c = st.columns([1,1,1])
                        with col_b:
                            if st.button("🔄", key="lib_reroll", type="primary", use_container_width=True):
                                st.session_state.lib_book = random.choice(books_db[st.session_state.lib_genre])
                                st.session_state.lib_anim_done = False
                                st.rerun()
        
        with tab2:
            st.subheader("리뷰 작성")
            book_name = st.text_input("책 이름 (필수)")
            author = st.text_input("저자 (필수)")
            read_time = st.text_input("읽은 시간 (예: 2시간)")
            rating = st.slider("도서 별점 (필수)", 1, 5, 5, step=1)
            st.markdown(f"<h3 style='color: gold;'>{'⭐'*rating}{'☆'*(5-rating)}</h3>", unsafe_allow_html=True)
            review = st.text_area("한 줄 평")
            if st.button("도서 리뷰 저장하기", use_container_width=True):
                if not book_name or not author:
                    st.error("책 이름과 저자는 필수 항목입니다.")
                else:
                    data["book_reviews"].append({"name": book_name, "author": author, "time": read_time, "rating": rating, "review": review})
                    save_data(data)
                    st.success("도서 리뷰가 저장되었습니다!")
        with tab3:
            st.subheader("나의 도서 리뷰")
            if not data["book_reviews"]:
                st.info("작성된 리뷰가 없습니다.")
            for r in reversed(data["book_reviews"]):
                st.markdown(f"**{r['name']}** (저자: {r['author']}) - {'⭐'*int(r['rating'])}{'☆'*(5-int(r['rating']))}")
                st.write(f"- 읽은 시간: {r['time']}\n- 한 줄 평: {r['review']}")
                st.write("---")

    elif st.session_state.page == "게임 🎮":
        st.markdown("<h1 style='text-align: center; font-size: 90px;'>게임 카테고리 🎮</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["게임 뽑기 🎲", "게임 설정(수정) ⚙️"])
        with tab1:
            st.markdown("<h3 style='text-align: center;'>추천 방식을 선택해서 버튼을 눌러주세요!</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("100% 전체 무작위 🎲", use_container_width=True):
                    all_games = []
                    for p, g_list in data["custom_games"].items():
                        all_games.extend([(p, g) for g in g_list])
                    if not all_games:
                        st.warning("등록된 게임이 없습니다.")
                    else:
                        st.session_state.game_mode = "all"
                        st.session_state.game_result = random.choice(all_games)
                        st.session_state.game_anim_done = False
            with col2:
                if st.button("카테고리 무작위 🎰", use_container_width=True):
                    st.session_state.game_mode = "cat"
                    plat_choices = [("PC", "💻"), ("Mobile", "📱"), ("Nintendo", "🕹️")]
                    st.session_state.game_won_plat_tuple = random.choice(plat_choices)
                    st.session_state.game_final_result = None
                    st.session_state.game_plat_anim_done = False

            if st.session_state.get("game_mode") == "all":
                st.write("---")
                chosen_p, chosen_g = st.session_state.game_result
                placeholder = st.empty()
                if not st.session_state.get("game_anim_done"):
                    slot_machine_effect(placeholder, ["🎮", "🕹️", "👾", "🎲", "📱", "💻"], "🎮")
                    st.session_state.game_anim_done = True
                else:
                    placeholder.markdown(f"<h1 style='text-align: center; font-size: 150px;'>🎮</h1>", unsafe_allow_html=True)
                st.success(f"당첨! 추천 게임은 **[{chosen_g}]** ({chosen_p}) 입니다!")
                col_a, col_b, col_c = st.columns([1,1,1])
                with col_b:
                    if st.button("🔄", key="game_all_reroll", type="primary", use_container_width=True):
                        all_games = []
                        for p, g_list in data["custom_games"].items():
                            all_games.extend([(p, x) for x in g_list])
                        st.session_state.game_result = random.choice(all_games)
                        st.session_state.game_anim_done = False
                        st.rerun()

            elif st.session_state.get("game_mode") == "cat":
                st.write("---")
                plat, emoji = st.session_state.game_won_plat_tuple
                
                placeholder = st.empty()
                if not st.session_state.get("game_plat_anim_done", True):
                    slot_machine_effect(placeholder, ["💻", "📱", "🕹️", "🎮", "👾"], emoji)
                    st.session_state.game_plat_anim_done = True
                else:
                    placeholder.markdown(f"<h1 style='text-align: center; font-size: 150px;'>{emoji}</h1>", unsafe_allow_html=True)
                    
                st.success(f"👉 카테고리는? **{plat}** {emoji}")
                
                if st.session_state.get("game_final_result") is None:
                    if st.button("OK (이 카테고리 내에서 게임 뽑기!) 🎲", use_container_width=True):
                        games = data["custom_games"].get(plat, [])
                        if not games:
                            st.warning(f"[{plat}]에 등록된 게임이 없습니다.")
                        else:
                            st.session_state.game_final_result = random.choice(games)
                            st.session_state.game_final_anim_done = False
                            st.rerun()
                
                if st.session_state.get("game_final_result") is not None:
                    final_placeholder = st.empty()
                    if not st.session_state.get("game_final_anim_done"):
                        slot_machine_effect(final_placeholder, ["🎮", "🕹️", "👾", "🎲", "📱", "💻"], "🎮")
                        st.session_state.game_final_anim_done = True
                    else:
                        final_placeholder.markdown(f"<h1 style='text-align: center; font-size: 150px;'>🎮</h1>", unsafe_allow_html=True)
                    st.success(f"최종 당첨! 추천 게임은 **[{st.session_state.game_final_result}]** ({plat}) 입니다!")
                    col_a, col_b, col_c = st.columns([1,1,1])
                    with col_b:
                        if st.button("🔄", key="game_fin_reroll", type="primary", use_container_width=True):
                            games = data["custom_games"].get(plat, [])
                            st.session_state.game_final_result = random.choice(games)
                            st.session_state.game_final_anim_done = False
                            st.rerun()
        
        with tab2:
            st.subheader("내가 설정한 게임 보기 및 수정")
            for p in ["PC", "Mobile", "Nintendo"]:
                st.markdown(f"#### {p}")
                games = data["custom_games"].get(p, [])
                if not games:
                    st.info("등록된 게임이 없습니다.")
                for i, g in enumerate(games):
                    col1, col2 = st.columns([4, 1])
                    col1.write(f"🎮 {g}")
                    if col2.button("삭제", key=f"del_{p}_{i}"):
                        data["custom_games"][p].remove(g)
                        save_data(data)
                        st.rerun()
                st.write("---")

            st.subheader("새 게임 추가")
            new_game_name = st.text_input("새로운 게임 이름 (필수)")
            new_platform = st.selectbox("추가할 플랫폼", ["PC", "Mobile", "Nintendo"])
            if st.button("리스트에 추가하기", use_container_width=True):
                if not new_game_name:
                    st.error("게임 이름을 입력해주세요.")
                elif new_game_name not in data["custom_games"][new_platform]:
                    data["custom_games"][new_platform].append(new_game_name)
                    save_data(data)
                    st.rerun()
                else:
                    st.info("이미 존재하는 게임입니다.")

    elif st.session_state.page == "음식 🍔":
        st.markdown("<h1 style='text-align: center; font-size: 90px;'>음식 카테고리 🍔</h1>", unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["랜덤 메뉴 추천 🎰", "리뷰 작성 ✍️", "리뷰 목록 🍽️"])
        with tab1:
            st.markdown("<h3 style='text-align: center;'>오늘 뭐 먹지? 추천 방식을 선택하세요!</h3>", unsafe_allow_html=True)
            
            food_db = {
                "한식": ["김치찌개", "비빔밥", "삼겹살", "불고기", "떡볶이", "국밥"],
                "중식": ["짜장면", "짬뽕", "탕수육", "마라탕", "볶음밥"],
                "일식": ["초밥", "돈까스", "우동", "라멘", "회"],
                "양식": ["파스타", "피자", "스테이크", "햄버거", "리조또"]
            }
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("100% 전체 무작위 🎲", use_container_width=True):
                    st.session_state.food_mode = "all"
                    all_foods = [item for sublist in food_db.values() for item in sublist]
                    st.session_state.food_result = random.choice(all_foods)
                    st.session_state.food_anim_done = False
            with col2:
                if st.button("카테고리 무작위 🎰", use_container_width=True):
                    st.session_state.food_mode = "cat"
                    cats = [("한식", "🇰🇷"), ("중식", "🇨🇳"), ("일식", "🇯🇵"), ("양식", "🇺🇸")]
                    st.session_state.food_won_cat_tuple = random.choice(cats)
                    st.session_state.food_final_result = None
                    st.session_state.food_cat_anim_done = False

            if st.session_state.get("food_mode") == "all":
                st.write("---")
                placeholder = st.empty()
                if not st.session_state.get("food_anim_done"):
                    slot_machine_effect(placeholder, ["🍔", "🍕", "🍣", "🍜", "🍛", "🌮", "🍲"], "🍽️")
                    st.session_state.food_anim_done = True
                else:
                    placeholder.markdown(f"<h1 style='text-align: center; font-size: 150px;'>🍽️</h1>", unsafe_allow_html=True)
                st.success(f"당첨! 오늘 추천 메뉴는 **[{st.session_state.food_result}]** 입니다!")
                col_a, col_b, col_c = st.columns([1,1,1])
                with col_b:
                    if st.button("🔄", key="food_all_reroll", type="primary", use_container_width=True):
                        food_db = {
                            "한식": ["김치찌개", "비빔밥", "삼겹살", "불고기", "떡볶이", "국밥"],
                            "중식": ["짜장면", "짬뽕", "탕수육", "마라탕", "볶음밥"],
                            "일식": ["초밥", "돈까스", "우동", "라멘", "회"],
                            "양식": ["파스타", "피자", "스테이크", "햄버거", "리조또"]
                        }
                        all_foods = [item for sublist in food_db.values() for item in sublist]
                        st.session_state.food_result = random.choice(all_foods)
                        st.session_state.food_anim_done = False
                        st.rerun()
            
            elif st.session_state.get("food_mode") == "cat":
                st.write("---")
                cat, emoji = st.session_state.food_won_cat_tuple
                
                placeholder = st.empty()
                if not st.session_state.get("food_cat_anim_done", True):
                    slot_machine_effect(placeholder, ["🇰🇷", "🇨🇳", "🇯🇵", "🇺🇸", "🍚", "🍝"], emoji)
                    st.session_state.food_cat_anim_done = True
                else:
                    placeholder.markdown(f"<h1 style='text-align: center; font-size: 150px;'>{emoji}</h1>", unsafe_allow_html=True)
                    
                st.success(f"👉 카테고리는? **{cat}** {emoji}")
                
                if st.session_state.get("food_final_result") is None:
                    if st.button("OK (이 카테고리 내에서 음식 뽑기!) 🎲", use_container_width=True):
                        st.session_state.food_final_result = random.choice(food_db[cat])
                        st.session_state.food_final_anim_done = False
                        st.rerun()
                
                if st.session_state.get("food_final_result") is not None:
                    final_placeholder = st.empty()
                    if not st.session_state.get("food_final_anim_done"):
                        slot_machine_effect(final_placeholder, ["🍔", "🍕", "🍣", "🍜", "🍛", "🌮", "🍲"], "🍽️")
                        st.session_state.food_final_anim_done = True
                    else:
                        final_placeholder.markdown(f"<h1 style='text-align: center; font-size: 150px;'>🍽️</h1>", unsafe_allow_html=True)
                    st.success(f"최종 당첨! 추천 음식은 **[{st.session_state.food_final_result}]** ({cat}) 입니다!")
                    col_a, col_b, col_c = st.columns([1,1,1])
                    with col_b:
                        if st.button("🔄", key="food_fin_reroll", type="primary", use_container_width=True):
                            food_db = {
                                "한식": ["김치찌개", "비빔밥", "삼겹살", "불고기", "떡볶이", "국밥"],
                                "중식": ["짜장면", "짬뽕", "탕수육", "마라탕", "볶음밥"],
                                "일식": ["초밥", "돈까스", "우동", "라멘", "회"],
                                "양식": ["파스타", "피자", "스테이크", "햄버거", "리조또"]
                            }
                            st.session_state.food_final_result = random.choice(food_db[cat])
                            st.session_state.food_final_anim_done = False
                            st.rerun()
        
        with tab2:
            st.subheader("리뷰 작성")
            restaurant_name = st.text_input("식당 이름 (필수)")
            rating = st.slider("별점 (필수)", 1, 5, 5, step=1)
            st.markdown(f"<h3 style='color: gold;'>{'⭐'*rating}{'☆'*(5-rating)}</h3>", unsafe_allow_html=True)
            review = st.text_area("상세 리뷰")
            
            if st.button("음식 리뷰 저장하기", use_container_width=True):
                if not restaurant_name:
                    st.error("식당 이름은 필수 항목입니다.")
                else:
                    data["food_reviews"].append({"name": restaurant_name, "rating": rating, "review": review})
                    save_data(data)
                    st.success("음식점 리뷰가 저장되었습니다!")
        with tab3:
            st.subheader("나의 음식점 리뷰")
            if not data["food_reviews"]:
                st.info("작성된 리뷰가 없습니다.")
            for r in reversed(data["food_reviews"]):
                st.markdown(f"**{r['name']}** - {'⭐'*int(r['rating'])}{'☆'*(5-int(r['rating']))}")
                st.write(f"- 리뷰: {r['review']}")
                st.write("---")

    elif st.session_state.page == "후기 📝":
        st.markdown("<h1 style='text-align: center; font-size: 90px;'>나의 취미 후기 📝</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🌟 오늘의 취미 후기 쓰기", "📚 지난 후기 모아보기"])
        
        with tab1:
            st.markdown("<h3 style='text-align: center;'>오늘의 취미는 어땠나요?</h3>", unsafe_allow_html=True)
            with st.form("daily_review_form"):
                today = st.date_input("날짜", date.today())
                cat = st.selectbox("어떤 카테고리를 즐기셨나요?", ["도서 📚", "게임 🎮", "음식 🍔"])
                rev = st.text_area("오늘의 한 줄 후기를 자유롭게 남겨주세요!")
                if st.form_submit_button("후기 등록하기", use_container_width=True):
                    if rev:
                        data["daily_reviews"].append({
                            "date": str(today),
                            "category": cat,
                            "review": rev
                        })
                        save_data(data)
                        st.success("오늘의 취미 후기가 등록되었습니다! 수고하셨어요!")
                    else:
                        st.error("후기를 입력해주세요.")
        
        with tab2:
            st.markdown("<h3>지금까지 남긴 취미 후기들</h3>", unsafe_allow_html=True)
            if not data["daily_reviews"]:
                st.info("아직 등록된 후기가 없습니다.")
            else:
                for r in reversed(data["daily_reviews"]):
                    st.markdown(f"**[{r['date']}] {r['category']}**")
                    st.write(f"💬 {r['review']}")
                    st.write("---")

    render_navigation()

if __name__ == "__main__":
    st.markdown("""
        <style>
            [data-testid="collapsedControl"] { display: none }
        </style>
    """, unsafe_allow_html=True)
    main()
