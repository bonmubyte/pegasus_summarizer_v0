from transformers import PegasusForConditionalGeneration, PegasusTokenizer

def summarize_news(news_text, model_name='tuner007/pegasus_summarizer'):
    # Load the tokenizer and model from the specified model name
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    # Tokenize the input text
    tokens = tokenizer(news_text, truncation=True, padding='longest', return_tensors='pt')

    # Generate the summary
    summary_ids = model.generate(tokens['input_ids'], num_beams=4, max_length=60, min_length=20, length_penalty=2.0, early_stopping=True)

    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Split the summary into three lines
    summary_lines = summary.split('. ')
    three_line_summary = '. '.join(summary_lines[:3]) + '.'

    return three_line_summary

# Example usage with a dummy news text
news_text = """
Novo Nordisk, Europe’s largest company by market capitalization, on Wednesday reported better-than-expected 2023 earnings, as sales of its wildly popular anti-obesity and diabetes drugs continued to soar. The maker of weight loss drug Wegovy and diabetes drug Ozempic reported an increase in sales of 31% in Danish kroner and 36% at constant exchange rates (CER) to 232.3 billion kroner ($33.71 billion). Full-year operating profit jumped by 37% in kroner and 44% at constant exchange rates to 102.6 billion kroner. The Danish pharmaceutical giant said it expects sales growth this year of between 18% and 26% in CER terms, as demand surges for Wegovy and Ozempic, which contain the same active ingredient. The 2023 results were fueled by strong performance in the company’s diabetes and obesity care division, with obesity care in particular spiking by 154% at CER to 41.6 billion. “The unmet needs in type 2 diabetes and obesity are growing by the day, and the rising prevalence of these closely related threats to global health has created surging demand for our GLP-1-based therapies,” Chairman Helge Lund and CEO Lars Fruergaard Jørgensen said in the earnings report. “This has enabled us to reach more patients than at any point in our 100-year history, contributing to strong sales growth across North America and International Operations.” The company also acknowledged that this had resulted in increased pressure on its supply chain, leading to “periodic constraints” across its portfolio as it struggled to keep pace with demand in 2023. “We have responded by investing heavily in expanding our production capacity with the aim of serving millions more patients worldwide. In 2023 alone, we announced investments totalling more than DKK 75 billion in the expansion of our production sites across the globe,” the chairman and CEO said. “With construction now underway on these projects, we strive to operate our existing facilities 24 hours a day, seven days a week, as we produce more of our life-changing medicines than ever before.”
"""

summary = summarize_news(news_text)
print(summary)
