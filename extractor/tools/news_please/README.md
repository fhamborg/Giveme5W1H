# news_please tools
- writer can only be used together with this reader, all data in the origin files are taken over to the output file.
- the news-please format is extended by a literal 'five5oneH' to follow the .js object naming conventions (should not start with numbers)
- filename will be recreated as the SHA224 value of the url to avoid collision and get a unique identifier for each articel
- 'five5oneH' can also be preexisting and hold the golden-standart under annotated
- output prefers allway objects over arrays to be as flexible as possible.  

```javascript
"fiveWoneH": {
    "how": {
      "annotated": [],
      "extracted": []
    },
    "what": {
      "annotated": [
        { text: "stands by decision not to charge Clinton after review of additional emails" },
        { text: "stands by decision not to charge Clinton after review of additional emails" }
      ],
      "extracted": [
        {
          "score": 1.0,
          "phrases": [
            { phrase: "delivered", tag: "VBD"},
            { phrase: "delivered", tag: "VBD"} 
            ]
        }
      ]
    }
}
```