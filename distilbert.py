<html>
<head>
<title>distilbert.py</title>
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
distilbert.py</font>
</center></td></tr></table>
<pre><span class="s0">'''import pandas as pd 
 
# Load the dataset 
file_path = '/mnt/data/amazon.csv' 
uploaded_df = pd.read_csv(file_path) 
 
# Define a function to process user input 
def process_query(user_query): 
    # Check for price-related terms 
    if &quot;price&quot; in user_query.lower(): 
        return uploaded_df[[&quot;actual_price&quot;, &quot;discounted_price&quot;]].head(1).to_dict(orient='records')[0] 
 
    # Check for link-related terms 
    if &quot;link&quot; in user_query.lower(): 
        return uploaded_df[[&quot;product_link&quot;]].head(1).to_dict(orient='records')[0] 
 
    # If everything is mentioned, return the requested columns 
    if &quot;everything&quot; in user_query.lower(): 
        return uploaded_df[ 
            [&quot;discounted_price&quot;, &quot;actual_price&quot;, &quot;rating&quot;, &quot;rating_count&quot;, &quot;about_product&quot;, &quot;review_content&quot;, &quot;product_link&quot;] 
        ].head(1).to_dict(orient='records')[0] 
 
    return &quot;Query did not match any criteria. Please specify price, link, or everything.&quot; 
 
# Example queries 
query_price = &quot;What is the price of the product?&quot; 
query_link = &quot;Can you provide the link to the product?&quot; 
query_everything = &quot;Give me all the product details.&quot; 
 
# Process queries 
response_price = process_query(query_price) 
response_link = process_query(query_link) 
response_everything = process_query(query_everything) 
 
# Output results 
print(&quot;Response for Price Query:&quot;, response_price) 
print(&quot;Response for Link Query:&quot;, response_link) 
print(&quot;Response for Everything Query:&quot;, response_everything)'''</span>

<span class="s2">import </span><span class="s1">pandas </span><span class="s2">as </span><span class="s1">pd</span>

<span class="s3"># Assuming 'uploaded_df' is already loaded or passed into the function</span>
<span class="s3"># Example: uploaded_df = pd.read_csv('path_to_your_csv_file')</span>

<span class="s3"># Define a function to process user input</span>
<span class="s2">def </span><span class="s1">process_query(user_query</span><span class="s2">, </span><span class="s1">uploaded_df):</span>
    <span class="s3"># Check for price-related terms</span>
    <span class="s2">if </span><span class="s4">&quot;price&quot; </span><span class="s2">in </span><span class="s1">user_query.lower():</span>
        <span class="s2">return </span><span class="s1">uploaded_df[[</span><span class="s4">&quot;actual_price&quot;</span><span class="s2">, </span><span class="s4">&quot;discounted_price&quot;</span><span class="s1">]].head(</span><span class="s5">1</span><span class="s1">).to_dict(orient=</span><span class="s4">'records'</span><span class="s1">)[</span><span class="s5">0</span><span class="s1">]</span>

    <span class="s3"># Check for link-related terms</span>
    <span class="s2">if </span><span class="s4">&quot;link&quot; </span><span class="s2">in </span><span class="s1">user_query.lower():</span>
        <span class="s2">return </span><span class="s1">uploaded_df[[</span><span class="s4">&quot;product_link&quot;</span><span class="s1">]].head(</span><span class="s5">1</span><span class="s1">).to_dict(orient=</span><span class="s4">'records'</span><span class="s1">)[</span><span class="s5">0</span><span class="s1">]</span>

    <span class="s3"># If everything is mentioned, return the requested columns</span>
    <span class="s2">if </span><span class="s4">&quot;everything&quot; </span><span class="s2">in </span><span class="s1">user_query.lower():</span>
        <span class="s2">return </span><span class="s1">uploaded_df[</span>
            <span class="s1">[</span><span class="s4">&quot;discounted_price&quot;</span><span class="s2">, </span><span class="s4">&quot;actual_price&quot;</span><span class="s2">, </span><span class="s4">&quot;rating&quot;</span><span class="s2">, </span><span class="s4">&quot;rating_count&quot;</span><span class="s2">, </span><span class="s4">&quot;about_product&quot;</span><span class="s2">, </span><span class="s4">&quot;review_content&quot;</span><span class="s2">, </span><span class="s4">&quot;product_link&quot;</span><span class="s1">]</span>
        <span class="s1">].head(</span><span class="s5">1</span><span class="s1">).to_dict(orient=</span><span class="s4">'records'</span><span class="s1">)[</span><span class="s5">0</span><span class="s1">]</span>

    <span class="s2">return </span><span class="s4">&quot;Query did not match any criteria. Please specify price, link, or everything.&quot;</span>

<span class="s3"># Example queries</span>
<span class="s1">query_price = </span><span class="s4">&quot;What is the price of the product?&quot;</span>
<span class="s1">query_link = </span><span class="s4">&quot;Can you provide the link to the product?&quot;</span>
<span class="s1">query_everything = </span><span class="s4">&quot;Give me all the product details.&quot;</span>

<span class="s3"># Example: Assuming uploaded_df is already loaded as a DataFrame</span>
<span class="s3"># uploaded_df = pd.read_csv('path_to_your_csv_file')  # Replace this line with your DataFrame loading code</span>

<span class="s3"># Process queries</span>
<span class="s1">response_price = process_query(query_price</span><span class="s2">, </span><span class="s1">uploaded_df)</span>
<span class="s1">response_link = process_query(query_link</span><span class="s2">, </span><span class="s1">uploaded_df)</span>
<span class="s1">response_everything = process_query(query_everything</span><span class="s2">, </span><span class="s1">uploaded_df)</span>

<span class="s3"># Output results</span>
<span class="s1">print(</span><span class="s4">&quot;Response for Price Query:&quot;</span><span class="s2">, </span><span class="s1">response_price)</span>
<span class="s1">print(</span><span class="s4">&quot;Response for Link Query:&quot;</span><span class="s2">, </span><span class="s1">response_link)</span>
<span class="s1">print(</span><span class="s4">&quot;Response for Everything Query:&quot;</span><span class="s2">, </span><span class="s1">response_everything)</span>

</pre>
</body>
</html>