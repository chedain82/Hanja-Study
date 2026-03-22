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
# Global Style (Responsive)
# =========================
st.markdown(
    """
    <style>
    /* =========================
       0. 다크 모드 고정
    ========================= */
    .stApp {
        background-color: #0E1117 !important;
    }

    html, body,
    [data-testid="stWidgetLabel"],
    .stMarkdown, p, h1, h2, h3, h4, h5, h6,
    span, div, label {
        color: #FFFFFF !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* =========================
       1. 전체 레이아웃
    ========================= */
    .block-container {
        max-width: 760px;
        padding-top: clamp(6.8rem, 10vw, 9.4rem) !important;
        padding-bottom: clamp(2.2rem, 4vw, 3.6rem) !important;
        padding-left: clamp(0.95rem, 3vw, 1.2rem) !important;
        padding-right: clamp(0.95rem, 3vw, 1.2rem) !important;
    }

    /* =========================
       2. 타이틀 / 텍스트
    ========================= */
    .app-title {
        text-align: center;
        font-size: clamp(2.25rem, 6.3vw, 3rem);
        font-weight: 900;
        color: #f7f9fc !important;
        margin-top: clamp(-0.6rem, -1vw, -0.1rem);
        margin-bottom: clamp(2rem, 4vw, 2.9rem);
        letter-spacing: -0.04em;
        line-height: 1.06;
    }

    .main-title {
        text-align: center;
        font-size: clamp(2.7rem, 7.5vw, 3.45rem);
        font-weight: 900;
        margin-top: 0.15rem;
        margin-bottom: clamp(0.65rem, 2vw, 0.95rem);
        color: #f7f9fc !important;
        letter-spacing: -0.045em;
        line-height: 1.04;
    }

    .sub-title {
        text-align: center;
        font-size: clamp(1.7rem, 5vw, 2.15rem);
        font-weight: 900;
        margin-top: 0.1rem;
        margin-bottom: clamp(0.45rem, 1.8vw, 0.8rem);
        color: #f7f9fc !important;
        letter-spacing: -0.02em;
        line-height: 1.08;
    }

    .small-info {
        text-align: center;
        font-size: clamp(1rem, 3.2vw, 1.18rem);
        color: #9aa7bd !important;
        margin-bottom: clamp(0.35rem, 1.3vw, 0.6rem);
        font-weight: 800;
        line-height: 1.1;
    }

    .range-info {
        text-align: center;
        margin-bottom: clamp(0.75rem, 2vw, 1.15rem);
    }

    .range-chip {
        display: inline-block;
        padding: clamp(0.4rem, 1vw, 0.52rem) clamp(0.82rem, 2vw, 1.08rem);
        border-radius: 999px;
        background: rgba(126, 231, 240, 0.08);
        border: 1px solid rgba(126, 231, 240, 0.68);
        color: #8ef3fb !important;
        font-size: clamp(0.96rem, 2.8vw, 1.08rem);
        font-weight: 900;
        margin: 0.14rem;
        line-height: 1.1;
    }

    .section-label {
        text-align: center;
        font-size: clamp(1.8rem, 5.3vw, 2.2rem);
        font-weight: 900;
        color: #f7f9fc !important;
        margin-top: clamp(0.35rem, 1vw, 0.75rem);
        margin-bottom: clamp(0.8rem, 2.2vw, 1.2rem);
        letter-spacing: -0.03em;
        line-height: 1.08;
    }

    /* =========================
       3. 버튼 공통
    ========================= */
    .stButton > button {
        width: 100%;
        min-height: clamp(72px, 10vw, 86px);
        border-radius: clamp(20px, 3vw, 25px);
        font-size: clamp(1.28rem, 3.9vw, 1.7rem);
        font-weight: 900;
        border: 1px solid rgba(255,255,255,0.12) !important;
        background: rgba(255,255,255,0.05) !important;
        color: #f7f9fc !important;
        backdrop-filter: blur(2px);
        -webkit-backdrop-filter: blur(2px);
        transition: all 0.18s ease;
        box-shadow: none !important;
        padding-top: 0.2rem !important;
        padding-bottom: 0.2rem !important;
    }

    .stButton > button:hover {
        border: 1px solid rgba(126, 231, 240, 0.45) !important;
        background: rgba(255,255,255,0.08) !important;
        color: #ffffff !important;
    }

    .stButton > button:focus,
    .stButton > button:active {
        outline: none !important;
        box-shadow: none !important;
    }

    .stButton > button[kind="primary"] {
        background: rgba(126, 231, 240, 0.14) !important;
        border: 1.8px solid rgba(126, 231, 240, 0.82) !important;
        color: #bafcff !important;
        transform: scale(1.02);
    }

    /* =========================
       4. 화면별 버튼 크기
    ========================= */
    .home-btn .stButton > button {
        min-height: clamp(84px, 11vw, 102px);
        font-size: clamp(1.8rem, 5vw, 2.35rem);
        font-weight: 900;
        border-radius: clamp(22px, 3vw, 28px);
        margin-top: clamp(0.4rem, 1.5vw, 0.9rem);
    }

    .grade-grid .stButton > button {
        min-height: clamp(88px, 11vw, 108px);
        font-size: clamp(1.75rem, 4.8vw, 2.2rem);
        font-weight: 900;
        border-radius: clamp(22px, 3vw, 26px);
        margin-bottom: clamp(0.2rem, 1vw, 0.5rem);
    }

    .range-group-btn .stButton > button {
        min-height: clamp(84px, 11vw, 104px);
        font-size: clamp(2rem, 6.2vw, 3.35rem);
        font-weight: 900;
        border-radius: clamp(22px, 3vw, 26px);
    }

    .step-btn .stButton > button {
        min-height: clamp(80px, 10.5vw, 96px);
        font-size: clamp(1.7rem, 5vw, 2.55rem);
        font-weight: 900;
        border-radius: clamp(20px, 3vw, 24px);
    }

    .mode-btn .stButton > button {
        min-height: clamp(86px, 11vw, 104px);
        font-size: clamp(1.5rem, 4.4vw, 2rem);
        font-weight: 900;
        border-radius: clamp(22px, 3vw, 26px);
    }

    .back-btn .stButton > button,
    .complete-btn .stButton > button {
        min-height: clamp(78px, 10vw, 92px);
        font-size: clamp(1.45rem, 4.1vw, 2rem);
        font-weight: 900;
        border-radius: clamp(20px, 3vw, 24px);
    }

    .back-small-btn .stButton > button {
        min-height: clamp(70px, 9vw, 80px);
        font-size: clamp(1.25rem, 3.7vw, 1.6rem);
        font-weight: 900;
        border-radius: clamp(18px, 3vw, 22px);
    }

    .exit-btn .stButton > button {
        min-height: clamp(60px, 8vw, 68px);
        font-size: clamp(1.05rem, 3vw, 1.35rem);
        font-weight: 900;
        border-radius: clamp(16px, 3vw, 20px);
        background: rgba(255,255,255,0.03) !important;
        color: #f7f9fc !important;
        border: 1px solid rgba(255,255,255,0.16) !important;
    }

    .quiz-type-btn .stButton > button {
        min-height: clamp(68px, 9vw, 80px);
        font-size: clamp(1.12rem, 3.4vw, 1.42rem);
        font-weight: 900;
        border-radius: clamp(18px, 3vw, 22px);
    }

    .quiz-action-btn .stButton > button {
        height: clamp(76px, 10vw, 90px) !important;
        min-height: clamp(76px, 10vw, 90px) !important;
        border-radius: clamp(20px, 3vw, 24px) !important;
        font-size: clamp(1.55rem, 4.5vw, 2.05rem) !important;
        font-weight: 900 !important;
    }

    /* =========================
       5. 카드 / 큰 글자
    ========================= */
    .hanja-card {
        background: transparent;
        border: none;
        min-height: clamp(220px, 28vw, 280px);
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 0.15rem;
        margin-bottom: clamp(0.3rem, 1vw, 0.55rem);
    }

    .hanja-big {
        font-size: clamp(7rem, 17vw, 10.4rem);
        font-weight: 900;
        line-height: 0.95;
        color: #ffffff !important;
        letter-spacing: -0.04em;
    }

    .question-big-hanja {
        font-size: clamp(6.2rem, 15vw, 9rem);
        font-weight: 900;
        line-height: 0.95;
        color: #ffffff !important;
        letter-spacing: -0.04em;
        text-align: center;
    }

    .question-big-text {
        font-size: clamp(2.6rem, 8vw, 4.2rem);
        font-weight: 900;
        line-height: 1.05;
        color: #f7f9fc !important;
        text-align: center;
        letter-spacing: -0.04em;
        word-break: keep-all;
    }

    /* =========================
       6. 공통 간격
    ========================= */
    .spacer-1 { height: clamp(0.45rem, 1vw, 0.6rem); }
    .spacer-2 { height: clamp(0.8rem, 2vw, 1.1rem); }
    .spacer-3 { height: clamp(1.3rem, 3vw, 1.8rem); }
    .spacer-4 { height: clamp(2rem, 4vw, 2.8rem); }

    /* =========================
       7. 작은 휴대폰 보정
    ========================= */
    @media (max-width: 430px) {
        .block-container {
            padding-top: clamp(7.3rem, 12vw, 9.6rem) !important;
            padding-left: 0.95rem !important;
            padding-right: 0.95rem !important;
        }

        .main-title {
            margin-bottom: 0.85rem;
        }

        .section-label {
            margin-bottom: 1rem;
        }

        .mode-btn .stButton > button {
            min-height: clamp(88px, 12vw, 102px);
            font-size: clamp(1.55rem, 4.8vw, 1.95rem);
        }

        .home-btn .stButton > button {
            min-height: clamp(88px, 12vw, 102px);
        }
    }

    /* =========================
       8. 큰 휴대폰/태블릿 보정
    ========================= */
    @media (min-width: 768px) {
        .block-container {
            padding-top: clamp(5.8rem, 7vw, 7.4rem) !important;
            max-width: 820px;
        }

        .stButton > button {
            min-height: clamp(68px, 7vw, 82px);
        }

        .mode-btn .stButton > button {
            min-height: clamp(78px, 8vw, 92px);
            font-size: clamp(1.4rem, 2.6vw, 1.8rem);
        }

        .range-group-btn .stButton > button {
            font-size: clamp(1.9rem, 4vw, 2.7rem);
        }

        .step-btn .stButton > button {
            font-size: clamp(1.5rem, 3vw, 2rem);
        }
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
    st.markdown(
        """
        <style>
        /* 외우기 페이지의 좌/중앙/우 거대 버튼 반응형 */
        button[kind="primary"] {
            height: clamp(190px, 28vw, 260px) !important;
            min-height: clamp(190px, 28vw, 260px) !important;
            border-radius: clamp(26px, 5vw, 40px) !important;
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

        button[kind="primary"] p,
        button[kind="primary"] div,
        button[kind="primary"] span {
            font-size: clamp(4rem, 10vw, 6.5rem) !important;
            font-weight: 900 !important;
            color: #ffffff !important;
            line-height: 1.15 !important;
            white-space: normal !important;
            word-break: keep-all !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        div[data-testid="column"]:nth-child(1) button[kind="primary"] p,
        div[data-testid="column"]:nth-child(1) button[kind="primary"] div,
        div[data-testid="column"]:nth-child(1) button[kind="primary"] span,
        div[data-testid="column"]:nth-child(3) button[kind="primary"] p,
        div[data-testid="column"]:nth-child(3) button[kind="primary"] div,
        div[data-testid="column"]:nth-child(3) button[kind="primary"] span {
            font-size: clamp(4.8rem, 12vw, 8rem) !important;
            line-height: 1 !important;
        }

        button[kind="primary"]:hover p,
        button[kind="primary"]:hover div,
        button[kind="primary"]:hover span {
            color: #00f2ff !important;
        }

        @media (min-width: 768px) {
            button[kind="primary"] {
                height: clamp(210px, 24vw, 250px) !important;
                min-height: clamp(210px, 24vw, 250px) !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

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

        st.markdown(
            f"""
            <div style="
                min-height: clamp(220px, 28vw, 260px);
                border-radius: clamp(26px, 5vw, 40px);
                background: rgba(255,255,255,0.03);
                border: 2px solid rgba(255,255,255,0.16);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 1.2rem;
                text-align: center;
            ">
                <div style="
                    font-size: clamp(2rem, 6vw, 3rem);
                    font-weight: 900;
                    color: #ffffff;
                    margin-bottom: 1rem;
                    line-height: 1.1;
                ">고생하셨습니다! 🎉</div>
                <div style="
                    font-size: clamp(1.35rem, 4vw, 2rem);
                    font-weight: 800;
                    color: #8ef3fb;
                    line-height: 1.25;
                ">
                    총 {len(df)}문제 중
                    <span style="font-size: clamp(1.9rem, 5vw, 2.5rem); color:#00f2ff;">{correct_count}</span>문제 정답
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='spacer-3'></div>", unsafe_allow_html=True)

        if wrong_count > 0:
            c1, c2 = st.columns(2, gap="small")
            with c1:
                st.markdown("<div class='quiz-action-btn'>", unsafe_allow_html=True)
                if st.button("🔥 오답만 다시 외우기", key="review_wrong", use_container_width=True, type="primary"):
                    wrong_df = pd.DataFrame(st.session_state.wrong_answers).drop_duplicates(subset=["hanja"])
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

    q_class = "question-big-hanja" if st.session_state.quiz_type == "hanja_to_sound" else "question-big-text"

    fixed_grid_style = """
        min-height: clamp(200px, 25vw, 260px);
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
    """

    if not checked:
        question_html = f"""
        <div style="{fixed_grid_style}">
            <div></div>
            <div class="{q_class}" style="margin:0; text-align:center;">{question}</div>
            <div></div>
        </div>
        """
    else:
        is_correct = selected_index == answer_index
        correct_text = options[answer_index]

        if is_correct:
            question_html = f"""
            <div style="{fixed_grid_style}">
                <div style="display: flex; justify-content: flex-end; padding-right: clamp(0.8rem, 3vw, 2rem);">
                    <div style="
                        font-size: clamp(4.5rem, 12vw, 8rem);
                        font-weight: 900;
                        color: #00f2ff;
                        line-height: 1;
                        text-shadow: 0 0 20px rgba(0,242,255,0.6);
                        margin-top:-10px;
                    ">O</div>
                </div>
                <div class="{q_class}" style="margin:0; text-align:center;">{question}</div>
                <div></div>
            </div>
            """
        else:
            question_html = f"""
            <div style="{fixed_grid_style}">
                <div style="display: flex; justify-content: flex-end; padding-right: clamp(0.8rem, 3vw, 2rem);">
                    <div style="
                        font-size: clamp(4.5rem, 12vw, 8rem);
                        font-weight: 900;
                        color: #ff4b4b;
                        line-height: 1;
                        text-shadow: 0 0 20px rgba(255,75,75,0.6);
                        margin-top:-10px;
                    ">X</div>
                </div>
                <div class="{q_class}" style="margin:0; text-align:center;">{question}</div>
                <div style="
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    text-align: left;
                    padding-left: clamp(0.8rem, 3vw, 2rem);
                ">
                    <span style="
                        font-size: clamp(1rem, 3vw, 1.6rem);
                        font-weight: 800;
                        color: #f7f9fc;
                        line-height: 1.2;
                        margin-bottom:0.5rem;
                    ">정답은</span>
                    <span style="
                        font-size: clamp(1.8rem, 5vw, 3.2rem);
                        font-weight: 900;
                        color: #00f2ff;
                        line-height: 1.1;
                        text-shadow: 0 0 10px rgba(0,242,255,0.4);
                    ">{correct_text}</span>
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
            min-height: clamp(96px, 16vw, 120px) !important;
            height: clamp(96px, 16vw, 120px) !important;
            border-radius: clamp(18px, 4vw, 24px) !important;
            background: {bg_color}
            border: {border}
            transition: all 0.2s ease !important;
            box-shadow: none !important;
            transform: none !important;
        }}

        div.element-container:has(.{marker_class}) + div.element-container button p,
        div.element-container:has(.{marker_class}) + div.element-container button span,
        div.element-container:has(.{marker_class}) + div.element-container button div {{
            font-size: clamp(1.7rem, 5vw, 4rem) !important;
            font-weight: 900 !important;
            color: {text_color}
            line-height: 1.15 !important;
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
        <div class="{marker_class}" style="display:none;"></div>
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