<html>
<head>
<title>main.py</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type="text/css">
.s0 { color: #629755; font-style: italic;}
.s1 { color: #a9b7c6;}
.s2 { color: #cc7832;}
.s3 { color: #808080;}
.s4 { color: #6a8759;}
.s5 { color: #6897bb;}
</style>
</head>
<body bgcolor="#2b2b2b">
<table CELLSPACING=0 CELLPADDING=5 COLS=1 WIDTH="100%" BGCOLOR="#606060" >
<tr><td><center>
<font face="Arial, Helvetica" color="#000000">
main.py</font>
</center></td></tr></table>
<pre><span class="s0">'''import streamlit as st  # Import Streamlit first to allow page config 
import pandas as pd 
import json 
import os 
import re 
from transformers import RobertaTokenizer, RobertaForSequenceClassification 
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification 
import torch 
from bart_model import generate_summary  # Import the BART summary generator 
 
# Page Configuration (MUST be first Streamlit command) 
st.set_page_config( 
    page_title=&quot;Amazon GPT Login&quot;, 
    page_icon=&quot;🛒&quot;, 
    layout=&quot;wide&quot;, 
) 
 
# Load the dataset 
products_df = pd.read_csv(&quot;amazon.csv&quot;)  # Replace with your dataset 
products_df.dropna(inplace=True)  # Remove rows with missing data 
 
# File to store user data 
USER_DATA_FILE = &quot;user_data.json&quot; 
 
# Load or initialize user data 
if not os.path.exists(USER_DATA_FILE): 
    with open(USER_DATA_FILE, &quot;w&quot;) as f: 
        json.dump({}, f) 
 
with open(USER_DATA_FILE, &quot;r&quot;) as f: 
    user_data = json.load(f) 
 
def save_user_data(): 
    &quot;&quot;&quot;Save user data back to the file.&quot;&quot;&quot; 
    with open(USER_DATA_FILE, &quot;w&quot;) as f: 
        json.dump(user_data, f, indent=4) 
 
def validate_name(name): 
    return bool(re.match(&quot;^[A-Za-z ]+$&quot;, name)) 
 
def validate_email(email): 
    return bool(re.match(r&quot;^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$&quot;, email)) 
 
def validate_phone(phone): 
    return phone.isdigit() and 10 &lt;= len(phone) &lt;= 15 
 
# Check if user is logged in 
if &quot;logged_in_user&quot; not in st.session_state: 
    st.session_state.logged_in_user = None 
 
# Login Page Design 
if not st.session_state.logged_in_user: 
    # Layout for Login Page 
    col1, col2 = st.columns([1, 2]) 
 
    # Left Side - Login Form 
    with col1: 
        st.markdown( 
            &quot;&quot;&quot; 
            &lt;div style='display: flex; justify-content: center;'&gt; 
                &lt;img src='https://upload.wikimedia.org/wikipedia/commons/d/de/Amazon_icon.png' width='100'/&gt; 
            &lt;/div&gt; 
            &quot;&quot;&quot;, 
            unsafe_allow_html=True 
        ) 
        st.markdown(&quot;&lt;h1 style='color: #FF9900; text-align: center;'&gt;Amazon GPT Login&lt;/h1&gt;&quot;, unsafe_allow_html=True) 
 
        with st.form(&quot;login_form&quot;): 
            name = st.text_input(&quot;Full Name:&quot;) 
            email = st.text_input(&quot;Email Address:&quot;) 
            phone = st.text_input(&quot;Phone Number:&quot;) 
 
            submitted = st.form_submit_button(&quot;Login&quot;) 
            if submitted: 
                errors = [] 
                if not validate_name(name): 
                    errors.append(&quot;Invalid Name: Only letters and spaces are allowed.&quot;) 
                if not validate_email(email): 
                    errors.append(&quot;Invalid Email: Enter a valid email address.&quot;) 
                if not validate_phone(phone): 
                    errors.append(&quot;Invalid Phone: Must be 10-15 digits.&quot;) 
 
                if errors: 
                    st.error(&quot; &quot;.join(errors)) 
                else: 
                    if email not in user_data: 
                        user_data[email] = {&quot;name&quot;: name, &quot;phone&quot;: phone, &quot;search_history&quot;: []} 
                        save_user_data() 
 
                    st.session_state.logged_in_user = email 
                    st.success(f&quot;Welcome, {name}!&quot;) 
 
    # Right Side - Yellow Background 
    with col2: 
        st.markdown( 
            &quot;&quot;&quot; 
            &lt;div style='background-color: #FF9900; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center;'&gt; 
                &lt;h1 style='color: black; text-align: center; font-size: 50px;'&gt;AMAZON PRODUCT RESEARCH&lt;/h1&gt; 
                &lt;h2 style='color: black; text-align: center; font-size: 30px;'&gt;MERRY CHRISTMAS 🎄&lt;/h2&gt; 
            &lt;/div&gt; 
            &quot;&quot;&quot;, 
            unsafe_allow_html=True, 
        ) 
 
else: 
    # Main Interface 
    current_user_email = st.session_state.logged_in_user 
    current_user = user_data[current_user_email] 
 
    # Sidebar - Model Selection and History 
    st.sidebar.title(&quot;Options&quot;) 
    st.sidebar.subheader(&quot;Select Model&quot;) 
    model_options = [&quot;BART&quot;, &quot;RoBERTa&quot;, &quot;DistilBERT&quot;] 
    selected_model = st.sidebar.radio(&quot;Choose a model:&quot;, model_options) 
 
    st.sidebar.subheader(&quot;Search History&quot;) 
    if current_user[&quot;search_history&quot;]: 
        st.sidebar.markdown( 
            &quot;\n&quot;.join([f&quot;- {item}&quot; for item in current_user[&quot;search_history&quot;]]) 
        ) 
    else: 
        st.sidebar.write(&quot;No search history yet.&quot;) 
 
    # Main Header 
    st.markdown(&quot;&lt;h1 style='text-align: center;'&gt;Amazon Product Research&lt;/h1&gt;&quot;, unsafe_allow_html=True) 
 
    logout = st.button(&quot;Logout&quot;, key=&quot;logout_button&quot;, help=&quot;Logout&quot;) 
    if logout: 
        st.session_state.logged_in_user = None 
 
    st.markdown(f&quot;&lt;h3 style='text-align: center;'&gt;Welcome, {current_user['name']}&lt;/h3&gt;&quot;, unsafe_allow_html=True) 
    query = st.text_input(&quot;Search for a product:&quot;) 
 
    # Load the fine-tuned RoBERTa and DistilBERT models and tokenizers 
    model_path_roberta = &quot;./custom_roberta_model_recommendation&quot; 
    model_roberta = RobertaForSequenceClassification.from_pretrained(model_path_roberta) 
    tokenizer_roberta = RobertaTokenizer.from_pretrained(model_path_roberta) 
 
    model_path_distilbert = &quot;./custom_distilbert_model&quot; 
    model_distilbert = DistilBertForSequenceClassification.from_pretrained(model_path_distilbert) 
    tokenizer_distilbert = DistilBertTokenizer.from_pretrained(model_path_distilbert) 
 
    # Function to predict sentiment from the user query for RoBERTa model 
    def predict_sentiment_roberta(query): 
        inputs = tokenizer_roberta(query, return_tensors=&quot;pt&quot;, truncation=True, padding=&quot;max_length&quot;, max_length=512) 
        with torch.no_grad(): 
            outputs = model_roberta(**inputs) 
            logits = outputs.logits 
            prediction = torch.argmax(logits, dim=-1).item() 
        return &quot;Positive&quot; if prediction == 1 else &quot;Negative&quot; 
 
    # Function to predict sentiment from the user query for DistilBERT model 
    def predict_sentiment_distilbert(query): 
        inputs = tokenizer_distilbert(query, return_tensors=&quot;pt&quot;, truncation=True, padding=&quot;max_length&quot;, max_length=512) 
        with torch.no_grad(): 
            outputs = model_distilbert(**inputs) 
            logits = outputs.logits 
            prediction = torch.argmax(logits, dim=-1).item() 
        return &quot;Positive&quot; if prediction == 1 else &quot;Negative&quot; 
 
    # Function to handle user queries with RoBERTa model 
    def get_response_roberta(query, dataset): 
        sentiment = predict_sentiment_roberta(query) 
 
        if &quot;best product&quot; in query.lower() or &quot;best reviewed&quot; in query.lower(): 
            best_reviewed_product = dataset.loc[ 
                dataset['review_content'].str.contains('good|best', case=False, na=False) 
            ].sort_values(by='rating', ascending=False).iloc[0] 
            return ( 
                f&quot;**Product:** {best_reviewed_product['product_name']}\n&quot; 
                f&quot;**Rating:** {best_reviewed_product['rating']} stars\n&quot; 
                f&quot;**Price:** ${best_reviewed_product['discounted_price']}&quot; 
            ) 
 
        elif &quot;highest rating&quot; in query.lower(): 
            highest_rated_product = dataset.loc[dataset['rating'] == dataset['rating'].max()].iloc[0] 
            return ( 
                f&quot;**Product:** {highest_rated_product['product_name']}\n&quot; 
                f&quot;**Rating:** {highest_rated_product['rating']} stars\n&quot; 
                f&quot;**Price:** ${highest_rated_product['discounted_price']}&quot; 
            ) 
 
        elif &quot;most expensive&quot; in query.lower(): 
            most_expensive_product = dataset.loc[dataset['discounted_price'] == dataset['discounted_price'].max()].iloc[0] 
            return ( 
                f&quot;**Product:** {most_expensive_product['product_name']}\n&quot; 
                f&quot;**Price:** ${most_expensive_product['discounted_price']}&quot; 
            ) 
 
        elif &quot;cheapest&quot; in query.lower(): 
            cheapest_product = dataset.loc[dataset['discounted_price'] == dataset['discounted_price'].min()].iloc[0] 
            return ( 
                f&quot;**Product:** {cheapest_product['product_name']}\n&quot; 
                f&quot;**Price:** ${cheapest_product['discounted_price']}&quot; 
            ) 
 
        elif &quot;recommend&quot; in query.lower() and sentiment == &quot;Positive&quot;: 
            recommended_product = dataset.sort_values(by='rating', ascending=False).iloc[0] 
            return ( 
                f&quot;**Product:** {recommended_product['product_name']}\n&quot; 
                f&quot;**Rating:** {recommended_product['rating']} stars\n&quot; 
                f&quot;**Price:** ${recommended_product['discounted_price']}&quot; 
            ) 
 
        elif &quot;recommend&quot; in query.lower() and sentiment == &quot;Negative&quot;: 
            least_recommended_product = dataset.sort_values(by='rating', ascending=True).iloc[0] 
            return ( 
                f&quot;**Product:** {least_recommended_product['product_name']}\n&quot; 
                f&quot;**Rating:** {least_recommended_product['rating']} stars\n&quot; 
                f&quot;**Price:** ${least_recommended_product['discounted_price']}&quot; 
            ) 
 
        else: 
            return &quot;I'm sorry, I couldn't understand your query. Please try asking about the best, highest-rated, cheapest, or most expensive product.&quot; 
 
    # Handle query processing based on selected model 
    def process_query(user_query, dataset): 
        # Check for price-related terms 
        if &quot;price&quot; in user_query.lower(): 
            return dataset[[&quot;actual_price&quot;, &quot;discounted_price&quot;]].head(1).to_dict(orient='records')[0] 
 
        # Check for link-related terms 
        if &quot;link&quot; in user_query.lower(): 
            return dataset[[&quot;product_link&quot;]].head(1).to_dict(orient='records')[0] 
 
        # If everything is mentioned, return the requested columns 
        if &quot;everything&quot; in user_query.lower(): 
            return dataset[ 
                [&quot;discounted_price&quot;, &quot;actual_price&quot;, &quot;rating&quot;, &quot;rating_count&quot;, &quot;about_product&quot;, &quot;review_content&quot;, &quot;product_link&quot;] 
            ].head(1).to_dict(orient='records')[0] 
 
        return &quot;Query did not match any criteria. Please specify price, link, or everything.&quot; 
 
    if query: 
        if query not in current_user[&quot;search_history&quot;]: 
            current_user[&quot;search_history&quot;].append(query) 
            save_user_data() 
 
        # Generate output based on selected model 
        if selected_model == &quot;BART&quot;: 
            st.write(&quot;Generating summary using *BART*...&quot;) 
            summary = generate_summary(query) 
            st.markdown(f&quot;### Summary:\n{summary}&quot;) 
 
        elif selected_model == &quot;FLAN-T5&quot;: 
            st.write(f&quot;You selected *FLAN-T5*. Results for *{query}* will appear here.&quot;) 
 
        elif selected_model == &quot;RoBERTa&quot;: 
            st.write(f&quot;You selected *RoBERTa*.&quot;) 
            response_roberta = get_response_roberta(query, products_df) 
            st.markdown(f&quot;### Response:\n{response_roberta}&quot;) 
 
        elif selected_model == &quot;DistilBERT&quot;: 
            st.write(f&quot;You selected *DistilBERT*. Processing query...&quot;) 
            sentiment = predict_sentiment_distilbert(query) 
            st.markdown(f&quot;Sentiment Analysis Result: {sentiment}&quot;) 
            response_distilbert = process_query(query, products_df) 
            st.markdown(f&quot;### Response:\n{response_distilbert}&quot;) 
 
        elif selected_model == &quot;T5&quot;: 
            st.write(f&quot;You selected *T5*. Results for *{query}* will appear here.&quot;)'''</span>

<span class="s2">import </span><span class="s1">streamlit </span><span class="s2">as </span><span class="s1">st  </span><span class="s3"># Import Streamlit first to allow page config</span>

<span class="s3"># Page Configuration (MUST be first Streamlit command)</span>
<span class="s1">st.set_page_config(</span>
    <span class="s1">page_title=</span><span class="s4">&quot;Amazon GPT Login&quot;</span><span class="s2">,</span>
    <span class="s1">page_icon=</span><span class="s4">&quot;&quot;</span><span class="s2">,</span>
    <span class="s1">layout=</span><span class="s4">&quot;wide&quot;</span><span class="s2">,</span>
<span class="s1">)</span>

<span class="s2">import </span><span class="s1">json</span>
<span class="s2">import </span><span class="s1">os</span>
<span class="s2">import </span><span class="s1">re</span>
<span class="s2">from </span><span class="s1">bart_model </span><span class="s2">import </span><span class="s1">generate_summary  </span><span class="s3"># Import the BART summary generator</span>
<span class="s2">import </span><span class="s1">pandas </span><span class="s2">as </span><span class="s1">pd</span>
<span class="s2">from </span><span class="s1">transformers </span><span class="s2">import </span><span class="s1">RobertaTokenizer</span><span class="s2">, </span><span class="s1">RobertaForSequenceClassification</span>
<span class="s2">import </span><span class="s1">torch</span>

<span class="s3"># Load the dataset</span>
<span class="s1">products_df = pd.read_csv(</span><span class="s4">&quot;amazon.csv&quot;</span><span class="s1">)  </span><span class="s3"># Replace with your dataset</span>
<span class="s1">products_df.dropna(inplace=</span><span class="s2">True</span><span class="s1">)  </span><span class="s3"># Remove rows with missing data</span>

<span class="s3"># File to store user data</span>
<span class="s1">USER_DATA_FILE = </span><span class="s4">&quot;user_data.json&quot;</span>

<span class="s3"># Load or initialize user data</span>
<span class="s2">if not </span><span class="s1">os.path.exists(USER_DATA_FILE):</span>
    <span class="s2">with </span><span class="s1">open(USER_DATA_FILE</span><span class="s2">, </span><span class="s4">&quot;w&quot;</span><span class="s1">) </span><span class="s2">as </span><span class="s1">f:</span>
        <span class="s1">json.dump({}</span><span class="s2">, </span><span class="s1">f)</span>

<span class="s2">with </span><span class="s1">open(USER_DATA_FILE</span><span class="s2">, </span><span class="s4">&quot;r&quot;</span><span class="s1">) </span><span class="s2">as </span><span class="s1">f:</span>
    <span class="s1">user_data = json.load(f)</span>

<span class="s2">def </span><span class="s1">save_user_data():</span>
    <span class="s0">&quot;&quot;&quot;Save user data back to the file.&quot;&quot;&quot;</span>
    <span class="s2">with </span><span class="s1">open(USER_DATA_FILE</span><span class="s2">, </span><span class="s4">&quot;w&quot;</span><span class="s1">) </span><span class="s2">as </span><span class="s1">f:</span>
        <span class="s1">json.dump(user_data</span><span class="s2">, </span><span class="s1">f</span><span class="s2">, </span><span class="s1">indent=</span><span class="s5">4</span><span class="s1">)</span>

<span class="s2">def </span><span class="s1">validate_name(name):</span>
    <span class="s2">return </span><span class="s1">bool(re.match(</span><span class="s4">&quot;^[A-Za-z ]+$&quot;</span><span class="s2">, </span><span class="s1">name))</span>

<span class="s2">def </span><span class="s1">validate_email(email):</span>
    <span class="s2">return </span><span class="s1">bool(re.match(</span><span class="s4">r&quot;^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$&quot;</span><span class="s2">, </span><span class="s1">email))</span>

<span class="s2">def </span><span class="s1">validate_phone(phone):</span>
    <span class="s2">return </span><span class="s1">phone.isdigit() </span><span class="s2">and </span><span class="s5">10 </span><span class="s1">&lt;= len(phone) &lt;= </span><span class="s5">15</span>

<span class="s3"># Check if user is logged in</span>
<span class="s2">if </span><span class="s4">&quot;logged_in_user&quot; </span><span class="s2">not in </span><span class="s1">st.session_state:</span>
    <span class="s1">st.session_state.logged_in_user = </span><span class="s2">None</span>

<span class="s3"># Login Page Design</span>
<span class="s2">if not </span><span class="s1">st.session_state.logged_in_user:</span>
    <span class="s3"># Layout for Login Page</span>
    <span class="s1">col1</span><span class="s2">, </span><span class="s1">col2 = st.columns([</span><span class="s5">1</span><span class="s2">, </span><span class="s5">2</span><span class="s1">])</span>

    <span class="s3"># Left Side - Login Form</span>
    <span class="s2">with </span><span class="s1">col1:</span>
        <span class="s1">st.markdown(</span>
            <span class="s4">&quot;&quot;&quot; 
            &lt;div style='display: flex; justify-content: center;'&gt; 
                &lt;img src='https://upload.wikimedia.org/wikipedia/commons/d/de/Amazon_icon.png' width='100'/&gt; 
            &lt;/div&gt; 
            &quot;&quot;&quot;</span><span class="s2">,</span>
            <span class="s1">unsafe_allow_html=</span><span class="s2">True</span>
        <span class="s1">)</span>
        <span class="s1">st.markdown(</span><span class="s4">&quot;&lt;h1 style='color: #FF9900; text-align: center;'&gt;Amazon GPT Login&lt;/h1&gt;&quot;</span><span class="s2">, </span><span class="s1">unsafe_allow_html=</span><span class="s2">True</span><span class="s1">)</span>

        <span class="s2">with </span><span class="s1">st.form(</span><span class="s4">&quot;login_form&quot;</span><span class="s1">):</span>
            <span class="s1">name = st.text_input(</span><span class="s4">&quot;Full Name:&quot;</span><span class="s1">)</span>
            <span class="s1">email = st.text_input(</span><span class="s4">&quot;Email Address:&quot;</span><span class="s1">)</span>
            <span class="s1">phone = st.text_input(</span><span class="s4">&quot;Phone Number:&quot;</span><span class="s1">)</span>

            <span class="s1">submitted = st.form_submit_button(</span><span class="s4">&quot;Login&quot;</span><span class="s1">)</span>
            <span class="s2">if </span><span class="s1">submitted:</span>
                <span class="s1">errors = []</span>
                <span class="s2">if not </span><span class="s1">validate_name(name):</span>
                    <span class="s1">errors.append(</span><span class="s4">&quot;Invalid Name: Only letters and spaces are allowed.&quot;</span><span class="s1">)</span>
                <span class="s2">if not </span><span class="s1">validate_email(email):</span>
                    <span class="s1">errors.append(</span><span class="s4">&quot;Invalid Email: Enter a valid email address.&quot;</span><span class="s1">)</span>
                <span class="s2">if not </span><span class="s1">validate_phone(phone):</span>
                    <span class="s1">errors.append(</span><span class="s4">&quot;Invalid Phone: Must be 10-15 digits.&quot;</span><span class="s1">)</span>

                <span class="s2">if </span><span class="s1">errors:</span>
                    <span class="s1">st.error(</span><span class="s4">&quot; &quot;</span><span class="s1">.join(errors))</span>
                <span class="s2">else</span><span class="s1">:</span>
                    <span class="s2">if </span><span class="s1">email </span><span class="s2">not in </span><span class="s1">user_data:</span>
                        <span class="s1">user_data[email] = {</span><span class="s4">&quot;name&quot;</span><span class="s1">: name</span><span class="s2">, </span><span class="s4">&quot;phone&quot;</span><span class="s1">: phone</span><span class="s2">, </span><span class="s4">&quot;search_history&quot;</span><span class="s1">: []}</span>
                        <span class="s1">save_user_data()</span>

                    <span class="s1">st.session_state.logged_in_user = email</span>
                    <span class="s1">st.success(</span><span class="s4">f&quot;Welcome, </span><span class="s2">{</span><span class="s1">name</span><span class="s2">}</span><span class="s4">!&quot;</span><span class="s1">)</span>

    <span class="s3"># Right Side - Yellow Background</span>
    <span class="s2">with </span><span class="s1">col2:</span>
        <span class="s1">st.markdown(</span>
            <span class="s4">&quot;&quot;&quot; 
            &lt;div style='background-color: #FF9900; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center;'&gt; 
                &lt;h1 style='color: black; text-align: center; font-size: 50px;'&gt;AMAZON PRODUCT RESEARCH&lt;/h1&gt; 
                &lt;h2 style='color: black; text-align: center; font-size: 30px;'&gt;MERRY CHRISTMAS 🎄&lt;/h2&gt; 
            &lt;/div&gt; 
            &quot;&quot;&quot;</span><span class="s2">,</span>
            <span class="s1">unsafe_allow_html=</span><span class="s2">True,</span>
        <span class="s1">)</span>

<span class="s2">else</span><span class="s1">:</span>
    <span class="s3"># Main Interface</span>
    <span class="s1">current_user_email = st.session_state.logged_in_user</span>
    <span class="s1">current_user = user_data[current_user_email]</span>

    <span class="s3"># Sidebar - Model Selection and History</span>
    <span class="s1">st.sidebar.title(</span><span class="s4">&quot;Options&quot;</span><span class="s1">)</span>
    <span class="s1">st.sidebar.subheader(</span><span class="s4">&quot;Select Model&quot;</span><span class="s1">)</span>
    <span class="s1">model_options = [</span><span class="s4">&quot;BART&quot;</span><span class="s2">, </span><span class="s4">&quot;RoBERTa&quot;</span><span class="s2">, </span><span class="s4">&quot;DistilBERT&quot;</span><span class="s1">]</span>
    <span class="s1">selected_model = st.sidebar.radio(</span><span class="s4">&quot;Choose a model:&quot;</span><span class="s2">, </span><span class="s1">model_options)</span>

    <span class="s1">st.sidebar.subheader(</span><span class="s4">&quot;Search History&quot;</span><span class="s1">)</span>
    <span class="s3"># Sidebar background set to white</span>
    <span class="s2">with </span><span class="s1">st.sidebar:</span>
        <span class="s1">st.markdown(</span>
            <span class="s4">&quot;&quot;&quot; 
            &lt;style&gt; 
                .css-1v3fvcr {  
                    background-color: white; 
                } 
            &lt;/style&gt; 
            &quot;&quot;&quot;</span><span class="s2">, </span><span class="s1">unsafe_allow_html=</span><span class="s2">True</span>
        <span class="s1">)</span>
    <span class="s2">if </span><span class="s1">current_user[</span><span class="s4">&quot;search_history&quot;</span><span class="s1">]:</span>
        <span class="s1">st.sidebar.markdown(</span>
            <span class="s4">&quot;</span><span class="s2">\n</span><span class="s4">&quot;</span><span class="s1">.join([</span><span class="s4">f&quot;- </span><span class="s2">{</span><span class="s1">item</span><span class="s2">}</span><span class="s4">&quot; </span><span class="s2">for </span><span class="s1">item </span><span class="s2">in </span><span class="s1">current_user[</span><span class="s4">&quot;search_history&quot;</span><span class="s1">]])</span>
        <span class="s1">)</span>
    <span class="s2">else</span><span class="s1">:</span>
        <span class="s1">st.sidebar.write(</span><span class="s4">&quot;No search history yet.&quot;</span><span class="s1">)</span>

    <span class="s3"># Main Header</span>
    <span class="s1">st.markdown(</span><span class="s4">&quot;&lt;h1 style='color: #FF9900; text-align: center;'&gt;Amazon Product Research&lt;/h1&gt;&quot;</span><span class="s2">, </span><span class="s1">unsafe_allow_html=</span><span class="s2">True</span><span class="s1">)</span>

    <span class="s1">logout = st.button(</span><span class="s4">&quot;Logout&quot;</span><span class="s2">, </span><span class="s1">key=</span><span class="s4">&quot;logout_button&quot;</span><span class="s2">, </span><span class="s1">help=</span><span class="s4">&quot;Logout&quot;</span><span class="s1">)</span>
    <span class="s2">if </span><span class="s1">logout:</span>
        <span class="s1">st.session_state.logged_in_user = </span><span class="s2">None</span>

    <span class="s1">st.markdown(</span><span class="s4">f&quot;&lt;h3 style='text-align: center;'&gt;Welcome, </span><span class="s2">{</span><span class="s1">current_user[</span><span class="s4">'name'</span><span class="s1">]</span><span class="s2">}</span><span class="s4">&lt;/h3&gt;&quot;</span><span class="s2">, </span><span class="s1">unsafe_allow_html=</span><span class="s2">True</span><span class="s1">)</span>
    <span class="s1">query = st.text_input(</span><span class="s4">&quot;Search for a product:&quot;</span><span class="s1">)</span>

    <span class="s3"># Load the fine-tuned RoBERTa model and tokenizer</span>
    <span class="s1">model_path_roberta = </span><span class="s4">&quot;./custom_roberta_model_recommendation&quot;</span>
    <span class="s1">model_roberta = RobertaForSequenceClassification.from_pretrained(model_path_roberta)</span>
    <span class="s1">tokenizer_roberta = RobertaTokenizer.from_pretrained(model_path_roberta)</span>

    <span class="s3"># Function to predict sentiment from the user query for RoBERTa model</span>
    <span class="s2">def </span><span class="s1">predict_sentiment_roberta(query):</span>
        <span class="s1">inputs = tokenizer_roberta(query</span><span class="s2">, </span><span class="s1">return_tensors=</span><span class="s4">&quot;pt&quot;</span><span class="s2">, </span><span class="s1">truncation=</span><span class="s2">True, </span><span class="s1">padding=</span><span class="s4">&quot;max_length&quot;</span><span class="s2">, </span><span class="s1">max_length=</span><span class="s5">512</span><span class="s1">)</span>
        <span class="s2">with </span><span class="s1">torch.no_grad():</span>
            <span class="s1">outputs = model_roberta(**inputs)</span>
            <span class="s1">logits = outputs.logits</span>
            <span class="s1">prediction = torch.argmax(logits</span><span class="s2">, </span><span class="s1">dim=-</span><span class="s5">1</span><span class="s1">).item()</span>
        <span class="s2">return </span><span class="s4">&quot;Positive&quot; </span><span class="s2">if </span><span class="s1">prediction == </span><span class="s5">1 </span><span class="s2">else </span><span class="s4">&quot;Negative&quot;</span>

    <span class="s3"># Function to handle user queries with RoBERTa model</span>
    <span class="s2">def </span><span class="s1">get_response_roberta(query</span><span class="s2">, </span><span class="s1">dataset):</span>
        <span class="s1">sentiment = predict_sentiment_roberta(query)</span>

        <span class="s2">if </span><span class="s4">&quot;best product&quot; </span><span class="s2">in </span><span class="s1">query.lower() </span><span class="s2">or </span><span class="s4">&quot;best reviewed&quot; </span><span class="s2">in </span><span class="s1">query.lower():</span>
            <span class="s1">best_reviewed_product = dataset.loc[</span>
                <span class="s1">dataset[</span><span class="s4">'review_content'</span><span class="s1">].str.contains(</span><span class="s4">'good|best'</span><span class="s2">, </span><span class="s1">case=</span><span class="s2">False, </span><span class="s1">na=</span><span class="s2">False</span><span class="s1">)</span>
            <span class="s1">].sort_values(by=</span><span class="s4">'rating'</span><span class="s2">, </span><span class="s1">ascending=</span><span class="s2">False</span><span class="s1">).iloc[</span><span class="s5">0</span><span class="s1">]</span>
            <span class="s2">return </span><span class="s1">(</span>
                <span class="s4">f&quot;**Product:** </span><span class="s2">{</span><span class="s1">best_reviewed_product[</span><span class="s4">'product_name'</span><span class="s1">]</span><span class="s2">}\n</span><span class="s4">&quot;</span>
                <span class="s4">f&quot;**Rating:** </span><span class="s2">{</span><span class="s1">best_reviewed_product[</span><span class="s4">'rating'</span><span class="s1">]</span><span class="s2">} </span><span class="s4">stars</span><span class="s2">\n</span><span class="s4">&quot;</span>
                <span class="s4">f&quot;**Price:** $</span><span class="s2">{</span><span class="s1">best_reviewed_product[</span><span class="s4">'discounted_price'</span><span class="s1">]</span><span class="s2">}</span><span class="s4">&quot;</span>
            <span class="s1">)</span>

        <span class="s2">elif </span><span class="s4">&quot;highest rating&quot; </span><span class="s2">in </span><span class="s1">query.lower():</span>
            <span class="s1">highest_rated_product = dataset.loc[dataset[</span><span class="s4">'rating'</span><span class="s1">] == dataset[</span><span class="s4">'rating'</span><span class="s1">].max()].iloc[</span><span class="s5">0</span><span class="s1">]</span>
            <span class="s2">return </span><span class="s1">(</span>
                <span class="s4">f&quot;**Product:** </span><span class="s2">{</span><span class="s1">highest_rated_product[</span><span class="s4">'product_name'</span><span class="s1">]</span><span class="s2">}\n</span><span class="s4">&quot;</span>
                <span class="s4">f&quot;**Rating:** </span><span class="s2">{</span><span class="s1">highest_rated_product[</span><span class="s4">'rating'</span><span class="s1">]</span><span class="s2">} </span><span class="s4">stars</span><span class="s2">\n</span><span class="s4">&quot;</span>
                <span class="s4">f&quot;**Price:** $</span><span class="s2">{</span><span class="s1">highest_rated_product[</span><span class="s4">'discounted_price'</span><span class="s1">]</span><span class="s2">}</span><span class="s4">&quot;</span>
            <span class="s1">)</span>

        <span class="s2">elif </span><span class="s4">&quot;most expensive&quot; </span><span class="s2">in </span><span class="s1">query.lower():</span>
            <span class="s1">most_expensive_product = dataset.loc[dataset[</span><span class="s4">'discounted_price'</span><span class="s1">] == dataset[</span><span class="s4">'discounted_price'</span><span class="s1">].max()].iloc[</span><span class="s5">0</span><span class="s1">]</span>
            <span class="s2">return </span><span class="s1">(</span>
                <span class="s4">f&quot;**Product:** </span><span class="s2">{</span><span class="s1">most_expensive_product[</span><span class="s4">'product_name'</span><span class="s1">]</span><span class="s2">}\n</span><span class="s4">&quot;</span>
                <span class="s4">f&quot;**Price:** $</span><span class="s2">{</span><span class="s1">most_expensive_product[</span><span class="s4">'discounted_price'</span><span class="s1">]</span><span class="s2">}</span><span class="s4">&quot;</span>
            <span class="s1">)</span>

        <span class="s2">elif </span><span class="s4">&quot;cheapest&quot; </span><span class="s2">in </span><span class="s1">query.lower():</span>
            <span class="s1">cheapest_product = dataset.loc[dataset[</span><span class="s4">'discounted_price'</span><span class="s1">] == dataset[</span><span class="s4">'discounted_price'</span><span class="s1">].min()].iloc[</span><span class="s5">0</span><span class="s1">]</span>
            <span class="s2">return </span><span class="s1">(</span>
                <span class="s4">f&quot;**Product:** </span><span class="s2">{</span><span class="s1">cheapest_product[</span><span class="s4">'product_name'</span><span class="s1">]</span><span class="s2">}\n</span><span class="s4">&quot;</span>
                <span class="s4">f&quot;**Price:** $</span><span class="s2">{</span><span class="s1">cheapest_product[</span><span class="s4">'discounted_price'</span><span class="s1">]</span><span class="s2">}</span><span class="s4">&quot;</span>
            <span class="s1">)</span>

        <span class="s2">elif </span><span class="s4">&quot;recommend&quot; </span><span class="s2">in </span><span class="s1">query.lower() </span><span class="s2">and </span><span class="s1">sentiment == </span><span class="s4">&quot;Positive&quot;</span><span class="s1">:</span>
            <span class="s1">recommended_product = dataset.sort_values(by=</span><span class="s4">'rating'</span><span class="s2">, </span><span class="s1">ascending=</span><span class="s2">False</span><span class="s1">).iloc[</span><span class="s5">0</span><span class="s1">]</span>
            <span class="s2">return </span><span class="s1">(</span>
                <span class="s4">f&quot;**Product:** </span><span class="s2">{</span><span class="s1">recommended_product[</span><span class="s4">'product_name'</span><span class="s1">]</span><span class="s2">}\n</span><span class="s4">&quot;</span>
                <span class="s4">f&quot;**Rating:** </span><span class="s2">{</span><span class="s1">recommended_product[</span><span class="s4">'rating'</span><span class="s1">]</span><span class="s2">} </span><span class="s4">stars</span><span class="s2">\n</span><span class="s4">&quot;</span>
                <span class="s4">f&quot;**Price:** $</span><span class="s2">{</span><span class="s1">recommended_product[</span><span class="s4">'discounted_price'</span><span class="s1">]</span><span class="s2">}</span><span class="s4">&quot;</span>
            <span class="s1">)</span>

        <span class="s2">elif </span><span class="s4">&quot;recommend&quot; </span><span class="s2">in </span><span class="s1">query.lower() </span><span class="s2">and </span><span class="s1">sentiment == </span><span class="s4">&quot;Negative&quot;</span><span class="s1">:</span>
            <span class="s1">least_recommended_product = dataset.sort_values(by=</span><span class="s4">'rating'</span><span class="s2">, </span><span class="s1">ascending=</span><span class="s2">True</span><span class="s1">).iloc[</span><span class="s5">0</span><span class="s1">]</span>
            <span class="s2">return </span><span class="s1">(</span>
                <span class="s4">f&quot;**Product:** </span><span class="s2">{</span><span class="s1">least_recommended_product[</span><span class="s4">'product_name'</span><span class="s1">]</span><span class="s2">}\n</span><span class="s4">&quot;</span>
                <span class="s4">f&quot;**Rating:** </span><span class="s2">{</span><span class="s1">least_recommended_product[</span><span class="s4">'rating'</span><span class="s1">]</span><span class="s2">} </span><span class="s4">stars</span><span class="s2">\n</span><span class="s4">&quot;</span>
                <span class="s4">f&quot;**Price:** $</span><span class="s2">{</span><span class="s1">least_recommended_product[</span><span class="s4">'discounted_price'</span><span class="s1">]</span><span class="s2">}</span><span class="s4">&quot;</span>
            <span class="s1">)</span>

        <span class="s2">else</span><span class="s1">:</span>
            <span class="s2">return </span><span class="s4">&quot;I'm sorry, I couldn't understand your query. Please try asking about the best, highest-rated, cheapest, or most expensive product.&quot;</span>

    <span class="s2">if </span><span class="s1">query:</span>
        <span class="s2">if </span><span class="s1">query </span><span class="s2">not in </span><span class="s1">current_user[</span><span class="s4">&quot;search_history&quot;</span><span class="s1">]:</span>
            <span class="s1">current_user[</span><span class="s4">&quot;search_history&quot;</span><span class="s1">].append(query)</span>
            <span class="s1">save_user_data()</span>

        <span class="s3"># Generate output based on selected model</span>
        <span class="s2">if </span><span class="s1">selected_model == </span><span class="s4">&quot;BART&quot;</span><span class="s1">:</span>
            <span class="s1">st.write(</span><span class="s4">&quot;Generating summary using *BART*...&quot;</span><span class="s1">)</span>
            <span class="s1">summary = generate_summary(query)</span>
            <span class="s1">st.markdown(</span><span class="s4">f&quot;### Summary:</span><span class="s2">\n{</span><span class="s1">summary</span><span class="s2">}</span><span class="s4">&quot;</span><span class="s1">)</span>

        <span class="s2">elif </span><span class="s1">selected_model == </span><span class="s4">&quot;FLAN-T5&quot;</span><span class="s1">:</span>
            <span class="s1">st.write(</span><span class="s4">f&quot;You selected *FLAN-T5*. Results for *</span><span class="s2">{</span><span class="s1">query</span><span class="s2">}</span><span class="s4">* will appear here.&quot;</span><span class="s1">)</span>

        <span class="s2">elif </span><span class="s1">selected_model == </span><span class="s4">&quot;RoBERTa&quot;</span><span class="s1">:</span>
            <span class="s1">st.write(</span><span class="s4">f&quot;You selected *RoBERTa*.&quot;</span><span class="s1">)</span>
            <span class="s1">response_roberta = get_response_roberta(query</span><span class="s2">, </span><span class="s1">products_df)</span>
            <span class="s1">st.markdown(</span><span class="s4">f&quot;### Response:</span><span class="s2">\n{</span><span class="s1">response_roberta</span><span class="s2">}</span><span class="s4">&quot;</span><span class="s1">)</span>

        <span class="s2">elif </span><span class="s1">selected_model == </span><span class="s4">&quot;DistilBERT&quot;</span><span class="s1">:</span>
            <span class="s1">st.write(</span><span class="s4">f&quot;You selected *DistilBERT*. Results for *</span><span class="s2">{</span><span class="s1">query</span><span class="s2">}</span><span class="s4">* will appear here.&quot;</span><span class="s1">)</span>

        <span class="s2">elif </span><span class="s1">selected_model == </span><span class="s4">&quot;T5&quot;</span><span class="s1">:</span>
            <span class="s1">st.write(</span><span class="s4">f&quot;You selected *T5*. Results for *</span><span class="s2">{</span><span class="s1">query</span><span class="s2">}</span><span class="s4">* will appear here.&quot;</span><span class="s1">)</span>



</pre>
</body>
</html>
