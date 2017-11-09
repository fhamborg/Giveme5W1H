This is the original dataset, before conversation and without how annotation


- ICR-annotations.csv is a "one to one" port of the original excel file tab 'golden_standard'
- annotation.json are the original annotations as provided by the previous work
- annotation_new.json is a new extract from ICR-annotations.csv, this is removing copy paste errors within annotation.json and includes the "how" annotations

- Reproduce results:
- run generate_annotations => annotation_new.json
- run converter.py => writes in output