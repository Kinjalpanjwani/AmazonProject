<html>
<head>
<title>bart_model.py</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type="text/css">
.s0 { color: #629755; font-style: italic;}
.s1 { color: #a9b7c6;}
.s2 { color: #6a8759;}
.s3 { color: #cc7832;}
.s4 { color: #808080;}
.s5 { color: #6897bb;}
</style>
</head>
<body bgcolor="#2b2b2b">
<table CELLSPACING=0 CELLPADDING=5 COLS=1 WIDTH="100%" BGCOLOR="#606060" >
<tr><td><center>
<font face="Arial, Helvetica" color="#000000">
bart_model.py</font>
</center></td></tr></table>
<pre><span class="s0">'''# bart_model.py 
import torch 
from transformers import BartTokenizer, BartForConditionalGeneration 
 
# Step 1: Load the fine-tuned model and tokenizer 
MODEL_PATH = &quot;./custom_bart_model&quot;  # Path to the saved model 
model = BartForConditionalGeneration.from_pretrained(MODEL_PATH) 
tokenizer = BartTokenizer.from_pretrained(MODEL_PATH) 
 
def generate_summary(product_descriptions): 
    &quot;&quot;&quot; 
    Generate review summaries for a list of product descriptions. 
 
    Args: 
        product_descriptions (list): List of input product descriptions. 
 
    Returns: 
        str: Generated review summaries, each on a new line. 
    &quot;&quot;&quot; 
    review_summaries = [] 
 
    for product_description in product_descriptions: 
        # Tokenize the input 
        inputs = tokenizer( 
            &quot;Product Description: &quot; + product_description, 
            max_length=512, 
            truncation=True, 
            return_tensors=&quot;pt&quot; 
        ) 
 
        # Generate output 
        with torch.no_grad(): 
            outputs = model.generate( 
                inputs[&quot;input_ids&quot;], 
                max_length=128, 
                num_beams=4, 
                early_stopping=True 
            ) 
 
        # Decode the generated output and add to list 
        review_summary = tokenizer.decode(outputs[0], skip_special_tokens=True) 
        review_summaries.append(review_summary) 
 
    # Join all reviews with a newline separator 
    return &quot;\n&quot;.join(review_summaries)'''</span>

<span class="s2">'''import torch 
from transformers import BartTokenizer, BartForConditionalGeneration 
 
# Step 1: Load the fine-tuned model and tokenizer 
MODEL_PATH = &quot;./custom_bart_model&quot;  # Path to the saved model 
model = BartForConditionalGeneration.from_pretrained(MODEL_PATH) 
tokenizer = BartTokenizer.from_pretrained(MODEL_PATH) 
 
def generate_summary(product_descriptions): 
    &quot;&quot;&quot; 
    Generate review summaries for a list of product descriptions. 
 
    Args: 
        product_descriptions (list): List of input product descriptions. 
 
    Returns: 
        str: Generated review summaries, each on a new line with duplicates removed. 
    &quot;&quot;&quot; 
    review_summaries = set()  # Using a set to avoid duplicates 
 
    for idx, product_description in enumerate(product_descriptions): 
        # Tokenize the input 
        inputs = tokenizer( 
            &quot;Product Description: &quot; + product_description, 
            max_length=512, 
            truncation=True, 
            return_tensors=&quot;pt&quot; 
        ) 
 
        # Generate output 
        with torch.no_grad(): 
            outputs = model.generate( 
                inputs[&quot;input_ids&quot;], 
                max_length=128, 
                num_beams=4, 
                early_stopping=True 
            ) 
 
        # Decode the generated output 
        review_summary = tokenizer.decode(outputs[0], skip_special_tokens=True).strip() 
 
        # Add summary to the set 
        review_summaries.add(review_summary) 
 
    # Return all unique summaries joined by a newline 
    return &quot;</span><span class="s3">\n</span><span class="s2">&quot;.join(sorted(review_summaries))  # Sorted for consistency 
 
# Example usage: 
if __name__ == &quot;__main__&quot;: 
    product_descriptions = [ 
        &quot;This is a good product with minor issues.&quot;, 
        &quot;A similar product with good features but bad packaging.&quot;, 
        &quot;The product is very good and easy to use.&quot;, 
        &quot;This is a good product with minor issues.&quot;,  # Intentional duplicate 
        &quot;A good product overall but the packaging needs improvement.&quot;, 
    ] 
    summaries = generate_summary(product_descriptions) 
    print(&quot;</span><span class="s3">\n</span><span class="s2">Generated Review Summaries:</span><span class="s3">\n</span><span class="s2">&quot;, summaries)'''</span>

<span class="s3">import </span><span class="s1">torch</span>
<span class="s3">from </span><span class="s1">transformers </span><span class="s3">import </span><span class="s1">BartTokenizer</span><span class="s3">, </span><span class="s1">BartForConditionalGeneration</span>

<span class="s4"># Step 1: Load the fine-tuned model and tokenizer</span>
<span class="s1">MODEL_PATH = </span><span class="s2">&quot;./custom_bart_model&quot;  </span><span class="s4"># Path to the saved model</span>
<span class="s1">model = BartForConditionalGeneration.from_pretrained(MODEL_PATH)</span>
<span class="s1">tokenizer = BartTokenizer.from_pretrained(MODEL_PATH)</span>

<span class="s3">def </span><span class="s1">generate_summary(product_description):</span>
    <span class="s0">&quot;&quot;&quot; 
    Generate a review summary based on the product description. 
 
    Args: 
        product_description (str): Input product description text. 
 
    Returns: 
        str: Generated review summary. 
    &quot;&quot;&quot;</span>
    <span class="s4"># Tokenize the input</span>
    <span class="s1">inputs = tokenizer(</span>
        <span class="s2">&quot;Product Description: &quot; </span><span class="s1">+ product_description</span><span class="s3">,</span>
        <span class="s1">max_length=</span><span class="s5">512</span><span class="s3">,</span>
        <span class="s1">truncation=</span><span class="s3">True,</span>
        <span class="s1">return_tensors=</span><span class="s2">&quot;pt&quot;</span>
    <span class="s1">)</span>

    <span class="s4"># Generate output</span>
    <span class="s3">with </span><span class="s1">torch.no_grad():</span>
        <span class="s1">outputs = model.generate(</span>
            <span class="s1">inputs[</span><span class="s2">&quot;input_ids&quot;</span><span class="s1">]</span><span class="s3">,</span>
            <span class="s1">max_length=</span><span class="s5">128</span><span class="s3">,</span>
            <span class="s1">num_beams=</span><span class="s5">4</span><span class="s3">,</span>
            <span class="s1">early_stopping=</span><span class="s3">True</span>
        <span class="s1">)</span>

    <span class="s4"># Decode the generated output</span>
    <span class="s3">return </span><span class="s1">tokenizer.decode(outputs[</span><span class="s5">0</span><span class="s1">]</span><span class="s3">, </span><span class="s1">skip_special_tokens=</span><span class="s3">True</span><span class="s1">)</span>


</pre>
</body>
</html>