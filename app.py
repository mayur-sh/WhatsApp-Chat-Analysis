import streamlit as st
import plotly.express as px
from utils import *

st.set_option('deprecation.showPyplotGlobalUse', False)

# Interface Building

st.set_page_config(page_title='WhatsApp Chat Analysis', page_icon='💬', layout="wide", initial_sidebar_state="auto", menu_items=None)


###################################################### Aesthetics ######################################################################
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center;'><font face='High Tower Text'>WhatsApp Chat Analysis</font></h1>", unsafe_allow_html=True)
st.header("", divider='rainbow')
st.markdown("<p style='text-align: right; color: #ffd11a;'><font face='Brush Script MT' weight=5 size=5>-By Mayur Shrotriya</font></p>", unsafe_allow_html=True)

st.markdown("***")

with st.sidebar:
    txt_file = st.file_uploader(
        "Upload your Extracted Whatsapp txt file.", 
        type=['txt'], 
        # on_change=analyse
    )

    # st.markdown("***")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("""<p style="text-align:center;">Connect with me!<p>""", unsafe_allow_html=True)
    st.markdown("""
<html>
	<head>
		<style>
            body {
                margin: 0;
                display: flex;
                flex-wrap: wrap;
                justify-content: space-evenly;
                align-items: center;
                background-color: #16121200;
            }
            img{
                transition: transform 0.3s ease-in-out;
            }
            img:hover{
                transform: scale(1.1);
            }
        </style>
	</head>
    <body>
        <div style="display: flex;align-items: center;justify-content: center;text-align: center;align-content: center;">
            <a href="https://wa.me/919284999269" target="_blank">
                <img src="https://drive.google.com/thumbnail?id=1mdwT4obMTmtvHawcAs5ig4vlQ2-oxYzo" alt="whatsapp-icon" width="50%" height="auto">
            </a>
            <a href="https://www.linkedin.com/in/mayur-sh/" target="_blank">
                <img src="https://drive.google.com/thumbnail?id=13toM3454K63dYgyPH03nLUPYL0262tFC" alt="linkedin-icon" width="50%" height="auto">
            </a>
            <a href="https://github.com/mayur-sh" target="_blank">
                <img src="https://drive.google.com/thumbnail?id=1aSXwuGN4ZFwp3gwWtZTFh-fINlOmnII-" alt="github-icon" width="50%" height="auto">
            </a>
            <a href="mailto:mayurvs1998@gmail.com" target="_blank">
                <img src="https://drive.google.com/thumbnail?id=1ahdRXF4DXwBDAHXMdK1LiL6YKkVBiw0J" alt="gmail-icon" width="50%" height="auto">
            </a>
            <a href="https://sites.google.com/view/mayur-sh" target="_blank">
                <img src="https://drive.google.com/thumbnail?id=1KnyiOSU0x_aNrOy84py53e_AE_sFpDHw" alt="personal-portfolio-icon" width="50%" height="auto">
            </a>
        </div>
    </body>
</html>
""", unsafe_allow_html=True
)


if not txt_file:
    st.markdown("""<h4 style="text-align:center;">👈 Upload the exported WhatsApp text file in the sidebar.</h4>""", unsafe_allow_html=True)

