아, 죄송합니다! 제가 이전 답변에서 작성해 드린 코드는 **'스타일(CSS)' 부분만** 수정한 코드였습니다. 전체 코드를 다 보내드리지 않고 스타일 부분만 덜렁 보내드려서 혼란을 드렸네요. 😭

기존에 작성하셨던 **모든 기능(단어 불러오기, 화면 이동, 퀴즈 기능 등)은 그대로 살려두고**, 디자인(스타일) 부분만 아내분 휴대폰에서도 예쁘게 보이도록 수정한 **진짜 완전한 전체 코드**를 다시 보내드립니다.

이 코드를 복사해서 `hanja_study_app.py` 파일의 내용을 싹 지우고 붙여넣어 주세요!

```python
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
# Style (절대 깨지지 않는 안전한 스타일)
# =========================
st.markdown(
    """
    <style>
    /* 1. 다크모드 강제 고정 */
    .stApp {
        background-color: #0E1117 !important;
    }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3, span, div, label {
        color: #f7f9fc !important;
    }

    /* 2. 화면 여백 최적화 */
    .block-container {
        max-width: 600px !important; 
        padding-top: 2rem !important; 
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        margin: 0 auto;
    }

    /* 3. 제목 크기 (안전한 크기 제한 적용) */
    .app-title {
        text-align: center;
        font-size: clamp(1.8rem, 6vw, 2.5rem) !important; 
        font-weight: 900;
        margin-bottom: 1rem;
    }

    .main-title {
        text-align: center;
        font-size: clamp(2rem, 8vw, 3rem) !important;
        font-weight: 900;
        margin: 0.5rem 0;
    }

    .sub-title {
        text-align: center;
        font-size: clamp(1.2rem, 5vw, 1.8rem) !important;
        font-weight: 900;
        margin-bottom: 0.5rem;
        color: #f7f9fc;
    }

    .small-info {
        text-align: center;
        font-size: 1rem;
        color: #9aa7bd;
        margin-bottom: 0.5rem;
        font-weight: 800;
    }

    .range-info {
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .range-chip {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 999px;
        background: rgba(126, 231, 240, 0.08);
        border: 1px solid rgba(126, 231, 240, 0.65);
        color: #8ef3fb !important;
        font-size: 0.9rem;
        font-weight: 900;
        margin: 0.2rem;
    }

    .section-label {
        text-align: center;
        font-size: clamp(1.2rem, 5vw, 1.8rem) !important;
        font-weight: 900;
        margin-bottom: 0.5rem;
    }

    /* 4. 기본 버튼 스타일 */
    .stButton > button {
        width: 100%;
        border-radius: 15px;
        min-height: 60px;
        font-size: 1.2rem !important;
        font-weight: 900;
        border: 1px solid rgba(255,255,255,0.12) !important;
        background: rgba(255,255,255,0.05) !important;
        color: #f7f9fc !important;
    }

    .stButton > button:hover {
        border: 1px solid rgba(126, 231, 240, 0.45) !important;
        background: rgba(255,255,255,0.08) !important;
        color: #ffffff !important;
    }

    .stButton > button[kind="primary"] {
        background: rgba(126, 231, 240, 0.14) !important;
        border: 1.8px solid rgba(126, 231, 240, 0.82) !important;
        color: #bafcff !important;
    }

    /* 5. 대왕 한자 크기 (최소/최대 크기 제한을 두어 깨짐 방지) */
    .hanja-card {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 180px;
        margin: 1rem 0;
    }

    .hanja-big {
        font-size: clamp(5rem, 25vw, 9rem) !important; /* 너무 커지지 않게 제한 */
        font-weight: 900;
        line-height: 1;
        color: #ffffff !important;
        text-align: center;
    }

    .question-big-hanja {
        font-size: clamp(4rem, 20vw, 7rem) !important;
        font-weight: 900;
        line-height: 1;
        color: #ffffff !important;
        text-align: center;
    }

    .question-big-text {
        font-size: clamp(1.8rem, 8vw, 3.5rem) !important;
        font-weight: 900;
        line-height: 1.2;
        color: #f7f9fc !important;
        text-align: center;
        word-break: keep-all;
    }

    /* 하단 확인 버튼 */
    .quiz-action-btn .stButton > button {
        min-height: 60px !important;
        font-size: 1.3rem !important;
    }

    .spacer-1 { height: 0.5rem; }
    .spacer-2 { height: 1rem; }
    .spacer-3 { height: 1.5rem; }
    .spacer-4 { height: 2rem; }
    
    /* 상단바 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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

    left, center, right = st.columns([1, 2, 1])
    with center:
        if st.button("시작하기", key="start_app", use_container_width=True, type="primary"):
            go_page("grade")


def page_grade() -> None:
    st.markdown("<div class='main-title'>급수 선택</div>", unsafe_allow_html=True)
    st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)

    grade_cols = st.columns(3)
    for i, grade in enumerate(GRADE_ORDER):
        with grade_cols[i % 3]:
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

    st.markdown("<div class='spacer-4'></div>", unsafe_allow_html=True)
    left, center, right = st.columns([1, 1, 1])
    with center:
        if st.button("홈으로", key="grade_exit", use_container_width=True):
            go_page("home")


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
        _, center, _ = st.columns([1, 2, 1])
        with center:
            if st.button(groups[0], key=f"rg_{groups[0]}", use_container_width=True, type="primary"):
                st.session_state.selected_group = groups[0]
                st.session_state.selected_steps = []
                st.rerun()
    elif len(groups) == 2:
        c1, c2 = st.columns(2)
        with c1:
            if st.button(groups[0], key=f"rg_{groups[0]}", use_container_width=True, type="primary" if st.session_state.selected_group == groups[0] else "secondary"):
                st.session_state.selected_group = groups[0]
                st.session_state.selected_steps = []
                st.rerun()
        with c2:
            if st.button(groups[1], key=f"rg_{groups[1]}", use_container_width=True, type="primary" if st.session_state.selected_group == groups[1] else "secondary"):
                st.session_state.selected_group = groups[1]
                st.session_state.selected_steps = []
                st.rerun()
    else:
        g_cols = st.columns(3)
        for idx, group in enumerate(groups):
            with g_cols[idx % 3]:
                if st.button(group, key=f"rg_{group}", use_container_width=True, type="primary" if st.session_state.selected_group == group else "secondary"):
                    st.session_state.selected_group = group
                    st.session_state.selected_steps = []
                    st.rerun()

    st.markdown("<div class='spacer-3'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>단계 선택</div>", unsafe_allow_html=True)

    s_cols = st.columns(3)
    for i, step_num in enumerate(STEP_NUMBERS):
        with s_cols[i % 3]:
            selected = step_num in st.session_state.selected_steps
            if st.button(f"{step_num}단계", key=f"rs_{step_num}", use_container_width=True, type="primary" if selected else "secondary"):
                if selected:
                    st.session_state.selected_steps.remove(step_num)
                else:
                    st.session_state.selected_steps.append(step_num)
                st.session_state.selected_steps = sorted(st.session_state.selected_steps)
                st.rerun()

    st.markdown("<div class='spacer-3'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("뒤로", key="pr_back", use_container_width=True):
            go_page("grade")
    with c2:
        if st.button("선택 완료", key="pr_done", use_container_width=True, type="primary"):
            if not st.session_state.selected_group or not st.session_state.selected_steps:
                st.warning("그룹과 단계를 선택해 주세요.")
            else:
                go_page("study_type")


def page_study_type() -> None:
    st.markdown("<div class='main-title'>공부 유형</div>", unsafe_allow_html=True)
    render_range_info()
    st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-label'>선정 한자</div>", unsafe_allow_html=True)
        if st.button("외우기", key="db1_mem", use_container_width=True):
            set_study_mode("DB-1", "선정 한자", "외우기")
        if st.button("퀴즈", key="db1_quiz", use_container_width=True):
            set_study_mode("DB-1", "선정 한자", "퀴즈")

    with col2:
        st.markdown("<div class='section-label'>교과서 한자</div>", unsafe_allow_html=True)
        if st.button("외우기", key="db2_mem", use_container_width=True):
            set_study_mode("DB-2", "교과서 한자", "외우기")
        if st.button("퀴즈", key="db2_quiz", use_container_width=True):
            set_study_mode("DB-2", "교과서 한자", "퀴즈")

    st.markdown("<div class='spacer-3'></div>", unsafe_allow_html=True)
    _, center, _ = st.columns([1, 1, 1])
    with center:
        if st.button("뒤로", key="st_back", use_container_width=True):
            go_page("range")


def page_memorize() -> None:
    st.markdown("""
    <style>
    /* 외우기 페이지 중앙 대형 버튼 최적화 */
    button[kind="primary"] {
        height: auto !important;
        min-height: 200px !important;
        border-radius: 20px !important;
    }
    button[kind="primary"] p {
        font-size: clamp(2rem, 10vw, 4rem) !important;
        white-space: pre-wrap !important;
        line-height: 1.3 !important;
    }
    /* 좌우 화살표 버튼 크기 최적화 */
    div[data-testid="column"]:nth-child(1) button[kind="primary"] p,
    div[data-testid="column"]:nth-child(3) button[kind="primary"] p {
        font-size: clamp(1.5rem, 8vw, 3rem) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    df = st.session_state.filtered_df
    if df.empty:
        st.warning("데이터가 없습니다.")
        if st.button("돌아가기"): go_page("study_type")
        return

    idx = max(0, min(st.session_state.memorize_index, len(df) - 1))
    st.session_state.memorize_index = idx
    row = df.iloc[idx]
    
    st.markdown(f"<div class='main-title'>{st.session_state.study_label}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-info'>{st.session_state.memorize_cycle}회독 • {idx + 1} / {len(df)}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='hanja-card'><div class='hanja-big'>{row['hanja']}</div></div>", unsafe_allow_html=True)

    left, center, right = st.columns([1, 2, 1])
    with left:
        if st.button("◀", key="p_m", type="primary", use_container_width=True):
            st.session_state.memorize_index = len(df) - 1 if idx == 0 else idx - 1
            st.session_state.memorize_show_answer = False
            st.rerun()
    with center:
        if st.session_state.memorize_show_answer:
            ans = f"{row['meaning']} {row['sound']}".strip()
            if not ans: ans = row['meaning'] or row['sound']
            st.button(ans, key="h_a", type="primary", use_container_width=True)
        else:
            if st.button("정답 보기", key="s_a", type="primary", use_container_width=True):
                st.session_state.memorize_show_answer = True
                st.rerun()
    with right:
        if st.button("▶", key="n_m", type="primary", use_container_width=True):
            if idx < len(df) - 1:
                st.session_state.memorize_index += 1
            else:
                st.session_state.memorize_index = 0
                st.session_state.memorize_cycle += 1
            st.session_state.memorize_show_answer = False
            st.rerun()

    st.markdown("<div class='spacer-3'></div>", unsafe_allow_html=True)
    _, c_exit, _ = st.columns([1, 1, 1])
    with c_exit:
        if st.button("나가기", key="m_exit", use_container_width=True):
            go_page("study_type")


def page_quiz() -> None:
    df = st.session_state.filtered_df
    
    if not df.empty and st.session_state.quiz_index >= len(st.session_state.quiz_sequence):
        wrong_count = len(st.session_state.wrong_answers)
        st.markdown(f"<div class='main-title'>학습 완료!</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align:center; padding: 2rem; background: rgba(255,255,255,0.05); border-radius: 20px; margin: 1rem 0;'>
            <h2 style='color:white; margin-bottom:1rem;'>고생하셨습니다! 🎉</h2>
            <h3 style='color:#8ef3fb;'>총 {len(df)}문제 중 <span style='color:#00f2ff; font-size:1.5em;'>{len(df)-wrong_count}</span>문제 정답</h3>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if wrong_count > 0 and st.button("🔥 오답 외우기", use_container_width=True, type="primary"):
                st.session_state.filtered_df = pd.DataFrame(st.session_state.wrong_answers).drop_duplicates(subset=['hanja']).reset_index(drop=True)
                st.session_state.memorize_index = 0
                st.session_state.memorize_cycle = 1
                st.session_state.memorize_show_answer = False
                go_page("memorize")
        with c2:
            if st.button("처음으로", use_container_width=True): go_page("study_type")
        return

    if df.empty:
        st.warning("데이터가 없습니다.")
        if st.button("돌아가기"): go_page("study_type")
        return

    st.markdown(f"<div class='sub-title'>{st.session_state.study_label} 퀴즈</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-info'>{st.session_state.quiz_index + 1} / {len(df)}</div>", unsafe_allow_html=True)

    t1, t2 = st.columns(2)
    with t1:
        if st.button("뜻(독음) → 한자", use_container_width=True, type="primary" if st.session_state.quiz_type == "meaning_to_hanja" else "secondary"):
            st.session_state.quiz_type = "meaning_to_hanja"
            st.session_state.quiz_index = 0
            st.session_state.wrong_answers = []
            st.session_state.quiz_sequence = random.sample(range(len(df)), len(df))
            build_new_quiz_question()
            st.rerun()
    with t2:
        if st.button("한자 → 음", use_container_width=True, type="primary" if st.session_state.quiz_type == "hanja_to_sound" else "secondary"):
            st.session_state.quiz_type = "hanja_to_sound"
            st.session_state.quiz_index = 0
            st.session_state.wrong_answers = []
            st.session_state.quiz_sequence = random.sample(range(len(df)), len(df))
            build_new_quiz_question()
            st.rerun()

    if st.session_state.quiz_question is None: build_new_quiz_question()

    q = st.session_state.quiz_question
    opts = st.session_state.quiz_options
    ans_idx = st.session_state.quiz_answer_index
    sel_idx = st.session_state.quiz_selected_index
    chk = st.session_state.quiz_checked

    q_class = 'question-big-hanja' if st.session_state.quiz_type == "hanja_to_sound" else 'question-big-text'
    
    if not chk:
        st.markdown(f"<div style='min-height:120px; display:flex; align-items:center; justify-content:center;'><div class='{q_class}'>{q}</div></div>", unsafe_allow_html=True)
    else:
        is_corr = (sel_idx == ans_idx)
        mark = "<span style='color:#00f2ff; font-size:3rem;'>O</span>" if is_corr else "<span style='color:#ff4b4b; font-size:3rem;'>X</span>"
        ans_text = f"<br><span style='font-size:1.2rem; color:#8ef3fb;'>정답: {opts[ans_idx]}</span>" if not is_corr else ""
        st.markdown(f"<div style='min-height:120px; display:flex; flex-direction:column; align-items:center; justify-content:center;'><div style='position:absolute; right:10%;'>{mark}</div><div class='{q_class}'>{q}</div>{ans_text}</div>", unsafe_allow_html=True)

    st.markdown("<div class='spacer-1'></div>", unsafe_allow_html=True)

    o_cols = st.columns(2)
    for i, opt in enumerate(opts):
        bg = "rgba(255,255,255,0.05)"
        border = "1px solid rgba(255,255,255,0.2)"
        color = "#ffffff"
        
        if not chk and sel_idx == i:
            bg, border, color = "rgba(0,242,255,0.1)", "2px solid #00f2ff", "#00f2ff"
        elif chk:
            if i == ans_idx:
                bg, border, color = "rgba(0,242,255,0.2)", "3px solid #00f2ff", "#00f2ff"
            else:
                color = "rgba(255,255,255,0.3)"

        css = f"""
        <style>
        div.element-container:has(.opt-{i}) + div.element-container button {{
            min-height: 80px !important; height: auto !important; padding: 10px !important;
            background: {bg} !important; border: {border} !important; border-radius: 15px !important;
        }}
        div.element-container:has(.opt-{i}) + div.element-container button p {{
            font-size: 1.3rem !important; color: {color} !important; white-space: pre-wrap !important; word-break: keep-all !important;
        }}
        </style><div class='opt-{i}' style='display:none;'></div>
        """
        with o_cols[i % 2]:
            st.markdown(css, unsafe_allow_html=True)
            if st.button(opt, key=f"qo_{i}", use_container_width=True) and not chk:
                st.session_state.quiz_selected_index = i
                st.rerun()

    st.markdown("<div class='spacer-1'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("확인", key="q_chk", use_container_width=True, type="primary"):
            if sel_idx is not None:
                st.session_state.quiz_checked = True
                if sel_idx != ans_idx: st.session_state.wrong_answers.append(st.session_state.quiz_current_row)
                st.rerun()
    with c2:
        if st.button("다음 ▶", key="q_nxt", use_container_width=True):
            st.session_state.quiz_index += 1 
            build_new_quiz_question()
            st.rerun()

    st.markdown("<div class='spacer-2'></div>", unsafe_allow_html=True)
    _, c_exit, _ = st.columns([1, 1, 1])
    with c_exit:
        if st.button("나가기", key="q_exit", use_container_width=True): go_page("study_type")


# =========================
# Data check & Run
# =========================
try:
    db1, db2, excel_path = load_excel_data()
except Exception as exc:
    st.error(f"엑셀 오류: {exc}")
    st.stop()

if excel_path is None:
    st.warning("hanja.xlsm 파일을 찾을 수 없습니다.")
    st.stop()

page = st.session_state.page
if page == "home": page_home()
elif page == "grade": page_grade()
elif page == "range": page_range()
elif page == "study_type": page_study_type()
elif page == "memorize": page_memorize()
elif page == "quiz": page_quiz()
else: page_home()
```