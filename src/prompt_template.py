from langchain_core.prompts import PromptTemplate

def get_prompt_template() -> PromptTemplate:
    """
    Returns a PromptTemplate object with a specific template for summarization tasks.
    The template includes instructions for the model to follow when generating a summary.

    :returns:
        PromptTemplate: A PromptTemplate object configured for summarization tasks.
    """
    template: str = """
    <INSTRUCTIONS>
    - You are a helpful summarization assistant. Your task is to summarize the text below in a concise and clear manner.
    - The summary should capture the main points and key details of the text while maintaining its original meaning.
    - Please avoid adding any personal opinions or interpretations.
    - The summary should be in English.
    </INSTRUCTIONS>

    <TEXT>
    {text}
    </TEXT>
    """

    return PromptTemplate(
        input_variables=["text"],
        template=template,
        validate_template=True,
    )