import openai


def opt_gpt_summarise(input_data, opt_output):
    # Ensure your API key is correctly set in your environment variables
    openai.api_key = "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"

    # Construct the messages
    messages = [
        {
            "role": "system",
            "content": "You will be provided with the output of a basic power system capacity expansion model. The output is a DataFrame that includes some information. Btw, Energy Not Supplied category is not a generator but is the shedded load. I want you to write a Formal narrative style less than 200 words for me ONLY BASED ON THE DATA." 
        },
        {
            "role": "user",
            "content": f"Input Data about Generators: {input_data}, Output of optimisation model: {opt_output}.",
        },
    ]

    try:
        # Making the API call
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-3.5-turbo" based on your subscription
            messages=messages,
            max_tokens=600,  # Adjust the number of tokens as needed
            n=1,  # Number of completions to generate
            stop=None,  # Specify any stopping criteria if needed
        )

        # Extracting the response
        # generated_text = response.choices[0].message['content'].strip()
        generated_text = response.choices[0].message.content.strip()

        return generated_text
    except Exception as e:
        return str(e)



