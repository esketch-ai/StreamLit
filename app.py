# streamlit과 openai 라이브러리를 import합니다.
import streamlit as st
import openai

# openai API key를 입력합니다. 깃허브에 등록시에는 주석처리합니다.
openai.api_key = st.secrets["api_key"]

# streamlit 앱의 제목을 설정합니다.
st.title("Streamlit App")

# form을 생성합니다.
with st.form("promt_form"):
    # 사용자가 입력한 prompt를 받는 text_input을 생성합니다.
    user_promt_input = st.text_input("Prompt")
    # 이미지 사이즈를 선택하는 selectbox를 생성합니다.
    size = st.selectbox("Size",["512x512", "1024x1024", "1080x1080"])
    # form을 제출하는 버튼을 생성합니다.
    submit = st.form_submit_button("Gogogo")

# form이 제출되었고, 사용자가 prompt를 입력했다면
if submit and user_promt_input:
    # ChatGPT에 전달할 prompt를 생성합니다.
    gpt_promt = [{"role": "system", "content": "Imagine the detail appearance of the input, Response it shortly."}, {"role": "user", "content": user_promt_input}]
    
    # ChatGPT로부터 응답을 받을 때까지 대기합니다.
    with st.spinner("Waiting for ChatGPT..."):
        gpt_response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=gpt_promt)
    
    # ChatGPT의 응답에서 생성된 prompt를 추출합니다.
    promt = gpt_response["choices"][0]["message"]["content"]
    
    # Dall-E로 이미지를 생성할 때까지 대기합니다.
    with st.spinner("Wating for Dall-E"):
        dalle_response = openai.Image.create(prompt=promt, size=size)
    
    # 사용자가 입력한 prompt와 ChatGPT에서 생성된 prompt를 출력합니다.
    st.write(user_promt_input)
    st.write(promt)
    # Dall-E에서 생성된 이미지를 출력합니다.
    st.image(dalle_response["data"][0]["url"])
