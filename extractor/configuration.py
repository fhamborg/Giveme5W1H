class Configuration:

    __config = {
        "information": {
            "nlpIndexSentence": False,
            "candidate": {
                "nlpTag": False
                }
           },
        "onlyTopCandidate": False,
        "enhancements":
                    {
                        "Giveme5W_enhancer":  { # Thats the module name
                            "enabled": False,
                            "mainModule": "enhancement", # thats the .py file, must contain a class name Enhancement
                            "config": {} # This will passed to the constructor
                        }
                    }

        }

    @classmethod
    def get(cls):
        return cls.__config;