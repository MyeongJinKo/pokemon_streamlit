import streamlit as st

print("page reloaded")
# page config 설정
st.set_page_config(
    page_title='포켓몬 도감',
    page_icon='./images/monsterball.png'
)

# 커스텀 CSS 스타일 정의
# st.markdown("""
# <h1 style='color:red;'>포켓몬 도감</h1>
# """, unsafe_allow_html=True)

st.markdown("""
<style>
img {
	max-height: 300px;
}
</style>
""", unsafe_allow_html=True)


st.title("Streamlit 포켓몬 도감")
st.markdown("**포켓몬**을 하나씩 추가해보세요")

# 포켓몬 타입 선택
type_emoji_dict = {
    "노말": "⚪",
    "격투": "✊",
    "비행": "🕊",
    "독": "☠️",
    "땅": "🌋",
    "바위": "🪨",
    "벌레": "🐛",
    "고스트": "👻",
    "강철": "🤖",
    "불꽃": "🔥",
    "물": "💧",
    "풀": "🍃",
    "전기": "⚡",
    "에스퍼": "🔮",
    "얼음": "❄️",
    "드래곤": "🐲",
    "악": "😈",
    "페어리": "🧚"
}

# 포켓몬 데이터
initial_pokemons = [
    {
        "name": "피카츄",
        "types": ["전기"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/pikachu.webp"
    },
    {
        "name": "누오",
        "types": ["물", "땅"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/nuo.webp",
    },
    {
        "name": "갸라도스",
        "types": ["물", "비행"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/garados.webp",
    },
    {
        "name": "개굴닌자",
        "types": ["물", "악"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/frogninja.webp"
    },
    {
        "name": "루카리오",
        "types": ["격투", "강철"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/lukario.webp"
    },
    {
        "name": "에이스번",
        "types": ["불꽃"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/acebun.webp"
    },
]

# 예시 포켓몬 데이터
example_pokemon = {
    "name": "알로라 디그다",
    "types": ["땅", "강철"],
    "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/alora_digda.webp"
}


# session_state에 pokemons가 없으면 초기 포켓몬 데이터로 설정
if "pokemons" not in st.session_state:
    st.session_state.pokemons = initial_pokemons

auto_complete = st.toggle("예시 데이터로 채우기")
print("page_reload, auto_complete", auto_complete)

# 데이터 추가하기
with st.form(key="form"):
    col1, col2 = st.columns(2)
    with col1:
        # 포켓몬 이름 지정
        name = st.text_input(
            label="포켓몬 이름",
            value=example_pokemon["name"] if auto_complete else ""
            )
    with col2:
        # 포켓몬 타입 지정 최대 2개 선택 가능
        types = st.multiselect(
            label="포켓몬 속성",
            options=list(type_emoji_dict.keys()),
            max_selections=2,
            default=example_pokemon["types"] if auto_complete else []
            )
    image_url = st.text_input(
        label="포켓몬 이미지 URL",
        value=example_pokemon["image_url"] if auto_complete else ""
        )
    submit = st.form_submit_button(label="Submit")
    if submit:
        if not name:
            st.error("포켓몬 이름을 입력해주세요.")
        elif len(types) == 0:
            st.error("포켓몬 타입을 적어도 한개 이상 선택해주세요.")
        else:
            st.success("포켓몬이 추가되었습니다!")
            st.session_state.pokemons.append({
                "name": name,
                "types": types,
                "image_url": image_url if image_url else "./images/default.png"
            })
        
for i in range(0, len(st.session_state.pokemons), 3):
    row_pokemons = st.session_state.pokemons[i:i+3]
    cols = st.columns(3)
    for j in range(len(row_pokemons)): # 빈 칸을 채우기 위해 빈 딕셔너리 추가
        with cols[j]:
            pokemon = row_pokemons[j]
            with st.expander(label=f"**{i+j+1}. {pokemon["name"]}**", expanded=True): # expander를 사용하여 포켓몬 정보 표시 
                st.image(pokemon["image_url"]) # 포켓몬 이미지 표시
                emoji_types = [f"{type_emoji_dict[x]} {x}" for x in pokemon["types"]] # 포켓몬 타입 이모지 표시
                type_html = f"<span style='font-size:16px;'>{' / '.join(emoji_types)}</span>"
                st.markdown(type_html, unsafe_allow_html=True)
                delete_button = st.button(label="삭제", key=i+j, use_container_width=True)
                if delete_button:
                    print("delete button clicked")
                    del st.session_state.pokemons[i+j]
                    st.rerun() # 페이지를 새로고침하여 삭제된 포켓몬을 반영
