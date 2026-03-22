import random
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================
# Page setup
# =========================
st.set_page_config(
    page_title="한자 공부",
    page_icon="📘",
    layout="centered",
)

# =========================
# Style (통합 및 최적화된 스타일)
# =========================
st.markdown(
    """
    <style>
    /* 1. 배경 및 전체 텍스트 다크모드 강제 고정 */
    .stApp {
        background-color: #0E1117 !important;
    }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3, span, div, label {
        color: #f7f9fc !important;
    }

    /* 2. 전체 컨테이너 (모바일 화면에 쏙 들어오게 다이어트) */
    .block-container {
        max-width: 550px !important; 
        padding-top: 1.5rem !important; 
        padding-bottom: 1.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        margin: 0 auto;
    }

    /* 3. 타이틀 스타일 (고정 크기 rem 대신 화면 비율 vw 사용) */
    .app-title {
        text-align: center;
        font-size: 8vw !important; 
        font-weight: 900;
        margin-top: 0rem;
        margin-bottom: 1.5rem;
        letter-spacing: -0.04em;
        line-height: 1.1;
    }

    .main-title {
        text-align: center;
        font-size: 9vw !important;
        font-weight: 900;
        margin: 0.5rem 0;
        line-height: 1.1;
    }

    .sub-title {
        text-align: center;
        font-size: 6vw !important;
        font-weight: 900;
        margin-top: 0.05rem;
        margin-bottom: 0.35rem;
        color: #f7f9fc;
        letter-spacing: -0.02em;
        line-height: 1.05;
    }

    .small-info {
        text-align: center;
        font-size: 1.08rem;
        color: #9aa7bd;
        margin-bottom: 0.35rem;
        font-weight: 800;
        line-height: 1;
    }

    .range-info {
        text-align: center;
        margin-bottom: 0.55rem;
    }

    .range-chip {
        display: inline-block;
        padding: 0.42rem 0.92rem;
        border-radius: 999px;
        background: rgba(126, 231, 240, 0.08);
        border: 1px solid rgba(126, 231, 240, 0.65);
        color: #8ef3fb !important;
        font-size: 1rem;
        font-weight: 900;
        margin: 0.14rem;
    }

    .section-label {
        text-align: center;
        font-size: 6vw !important;
        font-weight: 900;
        color: #f7f9fc;
        margin-top: 0.15rem;
        margin-bottom: 0.65rem;
        letter-spacing: -0.03em;
    }

    /* 4. 일반 버튼 기본 스타일 */
    .stButton > button {
        width: 100%;
        border-radius: 22px;
        min-height: 62px;
        font-size: 1.35rem !important;
        font-weight: 900;
        border: 1px solid rgba(255,255,255,0.12) !important;
        background: rgba(255,255,255,0.05) !important;
        color: #f7f9fc !important;
        backdrop-filter: blur(2px);
        transition: all 0.18s ease;
        box-shadow: none;
    }

    .stButton > button:hover {
        border: 1px solid rgba(126, 231, 240, 0.45) !important;
        background: rgba(255,255,255,0.08) !important;
        color: #ffffff !important;
    }

    /* 전체 페이지에서 쓰이는 Primary 버튼 스타일 */
    .stButton > button[kind="primary"] {
        background: rgba(126, 231, 240, 0.14) !important;
        border: 1.8px solid rgba(126, 231, 240, 0.82) !important;
        color: #bafcff !important;
        transform: scale(1.02);
    }

    .home-btn .stButton > button {
        min-height: 86px;
        font-size: 2rem !important;
        font-weight: 900;
        border-radius: 24px;
    }

    .grade-grid .stButton > button {
        min-height: 96px;
        font-size: 2rem !important;
        font-weight: 900;
        border-radius: 22px;
        margin-bottom: 0.25rem;
    }

    .range-group-btn .stButton > button {
        min-height: 92px;
        font-size: 3.6rem !important;
        font-weight: 900;
        border-radius: 24px;
    }

    .step-btn .stButton > button {
        min-height: 86px;
        font-size: 3.2rem !important;
        font-weight: 900;
        border-radius: 24px;
    }

    .back-btn .stButton > button,
    .complete-btn .stButton > button {
        min-height: 74px;
        font-size: 1.7rem !important;
        font-weight: 900;
        border-radius: 22px;
    }

    .mode-btn .stButton > button {
        min-height: 76px;
        font-size: 1.7rem !important;
        font-weight: 900;
    }

    .back-small-btn .stButton > button {
        min-height: 66px;
        font-size: 1.35rem !important;
        font-weight: 900;
        border-radius: 22px;
    }

    .exit-btn .stButton > button {
        min-height: 58px;
        font-size: 1.2rem !important;
        font-weight: 900;
        border-radius: 20px;
        background: rgba(255,255,255,0.03) !important;
        color: #f7f9fc !important;
        border: 1px solid rgba(255,255,255,0.16) !important;
    }

    /* 5. 대왕 한자 크기 (화면 너비에 따라 유동적으로 변하게 수정) */
    .hanja-card {
        background: transparent;
        border: none;
        min-height: 210px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 0.1rem;
        margin-bottom: 0.25rem;
    }

    .hanja-big {
        font-size: 28vw !important; /* 9.4rem -> 28vw 변경 */
        font-weight: 900;
        line-height: 1;
        color: #ffffff !important;
        letter-spacing: -0.04em;
        text-align: center;
        display: block;
        margin: 10px 0;
    }

    .question-big-hanja {
        font-size: 22vw !important; /* 8rem -> 22vw 변경 */
        font-weight: 900;
        line-height: 1;
        color: #ffffff !important;
        letter-spacing: -0.04em;
        text-align: center;
    }

    .question-big-text {
        font-size: 10vw !important; /* 3.7rem -> 10vw 변경 */
        font-weight: 900;
        line-height: 1.02;
        color: #f7f9fc !important;
        text-align: center;
        letter-spacing: -0.04em;
    }

    .quiz-type-btn .stButton > button {
        min-height: 64px;
        font-size: 1.22rem !important;
        font-weight: 900;
    }

    /* 하단 확인/다음 버튼 사이즈 조절 */
    .quiz-action-btn .stButton > button {
        height: 70px !important;
        border-radius: 20px !important;
        font-size: 1.8rem !important;
        font-weight: 900 !important;
    }

    .spacer-1 { height: 0.35rem; }
    .spacer-2 { height: 0.7rem; }
    .spacer-3 { height: 1.2rem; }
    .spacer-4 { height: 2rem; }
    
    /* 6. 모바일 웹 브라우저 상단바 등 방해 요소 제거 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 7. 아이폰 미니 등 아주 작은 폰을 위한 미세 조정 */
    @media (max-width: 380px) {
        .main-title { font-size: 11vw !important; }
        .stButton>button { min-height: 55px !important; font-size: 1.1rem !important; }
        .hanja-big { font-size: 32vw !important; }
        .question-big-hanja { font-size: 25vw !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# Constants
# =========================
GRADE_GROUPS = {
    "8급": ["A"],
    "7급": ["B"],
    "6급": ["C"],
    "준5급": ["C"],
    "5급": ["D", "E"],
    "준4급": ["F", "G"],
    "4급": ["H", "I"],
    "준3급": ["J", "K"],
    "3급": ["L", "M", "N", "O"],
}

GRADE_ORDER = ["8급", "준5급", "4급", "7급", "5급", "준3급", "6급", "준4급", "3급"]

STEP_NUMBERS = [1, 2, 3, 4, 5, 6]


# =========================
# Session state
# =========================
def init_state() -> None:
    defaults = {
        "page": "home",
        "selected_grade": None,
        "selected_group": None,
        "selected_steps": [],
        "selected_db": None,
        "study_label": None,
        "study_mode": None,
        "filtered_df": pd.DataFrame(),
        "memorize_index": 0,
        "memorize_cycle": 1,
        "memorize_show_answer": False,
        "quiz_type": "meaning_to_hanja",
        "quiz_sequence": [],     
        "quiz_index": 0,         
        "quiz_current_row": None, 
        "quiz_question": None,
        "quiz_options": [],
        "quiz_answer_index": None,
        "quiz_selected_index": None,
        "quiz_checked": False,
        "wrong_answers": [],     
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()


# =========================
# Data load
# =========================
def normalize_columns(df: pd.DataFrame, db_name: str) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    if db_name == "DB-1":
        rename_map = {
            "한자": "hanja",
            "뜻": "meaning",
            "독음": "sound",
            "급수": "grade",
            "단계": "step",
        }
    else:
        rename_map = {
            "한자": "hanja",
            "독음": "sound",
            "급수": "grade",
            "단계": "step",
        }

    df = df.rename(columns=rename_map)

    for col in ["hanja", "sound", "grade", "step"]:
        if col not in df.columns:
            df[col] = ""

    if "meaning" not in df.columns:
        df["meaning"] = ""

    for col in ["hanja", "meaning", "sound", "grade", "step"]:
        df[col] = df[col].fillna("").astype(str).str.strip()

    return df[["hanja", "meaning", "sound", "grade", "step"]]


@st.cache_data
def load_excel_data():
    candidates = [
        Path("hanja.xlsm"),
        Path("hanja.xlsx"),
        Path("./hanja.xlsm"),
        Path("./hanja.xlsx"),
    ]

    file_path = None
    for candidate in candidates:
        if candidate.exists():
            file_path = candidate
            break

    if file_path is None:
        return pd.DataFrame(), pd.DataFrame(), None

    xls = pd.ExcelFile(file_path)
    if "DB-1" not in xls.sheet_names or "DB-2" not in xls.sheet_names:
        raise ValueError("엑셀 파일에 DB-1, DB-2 시트가 모두 있어야 합니다.")

    db1 = pd.read_excel(file_path, sheet_name="DB-1")
    db2 = pd.read_excel(file_path, sheet_name="DB-2")

    db1 = normalize_columns(db1, "DB-1")
    db2 = normalize_columns(db2, "DB-2")
    return db1, db2, str(file_path)


def step_values_from_selection(group: str | None, steps: list[int]) -> list[str]:
    if not group:
        return []
    return [f"{group}-{step}" for step in sorted(steps)]


def get_filtered_df() -> pd.DataFrame:
    db1, db2, _ = load_excel_data()
    db_name = st.session_state.selected_db
    source_df = db1 if db_name == "DB-1" else db2

    if source_df.empty:
        return source_df

    grade = st.session_state.selected_grade
    group = st.session_state.selected_group
    steps = st.session_state.selected_steps
    selected_step_values = step_values_from_selection(group, steps)

    filtered = source_df.copy()
    if grade:
        filtered = filtered[filtered["grade"] == grade]
    if selected_step_values:
        filtered = filtered[filtered["step"].isin(selected_step_values)]

    return filtered.reset_index(drop=True)


# =========================
# Helpers
# =========================
def go_page(page_name: str) -> None:
    st.session_state.page = page_name
    st.rerun()


def render_range_info() -> None:
    chips = []

    if st.session_state.selected_grade:
        chips.append(f"급수 {st.session_state.selected_grade}")

    if st.session_state.selected_group and st.session_state.selected_steps:
        step_text = ", ".join(
            [f"{st.session_state.selected_group}-{s}" for s in sorted(st.session_state.selected_steps)]
        )
        chips.append(step_text)

    if chips:
        html = "".join([f"<span class='range-chip'>{chip}</span>" for chip in chips])
        st.markdown(f"<div class='range-info'>{html}</div>", unsafe_allow_html=True)


def set_study_mode(db_name: str, label: str, mode: str) -> None:
    st.session_state.selected_db = db_name
    st.session_state.study_label = label
    st.session_state.study_mode = mode
    st.session_state.filtered_df = get_filtered_df()
    
    st.session_state.memorize_index = 0
    st.session_state.memorize_cycle = 1 
    st.session_state.memorize_show_answer = False
    
    st.session_state.wrong_answers = []
    st.session_state.quiz_index = 0

    if st.session_state.filtered_df.empty:
        st.warning("선택한 범위에 데이터가 없습니다.")
        return

    if mode == "외우기":
        go_page("memorize")
    else:
        df_len = len(st.session_state.filtered_df)
        st.session_state.quiz_sequence = random.sample(range(df_len), df_len)
        build_new_quiz_question()
        go_page("quiz")


def build_option_label(row: pd.Series, quiz_type: str) -> str:
    meaning = str(row.get("meaning", "")).strip()
    sound = str(row.get("sound", "")).strip()
    hanja = str(row.get("hanja", "")).strip()

    if quiz_type == "meaning_to_hanja":
        return hanja

    if meaning and sound:
        return f"{meaning} ({sound})"
    if sound:
        return sound
    if meaning:
        return meaning
    return hanja


def build_new_quiz_question() -> None:
    df = st.session_state.filtered_df

    if df.empty or st.session_state.quiz_index >= len(st.session_state.quiz_sequence):
        st.session_state.quiz_question = None
        st.session_state.quiz_options = []
        st.session_state.quiz_answer_index = None
        st.session_state.quiz_selected_index = None
        st.session_state.quiz_checked = False
        return

    row_idx = st.session_state.quiz_sequence[st.session_state.quiz_index]
    row = df.iloc[row_idx]
    st.session_state.quiz_current_row = row.to_dict() 

    quiz_type = st.session_state.quiz_type

    if quiz_type == "meaning_to_hanja":
        if row["meaning"] and row["sound"]:
            question = f"{row['meaning']} ({row['sound']})"
        elif row["meaning"]:
            question = row["meaning"]
        else:
            question = row["sound"]

        correct_value = row["hanja"]
        pool_df = df[df["hanja"] != correct_value].copy()
        wrong_rows = pool_df.sample(n=min(3, len(pool_df)), replace=False) if len(pool_df) > 0 else pool_df
        options = [r["hanja"] for _, r in wrong_rows.iterrows()]
        options.append(correct_value)
    else:
        question = row["hanja"]
        correct_value = build_option_label(row, quiz_type)
        pool_df = df[df["hanja"] != row["hanja"]].copy()
        wrong_rows = pool_df.sample(n=min(3, len(pool_df)), replace=False) if len(pool_df) > 0 else pool_df
        options = [build_option_label(r, quiz_type) for _, r in wrong_rows.iterrows()]
        options.append(correct_value)

    options = list(dict.fromkeys(options))

    while len(options) < 4:
        filler = "-"
        if filler not in options:
            options.append(filler)
        else:
            break

    random.shuffle(options)
    answer_index = options.index(correct_value)

    st.session_state.quiz_question = question
    st.session_state.quiz_options = options
    st.session_state.quiz_answer_index = answer_index
    st.session_state.quiz_selected_index = None
    st.session_state.quiz_checked = False


# =========================
# Pages
# =========================
def page_home() -> None:
    st.markdown("<div class='main-title'>한자 공부</div>", unsafe_allow_html=True)
    st.markdown("<div class='spacer-4'></div>", unsafe_allow_html=True)
    st.markdown("<div class='spacer-4'></div>", unsafe_allow_html=True)
    st.markdown("<div class='spacer-4'></div>", unsafe_allow_html=True)

    left, center, right = st.columns([1.6, 2.4, 1.6])
    with center:
        st.markdown("<div class='home-btn'>", unsafe_allow_html=True)
        if st.button("시작", key="start_app", use_container_width=True):
            go_page("grade")
        st.markdown("</div>", unsafe_allow_html=True)


def page_grade() -> None:
    st.markdown("<div class='main-title'>급수 선택</div>", unsafe_allow_html=True)
    st.markdown("<div class='spacer-4'></div>", unsafe_allow_html=True)

    grade_cols = st.columns(3)

    for i, grade in enumerate(GRADE_ORDER):
        with grade_cols[i % 3]:
            st.markdown("<div class='grade-grid'>", unsafe_allow_html=True)
            if st.button(
                grade,
                key=f"grade_{grade}",
                use_container_width=True,
                type="primary" if st.session_state.selected_grade == grade else "secondary",
            ):
                st.session_state.selected_grade = grade
                st.session_state.selected_group = GRADE_GROUPS[grade][0]
                st.session_state.selected_steps = []
                go_page("range")
            st.markdown("</div>", unsafe_allow_html=True)

        if i in [2, 5]:
            st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)

    st.markdown("<div class='spacer-4'></div>", unsafe_allow_html=True)

    left, center, right = st.columns([2.3, 1.2, 2.3])
    with center:
        st.markdown("<div class='exit-btn'>", unsafe_allow_html=True)
        if st.button("나가기", key="grade_exit", use_container_width=True):
            go_page("home")
        st.markdown("</div>", unsafe_allow_html=True)


def page_range() -> None:
    grade = st.session_state.selected_grade
    if not grade:
        go_page("grade")
        return

    groups = GRADE_GROUPS[grade]

    st.markdown("<div class='main-title'>범위 선택</div>", unsafe_allow_html=True)
    render_range_info()
    st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)

    if len(groups) == 1:
        left, center, right = st.columns([1.8, 2.4, 1.8])
        with center:
            st.markdown("<div class='range-group-btn'>", unsafe_allow_html=True)
            if st.button(
                groups[0],
                key=f"range_group_{groups[0]}",
                use_container_width=True,
                type="primary" if st.session_state.selected_group == groups[0] else "secondary",
            ):
                st.session_state.selected_group = groups[0]
                st.session_state.selected_steps = []
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    elif len(groups) == 2:
        outer_left, col1, col2, outer_right = st.columns([0.7, 1.2, 1.2, 0.7])

        with col1:
            st.markdown("<div class='range-group-btn'>", unsafe_allow_html=True)
            if st.button(
                groups[0],
                key=f"range_group_{groups[0]}",
                use_container_width=True,
                type="primary" if st.session_state.selected_group == groups[0] else "secondary",
            ):
                st.session_state.selected_group = groups[0]
                st.session_state.selected_steps = []
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='range-group-btn'>", unsafe_allow_html=True)
            if st.button(
                groups[1],
                key=f"range_group_{groups[1]}",
                use_container_width=True,
                type="primary" if st.session_state.selected_group == groups[1] else "secondary",
            ):
                st.session_state.selected_group = groups[1]
                st.session_state.selected_steps = []
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        group_cols = st.columns(3)
        for idx, group in enumerate(groups):
            with group_cols[idx % 3]:
                st.markdown("<div class='range-group-btn'>", unsafe_allow_html=True)
                if st.button(
                    group,
                    key=f"range_group_{group}",
                    use_container_width=True,
                    type="primary" if st.session_state.selected_group == group else "secondary",
                ):
                    st.session_state.selected_group = group
                    st.session_state.selected_steps = []
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='spacer-3'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>단계 선택</div>", unsafe_allow_html=True)
    st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)

    outer_left, s1, s2, s3, outer_right = st.columns([0.35, 1, 1, 1, 0.35])
    step_columns = [s1, s2, s3]

    for i, step_num in enumerate(STEP_NUMBERS):
        with step_columns[i % 3]:
            selected = step_num in st.session_state.selected_steps
            st.markdown("<div class='step-btn'>", unsafe_allow_html=True)
            if st.button(
                f"{step_num}",
                key=f"range_step_{step_num}",
                use_container_width=True,
                type="primary" if selected else "secondary",
            ):
                if selected:
                    st.session_state.selected_steps.remove(step_num)
                else:
                    st.session_state.selected_steps.append(step_num)
                st.session_state.selected_steps = sorted(st.session_state.selected_steps)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        if i == 2:
            st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)

    st.markdown("<div class='spacer-3'></div>", unsafe_allow_html=True)

    left_pad, c1, c2, right_pad = st.columns([0.45, 1, 1, 0.45])

    with c1:
        st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
        if st.button("뒤로", key="page_range_back", use_container_width=True):
            go_page("grade")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='complete-btn'>", unsafe_allow_html=True)
        if st.button("선택 완료", key="page_range_done", use_container_width=True):
            if not st.session_state.selected_group or not st.session_state.selected_steps:
                st.warning("그룹과 단계를 선택해 주세요.")
            else:
                go_page("study_type")
        st.markdown("</div>", unsafe_allow_html=True)


def page_study_type() -> None:
    st.markdown("<div class='main-title'>공부 유형</div>", unsafe_allow_html=True)
    render_range_info()
    st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-label'>선정 한자</div>", unsafe_allow_html=True)
        st.markdown("<div class='mode-btn'>", unsafe_allow_html=True)
        if st.button("외우기", key="db1_memorize", use_container_width=True):
            set_study_mode("DB-1", "선정 한자", "외우기")
        if st.button("퀴즈", key="db1_quiz", use_container_width=True):
            set_study_mode("DB-1", "선정 한자", "퀴즈")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-label'>교과서 한자</div>", unsafe_allow_html=True)
        st.markdown("<div class='mode-btn'>", unsafe_allow_html=True)
        if st.button("외우기", key="db2_memorize", use_container_width=True):
            set_study_mode("DB-2", "교과서 한자", "외우기")
        if st.button("퀴즈", key="db2_quiz", use_container_width=True):
            set_study_mode("DB-2", "교과서 한자", "퀴즈")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)
    left, center, right = st.columns([2.4, 1.4, 2.4])
    with center:
        st.markdown("<div class='back-small-btn'>", unsafe_allow_html=True)
        if st.button("뒤로", key="study_type_back", use_container_width=True):
            go_page("range")
        st.markdown("</div>", unsafe_allow_html=True)


def page_memorize() -> None:
    st.markdown("""
    <style>
    /* 외우기 페이지의 거대 버튼 (모바일에 맞게 조정) */
    button[kind="primary"] {
        height: 35vh !important; /* 높이를 화면 비율로 조정 */
        min-height: 200px !important;
        border-radius: 40px !important;
        background: rgba(255,255,255,0.03) !important;
        border: 2px solid rgba(255,255,255,0.16) !important;
        transition: 0.3s;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        margin: 0 auto !important;
        width: 100% !important;
        box-shadow: none !important;
        transform: none !important;
    }
    
    button[kind="primary"]:hover {
        background: rgba(255,255,255,0.08) !important;
        border-color: rgba(126, 231, 240, 0.45) !important;
    }

    button[kind="primary"] p, button[kind="primary"] div, button[kind="primary"] span {
        font-size: 10vw !important; /* 글자 크기도 비율로 조정 */
        font-weight: 900 !important;
        color: #ffffff !important;
        line-height: 1.2 !important;
        white-space: normal !important;
        word-break: keep-all !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 좌우 화살표 버튼 크기 조절 */
    div[data-testid="column"]:nth-child(1) button[kind="primary"] p,
    div[data-testid="column"]:nth-child(1) button[kind="primary"] div,
    div[data-testid="column"]:nth-child(1) button[kind="primary"] span,
    div[data-testid="column"]:nth-child(3) button[kind="primary"] p,
    div[data-testid="column"]:nth-child(3) button[kind="primary"] div,
    div[data-testid="column"]:nth-child(3) button[kind="primary"] span {
        font-size: 15vw !important;
        line-height: 1 !important;
    }

    button[kind="primary"]:hover p, button[kind="primary"]:hover div, button[kind="primary"]:hover span {
        color: #00f2ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

    df = st.session_state.filtered_df
    if df.empty:
        st.warning("데이터가 없습니다.")
        if st.button("공부 유형으로 돌아가기", key="mem_return_empty"):
            go_page("study_type")
        return

    idx = max(0, min(st.session_state.memorize_index, len(df) - 1))
    st.session_state.memorize_index = idx
    row = df.iloc[idx]
    
    cycle = st.session_state.memorize_cycle

    st.markdown(f"<div class='main-title'>{st.session_state.study_label}</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>외우기</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-info'>{cycle}회독 &nbsp;•&nbsp; {idx + 1} / {len(df)}</div>", unsafe_allow_html=True)
    st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='hanja-card'><div class='hanja-big'>{row['hanja']}</div></div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)

    left, center, right = st.columns([1.0, 1.8, 1.0])

    with left:
        if st.button("◀", key="prev_memorize", type="primary", use_container_width=True):
            if st.session_state.memorize_index > 0:
                st.session_state.memorize_index -= 1
            else:
                st.session_state.memorize_index = len(df) - 1
            st.session_state.memorize_show_answer = False
            st.rerun()

    with center:
        if st.session_state.memorize_show_answer:
            if row["meaning"] and row["sound"]:
                reveal_text = f"{row['meaning']} {row['sound']}"
            elif row["sound"]:
                reveal_text = row["sound"]
            else:
                reveal_text = row["meaning"]

            if st.button(reveal_text, key="hide_answer", type="primary", use_container_width=True):
                pass
        else:
            if st.button("?", key="show_answer", type="primary", use_container_width=True):
                st.session_state.memorize_show_answer = True
                st.rerun()

    with right:
        if st.button("▶", key="next_memorize", type="primary", use_container_width=True):
            if st.session_state.memorize_index < len(df) - 1:
                st.session_state.memorize_index += 1
            else:
                st.session_state.memorize_index = 0
                st.session_state.memorize_cycle += 1
            st.session_state.memorize_show_answer = False
            st.rerun()

    st.markdown("<div class='spacer-3'></div>", unsafe_allow_html=True)

    left_exit, center_exit, right_exit = st.columns([2.5, 1.2, 2.5])
    with center_exit:
        st.markdown("<div class='exit-btn'>", unsafe_allow_html=True)
        if st.button("나가기", key="memorize_exit", use_container_width=True):
            go_page("study_type")
        st.markdown("</div>", unsafe_allow_html=True)


def page_quiz() -> None:
    df = st.session_state.filtered_df
    
    if not df.empty and st.session_state.quiz_index >= len(st.session_state.quiz_sequence):
        wrong_count = len(st.session_state.wrong_answers)
        correct_count = len(df) - wrong_count

        st.markdown(f"<div class='main-title'>{st.session_state.study_label}</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>학습 완료!</div>", unsafe_allow_html=True)
        st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style='height: 260px; min-height: 260px; border-radius: 40px; background: rgba(255,255,255,0.03); border: 2px solid rgba(255,255,255,0.16); display: flex; flex-direction: column; justify-content: center; align-items: center;'>
            <div style='font-size: 2.5rem; font-weight: 900; color: #ffffff; margin-bottom: 1rem;'>고생하셨습니다! 🎉</div>
            <div style='font-size: 1.5rem; font-weight: 800; color: #8ef3fb;'>총 {len(df)}문제 중 <span style='font-size:2rem; color:#00f2ff;'>{correct_count}</span>문제 정답</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='spacer-3'></div>", unsafe_allow_html=True)
        
        if wrong_count > 0:
            c1, c2 = st.columns(2, gap="small")
            with c1:
                st.markdown("<div class='quiz-action-btn'>", unsafe_allow_html=True)
                if st.button("🔥 오답 다시 외우기", key="review_wrong", use_container_width=True, type="primary"):
                    wrong_df = pd.DataFrame(st.session_state.wrong_answers).drop_duplicates(subset=['hanja'])
                    st.session_state.filtered_df = wrong_df.reset_index(drop=True)
                    st.session_state.memorize_index = 0
                    st.session_state.memorize_cycle = 1
                    st.session_state.memorize_show_answer = False
                    go_page("memorize")
                st.markdown("</div>", unsafe_allow_html=True)
            with c2:
                st.markdown("<div class='quiz-action-btn'>", unsafe_allow_html=True)
                if st.button("처음으로 나가기", key="exit_from_result", use_container_width=True):
                    go_page("study_type")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            left, center, right = st.columns([2.4, 1.3, 2.4])
            with center:
                st.markdown("<div class='exit-btn'>", unsafe_allow_html=True)
                if st.button("나가기", key="exit_perfect", use_container_width=True):
                    go_page("study_type")
                st.markdown("</div>", unsafe_allow_html=True)
        return

    if df.empty:
        st.warning("데이터가 없습니다.")
        if st.button("공부 유형으로 돌아가기", key="quiz_return_empty"):
            go_page("study_type")
        return

    st.markdown(f"<div class='main-title'>{st.session_state.study_label}</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>퀴즈</div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='small-info'>{st.session_state.quiz_index + 1} / {len(df)}</div>", unsafe_allow_html=True)

    t1, t2 = st.columns(2)
    with t1:
        st.markdown("<div class='quiz-type-btn'>", unsafe_allow_html=True)
        if st.button(
            "뜻(독음) → 한자",
            key="quiz_type_1",
            use_container_width=True,
            type="primary" if st.session_state.quiz_type == "meaning_to_hanja" else "secondary",
        ):
            st.session_state.quiz_type = "meaning_to_hanja"
            st.session_state.quiz_index = 0
            st.session_state.wrong_answers = []
            st.session_state.quiz_sequence = random.sample(range(len(df)), len(df))
            build_new_quiz_question()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with t2:
        st.markdown("<div class='quiz-type-btn'>", unsafe_allow_html=True)
        if st.button(
            "한자 → 음",
            key="quiz_type_2",
            use_container_width=True,
            type="primary" if st.session_state.quiz_type == "hanja_to_sound" else "secondary",
        ):
            st.session_state.quiz_type = "hanja_to_sound"
            st.session_state.quiz_index = 0
            st.session_state.wrong_answers = []
            st.session_state.quiz_sequence = random.sample(range(len(df)), len(df))
            build_new_quiz_question()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.quiz_question is None:
        build_new_quiz_question()

    question = st.session_state.quiz_question
    options = st.session_state.quiz_options
    answer_index = st.session_state.quiz_answer_index
    selected_index = st.session_state.quiz_selected_index
    checked = st.session_state.quiz_checked

    if question is None:
        st.info("문제를 만들 수 없습니다.")
        return

    st.markdown("<div class='spacer-1'></div>", unsafe_allow_html=True)

    q_class = 'question-big-hanja' if st.session_state.quiz_type == "hanja_to_sound" else 'question-big-text'
    
    # 퀴즈 질문 박스 높이도 화면 비율(vh)로 조정
    fixed_grid_style = "height: 20vh; min-height: 150px; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; width: 100%; box-sizing: border-box;"

    if not checked:
        question_html = f"""
        <div style='{fixed_grid_style}'>
            <div></div>
            <div class='{q_class}' style='margin:0; text-align:center;'>{question}</div>
            <div></div>
        </div>
        """
    else:
        is_correct = (selected_index == answer_index)
        correct_text = options[answer_index]
        
        if is_correct:
            question_html = f"""
            <div style='{fixed_grid_style}'>
                <div style='display: flex; justify-content: flex-end; padding-right: 1rem;'>
                    <div style='font-size: 6rem; font-weight: 900; color: #00f2ff; line-height: 1; text-shadow: 0 0 20px rgba(0,242,255,0.6); margin-top:-10px;'>O</div>
                </div>
                <div class='{q_class}' style='margin:0; text-align:center;'>{question}</div>
                <div></div>
            </div>
            """
        else:
            question_html = f"""
            <div style='{fixed_grid_style}'>
                <div style='display: flex; justify-content: flex-end; padding-right: 1rem;'>
                    <div style='font-size: 6rem; font-weight: 900; color: #ff4b4b; line-height: 1; text-shadow: 0 0 20px rgba(255,75,75,0.6); margin-top:-10px;'>X</div>
                </div>
                <div class='{q_class}' style='margin:0; text-align:center;'>{question}</div>
                <div style='display: flex; flex-direction: column; justify-content: center; text-align: left; padding-left: 1rem;'>
                    <span style='font-size: 1.2rem; font-weight: 800; color: #f7f9fc; line-height: 1.2; margin-bottom:0.2rem;'>정답은</span>
                    <span style='font-size: 2rem; font-weight: 900; color: #00f2ff; line-height: 1.1; text-shadow: 0 0 10px rgba(0,242,255,0.4);'>{correct_text}</span>
                </div>
            </div>
            """
            
    st.markdown(question_html, unsafe_allow_html=True)
    st.markdown("<div class='spacer-1'></div>", unsafe_allow_html=True)

    option_cols = st.columns(2, gap="small")
    
    for idx, option in enumerate(options):
        label = option
        
        if not checked:
            if selected_index == idx:
                bg_color = "rgba(0, 242, 255, 0.1) !important;"
                border = "2px solid #00f2ff !important;"
                text_color = "#00f2ff !important;"
            else:
                bg_color = "rgba(255,255,255,0.03) !important;"
                border = "2px solid rgba(255,255,255,0.16) !important;"
                text_color = "#ffffff !important;"
        else:
            if idx == answer_index:
                bg_color = "rgba(0, 242, 255, 0.15) !important;"
                border = "3px solid #00f2ff !important;"
                text_color = "#00f2ff !important;"
            else:
                bg_color = "rgba(255,255,255,0.01) !important;"
                border = "2px solid rgba(255,255,255,0.05) !important;"
                text_color = "rgba(255,255,255,0.2) !important;"

        marker_class = f"quiz-opt-marker-{idx}"
        css = f"""
        <style>
        div.element-container:has(.{marker_class}) + div.element-container button {{
            height: 12vh !important; /* 보기 버튼 높이도 비율로 조정 */
            min-height: 80px !important;
            border-radius: 20px !important;
            background: {bg_color}
            border: {border}
            transition: all 0.2s ease !important;
            box-shadow: none !important;
            transform: none !important;
        }}
        
        div.element-container:has(.{marker_class}) + div.element-container button p,
        div.element-container:has(.{marker_class}) + div.element-container button span,
        div.element-container:has(.{marker_class}) + div.element-container button div {{
            font-size: 7vw !important; /* 글자 크기 비율 조정 */
            font-weight: 900 !important;
            color: {text_color}
            line-height: 1.2 !important;
            white-space: normal !important;
            word-break: keep-all !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        
        div.element-container:has(.{marker_class}) + div.element-container button:hover {{
            background: rgba(255,255,255,0.08) !important;
            border-color: rgba(126, 231, 240, 0.45) !important;
        }}
        
        div.element-container:has(.{marker_class}) + div.element-container button:hover p,
        div.element-container:has(.{marker_class}) + div.element-container button:hover span,
        div.element-container:has(.{marker_class}) + div.element-container button:hover div {{
            color: #00f2ff !important;
        }}
        </style>
        <div class='{marker_class}' style='display:none;'></div>
        """

        with option_cols[idx % 2]:
            st.markdown(css, unsafe_allow_html=True)
            if st.button(label, key=f"quiz_option_{idx}", use_container_width=True):
                if not checked:
                    st.session_state.quiz_selected_index = idx
                    st.rerun()

    st.markdown("<div class='spacer-1'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="small")
    with c1:
        st.markdown("<div class='quiz-action-btn'>", unsafe_allow_html=True)
        if st.button("확인", key="quiz_confirm", use_container_width=True):
            if st.session_state.quiz_selected_index is None:
                st.warning("답을 선택해 주세요.")
            else:
                st.session_state.quiz_checked = True
                if st.session_state.quiz_selected_index != answer_index:
                    st.session_state.wrong_answers.append(st.session_state.quiz_current_row)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='quiz-action-btn'>", unsafe_allow_html=True)
        if st.button("▶", key="quiz_next", use_container_width=True):
            st.session_state.quiz_index += 1 
            build_new_quiz_question()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)
    
    left, center, right = st.columns([2.4, 1.3, 2.4])
    with center:
        st.markdown("<div class='exit-btn'>", unsafe_allow_html=True)
        if st.button("나가기", key="quiz_exit", use_container_width=True):
            go_page("study_type")
        st.markdown("</div>", unsafe_allow_html=True)


# =========================
# Data check
# =========================
try:
    db1, db2, excel_path = load_excel_data()
except Exception as exc:
    st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {exc}")
    st.info("hanja.xlsm 또는 hanja.xlsx 파일에 DB-1, DB-2 시트가 있어야 합니다.")
    st.stop()

if excel_path is None:
    st.warning("hanja.xlsm 또는 hanja.xlsx 파일을 찾지 못했습니다.")
    st.info("파이썬 파일과 같은 폴더에 엑셀 파일을 넣어 주세요.")
    st.stop()


# =========================
# Router
# =========================
page = st.session_state.page

if page == "home":
    page_home()
elif page == "grade":
    page_grade()
elif page == "range":
    page_range()
elif page == "study_type":
    page_study_type()
elif page == "memorize":
    page_memorize()
elif page == "quiz":
    page_quiz()
else:
    page_home()