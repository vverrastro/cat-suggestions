from cat.mad_hatter.decorators import hook

@hook (priority=1)
def before_cat_sends_message(message, cat):
    
    # Load settings
    settings = cat.mad_hatter.get_plugin().load_settings()
    num_suggestions = settings["number_of_suggestions"]

    if isinstance(num_suggestions, int) and num_suggestions > 0:

        # Prepare the prompt for the LLM to generate brief suggestions in the same language as the main content message
        prompt = f"""First REMOVE ANY existing suggestions in the main content message [<hr><div>Suggestions: ... </div>].
                    Then, based on the main content message '{message['content']}', generate {num_suggestions} unique suggestions for the next interaction.
                    Each suggestion should offer a different perspective or idea related to the main content. Ensure that each suggestion is brief and in the same language as the main content message (max 6 words and do not use ", or ." at the end).
                    """

        # Format the suggestions as clickable links in HTML
        suggestions_html = "After generating the suggestions, please format them as follows: " + \
                       "<hr><div> <b>Suggestions: </b>" + ", ".join([f'<a href="javascript:void(0);" class="suggestion"><i>{{suggestion_{i+1}}}</i></a>' for i in range(num_suggestions)]) + "</div>"
        
        # Append the HTML-formatted suggestions to the prompt
        prompt += f"\n{suggestions_html}"

        # Request the LLM to generate suggestions based on the prompt
        suggestions = cat.llm(prompt, stream=True)

        #TO_DO: add suggestions in a new property
        # Append the generated suggestions to the message content
        message['content'] += suggestions

    return message