USERS = {}

def signup(email, password):
    USERS[email] = password
    return True

def login(email, password):
    return USERS.get(email) == password

In Streamlit:

if login(email, password):
    st.session_state.user_id = email
