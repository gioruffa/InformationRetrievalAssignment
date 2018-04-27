# Information Retrieval Assignment
## Profile Based Retrieval
### Giorgio Ruffa - Federico Ungolo

## Assignment
The student is required to create a method based in the space vector model to deliver small text snippets to different users depending on their profile. For instance, let us suppose that we have 4 different users: the first one being interested in politics and soccer, the second in music and films, the third in cars and politics and the fourth in soccer alone. An incoming document targeted at politics should be delivered to users 1 and 3, while a document on soccer should be delivered to users 1 and 4. Students must submit a written report no longer than 15 pages explaining the method used to encode both the documents and the user profiles, together with the algorithm used to process the queries (the more efficient, the better). The written report, which is mandatory will provide a grade of 8 (out of 10 points) maximum. To obtain the maximum grade (10 points out of 10), the student must provide a solid implementation of the proposed method in any programming language. The instructor recommends students to choose the Python programming language or Java since there are plenty of useful code snippets out there to help implement the required functionalities. If the student decides to submit the optional part, all the required stuff to execute the program must be provided.

## Workflow and implementation
The program will clean the corpus (removal of stopwords, lowering and tokenizing) and then build a tfidf model.
To each corpus document is associated a category, identified by the letter in the file title as follows:

* p: pizza
* f: fashion
* m: cars 

The user profiles are generated randomly and stored in a pandas dataframe.

The incoming text snippet is preprocessed in the same way and represented in the tfidf model as a query. 
Then the cosine distance with all the documents is calculated. The closest document is picked to determine the category
of the query (pizza, fashion or cars), and then delivered to the interested user profiles.


## Usage
Please provide the code snippet as the final argument **ENCLOSED IN HYPHENS** (see the following example)
```bash
$> python ir.py -c corpus "New pizzeria opens in New York"
Generating user profiles
Users profiles are:
       cars  fashion  pizza
users                      
0         0        1      0
1         0        0      1
2         1        1      0
3         1        1      0
4         0        0      1

The text snippet is: 
'New pizzeria opens in New York'

The closest document to the text snippet belongs to the category "pizza" and its content is:
('Sausage-Broccoli Rabe Make New York-Style Pizza (No. 6) with only 1 1/2 cups '
 'mozzarella. Add 2 crumbled raw sausages. Bake until just crisp, then top '
 'with 4 ounces bocconcini, sauteed broccoli rabe and jarred cherry peppers. '
 'Bake until the cheese melts. Stuffed Crust Make New York-Style Pizza (No. '
 '6), but before topping, place 8 string-cheese sticks along the edge and fold '
 'the dough over. Brush the stuffed crust with olive oil and sprinkle with '
 'dried oregano. Meatball Pizza\n')

The user id interested in the topic pizza are: [1 4]
```

