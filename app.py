import streamlit as st
from PIL import Image
from together import Together
import os 

image = Image.open('image.png')
st.image(image)

st.title("Hungry AI")

client = Together(api_key= os.environ['API_KEY'])

role_info = """Background information: you are a food order agent, users can search for restaurants and through menu to place an order. 

There are three restaurants with different menus. The format includes menu items followed by a price and a delivery time

Restaurant name: McDonalds
Menu:
Hamburger BigMac: 150sek
Cheese Hamburger: 160sek
Bacon Hamburger: 180sek
Milkshake strawberry: 50sek
Sprite: 30sek

Delivery time: 30 minutes

Restaurant name: Sushiparadise
Menu:
Original sushi: 100sek
Coca Cola: 50sek

Delivery time: 20 minutes

Restaurant name: BurgerKing
Menu:
Hamburger with cheese: 160sek
Milkshake banana: 50sek
Coca cola: 30sek

Delivery time: 20 minutes

Please only answer using the information above and a short and concise matter."""
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "mistralai/Mixtral-8x7B-Instruct-v0.1"

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": role_info})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["content"] != role_info:
            st.markdown(message["content"])

if prompt := st.chat_input("What do you fancy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )
        response = st.write(stream.choices[0].message.content)
    st.session_state.messages.append({"role": "assistant", "content": stream.choices[0].message.content})