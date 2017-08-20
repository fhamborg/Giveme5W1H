class Configuration:
    __config = {
        "information": {
            "nlpIndexSentence": False,
            "candidate": {
                "nlpTag": False
                }
           },
        "onlyTopCandidate": False,
        "enhancer": {}
        }

    @classmethod
    def get(cls):
        return cls.__config;