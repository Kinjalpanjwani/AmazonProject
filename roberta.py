<html>
<head>
<title>roberta.py</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type="text/css">
.s0 { color: #cc7832;}
.s1 { color: #a9b7c6;}
.s2 { color: #6a8759;}
.s3 { color: #6897bb;}
</style>
</head>
<body bgcolor="#2b2b2b">
<table CELLSPACING=0 CELLPADDING=5 COLS=1 WIDTH="100%" BGCOLOR="#606060" >
<tr><td><center>
<font face="Arial, Helvetica" color="#000000">
roberta.py</font>
</center></td></tr></table>
<pre><span class="s0">def </span><span class="s1">get_response(query</span><span class="s0">, </span><span class="s1">dataset):</span>
    <span class="s1">sentiment = predict_sentiment(query)</span>

    <span class="s0">if </span><span class="s2">&quot;best product&quot; </span><span class="s0">in </span><span class="s1">query.lower() </span><span class="s0">or </span><span class="s2">&quot;best reviewed&quot; </span><span class="s0">in </span><span class="s1">query.lower():</span>
        <span class="s1">best_reviewed_product = dataset.loc[</span>
            <span class="s1">dataset[</span><span class="s2">'review_content'</span><span class="s1">].str.contains(</span><span class="s2">'good|best'</span><span class="s0">, </span><span class="s1">case=</span><span class="s0">False, </span><span class="s1">na=</span><span class="s0">False</span><span class="s1">)</span>
        <span class="s1">].sort_values(by=</span><span class="s2">'rating'</span><span class="s0">, </span><span class="s1">ascending=</span><span class="s0">False</span><span class="s1">).iloc[</span><span class="s3">0</span><span class="s1">]</span>
        <span class="s0">return </span><span class="s1">(</span><span class="s2">f&quot;- **Product Name:** </span><span class="s0">{</span><span class="s1">best_reviewed_product[</span><span class="s2">'product_name'</span><span class="s1">]</span><span class="s0">}\n</span><span class="s2">&quot;</span>
                <span class="s2">f&quot;- **Rating:** </span><span class="s0">{</span><span class="s1">best_reviewed_product[</span><span class="s2">'rating'</span><span class="s1">]</span><span class="s0">} </span><span class="s2">stars</span><span class="s0">\n</span><span class="s2">&quot;</span>
                <span class="s2">f&quot;- **Price:** $</span><span class="s0">{</span><span class="s1">best_reviewed_product[</span><span class="s2">'discounted_price'</span><span class="s1">]</span><span class="s0">}</span><span class="s2">&quot;</span><span class="s1">)</span>

    <span class="s0">elif </span><span class="s2">&quot;highest rating&quot; </span><span class="s0">in </span><span class="s1">query.lower():</span>
        <span class="s1">highest_rated_product = dataset.loc[dataset[</span><span class="s2">'rating'</span><span class="s1">] == dataset[</span><span class="s2">'rating'</span><span class="s1">].max()].iloc[</span><span class="s3">0</span><span class="s1">]</span>
        <span class="s0">return </span><span class="s1">(</span><span class="s2">f&quot;- **Product Name:** </span><span class="s0">{</span><span class="s1">highest_rated_product[</span><span class="s2">'product_name'</span><span class="s1">]</span><span class="s0">}\n</span><span class="s2">&quot;</span>
                <span class="s2">f&quot;- **Rating:** </span><span class="s0">{</span><span class="s1">highest_rated_product[</span><span class="s2">'rating'</span><span class="s1">]</span><span class="s0">} </span><span class="s2">stars</span><span class="s0">\n</span><span class="s2">&quot;</span>
                <span class="s2">f&quot;- **Price:** $</span><span class="s0">{</span><span class="s1">highest_rated_product[</span><span class="s2">'discounted_price'</span><span class="s1">]</span><span class="s0">}</span><span class="s2">&quot;</span><span class="s1">)</span>

    <span class="s0">elif </span><span class="s2">&quot;most expensive&quot; </span><span class="s0">in </span><span class="s1">query.lower():</span>
        <span class="s1">most_expensive_product = dataset.loc[dataset[</span><span class="s2">'discounted_price'</span><span class="s1">] == dataset[</span><span class="s2">'discounted_price'</span><span class="s1">].max()].iloc[</span><span class="s3">0</span><span class="s1">]</span>
        <span class="s0">return </span><span class="s1">(</span><span class="s2">f&quot;- **Product Name:** </span><span class="s0">{</span><span class="s1">most_expensive_product[</span><span class="s2">'product_name'</span><span class="s1">]</span><span class="s0">}\n</span><span class="s2">&quot;</span>
                <span class="s2">f&quot;- **Price:** $</span><span class="s0">{</span><span class="s1">most_expensive_product[</span><span class="s2">'discounted_price'</span><span class="s1">]</span><span class="s0">}</span><span class="s2">&quot;</span><span class="s1">)</span>

    <span class="s0">elif </span><span class="s2">&quot;cheapest&quot; </span><span class="s0">in </span><span class="s1">query.lower():</span>
        <span class="s1">cheapest_product = dataset.loc[dataset[</span><span class="s2">'discounted_price'</span><span class="s1">] == dataset[</span><span class="s2">'discounted_price'</span><span class="s1">].min()].iloc[</span><span class="s3">0</span><span class="s1">]</span>
        <span class="s0">return </span><span class="s1">(</span><span class="s2">f&quot;- **Product Name:** </span><span class="s0">{</span><span class="s1">cheapest_product[</span><span class="s2">'product_name'</span><span class="s1">]</span><span class="s0">}\n</span><span class="s2">&quot;</span>
                <span class="s2">f&quot;- **Price:** $</span><span class="s0">{</span><span class="s1">cheapest_product[</span><span class="s2">'discounted_price'</span><span class="s1">]</span><span class="s0">}</span><span class="s2">&quot;</span><span class="s1">)</span>

    <span class="s0">elif </span><span class="s2">&quot;recommend&quot; </span><span class="s0">in </span><span class="s1">query.lower() </span><span class="s0">and </span><span class="s1">sentiment == </span><span class="s2">&quot;Positive&quot;</span><span class="s1">:</span>
        <span class="s1">recommended_product = dataset.sort_values(by=</span><span class="s2">'rating'</span><span class="s0">, </span><span class="s1">ascending=</span><span class="s0">False</span><span class="s1">).iloc[</span><span class="s3">0</span><span class="s1">]</span>
        <span class="s0">return </span><span class="s1">(</span><span class="s2">f&quot;- **Product Name:** </span><span class="s0">{</span><span class="s1">recommended_product[</span><span class="s2">'product_name'</span><span class="s1">]</span><span class="s0">}\n</span><span class="s2">&quot;</span>
                <span class="s2">f&quot;- **Rating:** </span><span class="s0">{</span><span class="s1">recommended_product[</span><span class="s2">'rating'</span><span class="s1">]</span><span class="s0">} </span><span class="s2">stars</span><span class="s0">\n</span><span class="s2">&quot;</span>
                <span class="s2">f&quot;- **Price:** $</span><span class="s0">{</span><span class="s1">recommended_product[</span><span class="s2">'discounted_price'</span><span class="s1">]</span><span class="s0">}</span><span class="s2">&quot;</span><span class="s1">)</span>

    <span class="s0">elif </span><span class="s2">&quot;recommend&quot; </span><span class="s0">in </span><span class="s1">query.lower() </span><span class="s0">and </span><span class="s1">sentiment == </span><span class="s2">&quot;Negative&quot;</span><span class="s1">:</span>
        <span class="s1">least_recommended_product = dataset.sort_values(by=</span><span class="s2">'rating'</span><span class="s0">, </span><span class="s1">ascending=</span><span class="s0">True</span><span class="s1">).iloc[</span><span class="s3">0</span><span class="s1">]</span>
        <span class="s0">return </span><span class="s1">(</span><span class="s2">f&quot;- **Product Name:** </span><span class="s0">{</span><span class="s1">least_recommended_product[</span><span class="s2">'product_name'</span><span class="s1">]</span><span class="s0">}\n</span><span class="s2">&quot;</span>
                <span class="s2">f&quot;- **Rating:** </span><span class="s0">{</span><span class="s1">least_recommended_product[</span><span class="s2">'rating'</span><span class="s1">]</span><span class="s0">} </span><span class="s2">stars&quot;</span><span class="s1">)</span>

    <span class="s0">else</span><span class="s1">:</span>
        <span class="s0">return </span><span class="s2">&quot;I'm sorry, I couldn't understand your query. Please try asking about the best, highest-rated, cheapest, or most expensive product.&quot;</span>
</pre>
</body>
</html>