import tiktoken

def override_tokenizer() -> None:
    """
    Registers tiktoken as the tokenizer by monkey-patching LangChain's default tokenizer.
    """
    tiktoken_encoder = tiktoken.get_encoding("cl100k_base")

    # Monkey patch the tokenizer to use tiktoken
    import langchain_core.language_models.base
    langchain_core.language_models.base._get_token_ids_default_method = lambda text: tiktoken_encoder.encode(text, disallowed_special=())