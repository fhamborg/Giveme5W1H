class Configuration:
    __config = {
        "candidate": {
            "nlpIndexSentence": True,  # determined by CoreNlp: include index of sentence
            "part": {
                "nlpTag": True  # determined by CoreNlp: Tag
            },
            "score": True  # determined by Giveme5W: calculated score for this candidate
        },
        "label": True,  # This repeating information is useful for template engines
        "onlyTopCandidate": False, # Return only the determined Candidate with the best score per question
        "Giveme5W-runtime-resources": './../../Giveme5w-runtime-resources/' # Runtime directory
    }

    @classmethod
    def get(cls):
        return cls.__config;

        #  "enhancements":
        #  {
        #      "Giveme5W_enhancer": {  # Thats the module name
        #          "enabled": False,
        #          "mainModule": "enhancement",  # thats the .py file, must contain a class name Enhancement
        #          "config": {}  # This will passed to the constructor
        #      }
        #  }
