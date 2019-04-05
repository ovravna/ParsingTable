# ParsingTable

Give me grammar!

Like this:

        E -> T E'
        E' -> + T E' | €
        T -> F T'
        T' -> * F T' | €
        F -> ( E ) | id

`€` is empty terminal.

Use space `' '` as seperator in production
Seperate productions with pipe `'|'` or with different arrow-productions
Any string on the left side of `->` is a nonterminal
Any non-nonterminal on the rightside of `->` is a terminal

Third argument is style of table. Default: fancy_grid
Valid options are:
plain simple github grid fancy_grid pipe orgtbl jira presto psql rst
mediawiki moinmoin youtrack html latex latex_raw latex_booktabs textile

#### Run after installing requirements:
```
$ python parsing_table.py grammar.txt 
```
#### Run executable on Linux:
```
$ ./parsing_table grammar.txt
```

### Result:
```
╒═════════════╤══════════╤═══════════╤═══════════╤══════════╤════════╤════════╤═════════╤════════════╕
│ NON -       │ id       │ +         │ *         │ (        │ )      │ $      │ FIRST   │ FOLLOW     │
│ TERMINALS   │          │           │           │          │        │        │         │            │
╞═════════════╪══════════╪═══════════╪═══════════╪══════════╪════════╪════════╪═════════╪════════════╡
│ E           │ E  → TE' │           │           │ E  → TE' │        │        │ (  id   │ $  )       │
├─────────────┼──────────┼───────────┼───────────┼──────────┼────────┼────────┼─────────┼────────────┤
│ E'          │          │ E' → +TE' │           │          │ E' → ε │ E' → ε │ ε  +    │ $  )       │
├─────────────┼──────────┼───────────┼───────────┼──────────┼────────┼────────┼─────────┼────────────┤
│ T           │ T  → FT' │           │           │ T  → FT' │        │        │ (  id   │ $  )  +    │
├─────────────┼──────────┼───────────┼───────────┼──────────┼────────┼────────┼─────────┼────────────┤
│ T'          │          │ T' → ε    │ T' → *FT' │          │ T' → ε │ T' → ε │ ε  *    │ $  )  +    │
├─────────────┼──────────┼───────────┼───────────┼──────────┼────────┼────────┼─────────┼────────────┤
│ F           │ F  → id  │           │           │ F  → (E) │        │        │ (  id   │ +  $  )  * │
╘═════════════╧══════════╧═══════════╧═══════════╧══════════╧════════╧════════╧═════════╧════════════╛
```

![Parsing Table](https://i.gyazo.com/2c7c0f2e7c0655596976717a8c46c9f0.png)
![Parsing Table Latex](https://i.gyazo.com/0c50a457010fe8a9563742e7aff8ad0a.png)