else:
    content = txt_file.read().decode("utf-8")
    chat = [ re.sub('[(\u202f)|(\n)]', ' ', p).strip() for p in re.split( '(\\n\d\d/\d\d/\d\d,\s\d?\d:\d\d\\u202f[ap]m - [\w\s]{1,}:.*)', content ) if p != '']

    data = []
    messageBuffer = []
    date, time, author = None, None, None
    for line in chat:
        # while True:
        # line = fp.readline()
        if not line:
            break
        # line = line.strip()
        if date_time(line):
            if len(messageBuffer) > 0:
                data.append([date, time, author, ' '.join(messageBuffer)])
            messageBuffer.clear()
            date, time, author, message = getDatapoint(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)

    # Get the Dataframe
    df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
    df['Date'] = pd.to_datetime(df['Date'])

    c1, c2 = st.columns(2)
    total_messages = df.shape[0]
    c1.markdown(f"""<h3 style="text-align:center;">Total Messages: {df.shape[0]}</h3>""", unsafe_allow_html=True)

    users = [ u for u in df['Author'].unique() if u != None]
    c2.markdown(f"""<h3 style="text-align:center;">Users in chats: {', '.join(users)}</h3>""", unsafe_allow_html=True)

    st.markdown("***", unsafe_allow_html=True )

    media_messages = df[df["Message"]=='<Media omitted>'].shape[0]
    df['emoji'] = df["Message"].apply(split_count)
    URLPATTERN = r'(https?://\S+)'
    df['urlcount'] = df.Message.apply(lambda x: re.findall(URLPATTERN, x)).str.len()
    links = np.sum(df.urlcount)


    media_messages_df = df[df['Message'] == '<Media omitted>']
    messages_df = df.drop(media_messages_df.index)
    messages_df['Letter_Count'] = messages_df['Message'].apply(lambda s : len(s))
    messages_df['Word_Count'] = messages_df['Message'].apply(lambda s : len(s.split(' ')))
    messages_df["MessageCount"]=1

    _, c1, _, c2, _ = st.columns([1,3,2,3,1])

    # Filtering out messages of particular user
    req_df= messages_df[messages_df["Author"] == users[0]]
    # req_df will contain messages of only one particular user
    c1.write(f'Stats for {users[0]}: ')
    # req_df will contain messages of only one particular user
    c2.write(f'Stats for {users[1]}: ')

    _, c1, _, c2, _ = st.columns([2,3,3,3,1])

    # shape will print number of rows which indirectly means the number of messages
    c1.write('Messages Sent: '+ str(req_df.shape[0]))
    #Word_Count contains of total words in one message. Sum of all words/ Total Messages will yield words per message
    words_per_message = (np.sum(req_df['Word_Count']))/req_df.shape[0]
    c1.write('Average Words per message: '+ str(round(words_per_message, 2)))
    #media conists of media messages
    media = media_messages_df[media_messages_df['Author'] == users[0]].shape[0]
    c1.write('Media Messages Sent: '+ str(media))
    # emojis conists of total emojis
    emojis = sum(req_df['emoji'].str.len())
    c1.write('Emojis Sent: '+ str(emojis))
    #links consist of total links
    links = sum(req_df["urlcount"])
    c1.write('Links Sent: '+ str(links))

    # Filtering out messages of particular user
    req_df= messages_df[messages_df["Author"] == users[1]]
    # shape will print number of rows which indirectly means the number of messages
    c2.write('Messages Sent: '+ str(req_df.shape[0]))
    #Word_Count contains of total words in one message. Sum of all words/ Total Messages will yield words per message
    words_per_message = (np.sum(req_df['Word_Count']))/req_df.shape[0]
    c2.write('Average Words per message: '+ str(round(words_per_message, 2)))
    #media conists of media messages
    media = media_messages_df[media_messages_df['Author'] == users[1]].shape[0]
    c2.write('Media Messages Sent: '+ str(media))
    # emojis conists of total emojis
    emojis = sum(req_df['emoji'].str.len())
    c2.write('Emojis Sent: '+ str(emojis))
    #links consist of total links
    links = sum(req_df["urlcount"])
    c2.write('Links Sent: '+ str(links))

    total_emojis_list = list(set([a for b in messages_df.emoji for a in b]))
    total_emojis = len(total_emojis_list)

    total_emojis_list = list([a for b in messages_df.emoji for a in b])
    emoji_dict = dict(Counter(total_emojis_list))
    emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    # for i in emoji_dict:
    #   print(i)

    emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
    # fig = px.pie(emoji_df, values='count', names='emoji')
    # fig.update_traces(textposition='inside', textinfo='percent+label')
    # st.plotly_chart(fig, use_container_width=True)

    st.markdown("***")


    st.markdown("<h3>WordClouds</h3>", unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(['All Messages', f"{users[0]}'s Messages", f"{users[1]}'s Messages" ])

    with t1:
        st.write("")
        st.write("")
        st.write("")

        text = " ".join(review for review in messages_df.Message)
        # st.header(f"Wordcloud for all messages:")
        stopwords = set(STOPWORDS)
        # Generate a word cloud image
        wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
        # Display the generated image:
        # the matplotlib way:
        plt.figure( figsize=(10,5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    with t2:
        st.write("")
        st.write("")
        st.write("")

        dummy_df = messages_df[messages_df['Author'] == users[0]]
        text = " ".join(review for review in dummy_df.Message)
        stopwords = set(STOPWORDS)
        #Generate a word cloud image
        # st.header(f'Wordcloud for {users[0]}')
        wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
        #Display the generated image
        plt.figure( figsize=(10,5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    with t3:
        st.write("")
        st.write("")
        st.write("")

        dummy_df = messages_df[messages_df['Author'] == users[1]]
        text = " ".join(review for review in dummy_df.Message)
        stopwords = set(STOPWORDS)
        #Generate a word cloud image
        # st.header(f'Wordcloud for {users[1]}')
        wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
        #Display the generated image
        plt.figure( figsize=(10,5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    