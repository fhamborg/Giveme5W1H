class Configuration:
    """
    These flags can be used to change the giveme5w configuration
    """
    __config = {
        "candidate": {
            "text": True,  # Concatenated 'originalText' from nlpToken
            "nlpIndexSentence": True,  # determined by CoreNlp: include index of sentence
            "parts": {
                "nlpToken": True  # determined by CoreNlp: Tag
            },
            "score": True  # determined by Giveme5W: calculated score for this candidate
        },
        "label": True,  # This repeating information is useful for template engines
        "onlyTopCandidate": True,  # Return only the  Candidate with the best score per question
        "Giveme5W-runtime-resources": './runtime-resources/'  # Runtime directory
    }

    @classmethod
    def get(cls):
        return cls.__config;
