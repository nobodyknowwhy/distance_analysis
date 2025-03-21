REFERENCE_WORDS = ["else", "but", "also", "then", "although", "thus", "therefore", "therefore", "however", "furthermore", "moreover", "additionally",
    "consequently", "similarly", "meanwhile", "while", "since", "unless"]
TRANSITIONAL_WORDS = [
   "on the other hand", "in contrast", "not only", "in addition", "for instance", "in my opinion", "for example", "but also", "to illustrate", "what's more", "in comparison"
]

t_t = ["who", "whom", "whose", "which", "when", "whether", "what", "where", "how", "why", "that"]

text1 = "You will act as an English learner.  Now you need to revise the given article to match the corresponding score of the article. There are a total of 5 scores (1-5) for the given article.  Specifically, You need to modify some words or sentences according to the requirement:"

text2 = "including some long difficult words, rare words to enrich the vocabulary of the article"

text3= "Reduce the use of connective words and advanced connective sentences"

text4 = "Add much grammar errors, such as some spelling errors, subject-verb agreement errors, improper use of tense errors, misuse of articles. But make sure they still exist,"

text5 = "Remember, you can only modify the vocabulary/connective structure/grammar error of the essay, the essay with the score {score} is followed: {text}"
print('\\ '.join(text5.split(' ')))