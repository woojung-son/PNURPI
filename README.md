**2020 graduation Piece of Pusan National University**
- Subject : Developing model which improves performance better than previous researches using RNA Protein Interaction(RPI) Database datasets.
- Team No. : 6
- Team Name : `Could we graduate ..?`
- Team Member : 201724545 이지현, 201729127 박성아, 201724493 Woojung Son
- Visualization Server : http://52.79.184.82:5601/app/kibana#/dashboard/4d687850-fe37-11ea-9a80-5b5ed9a16699 -> Dashboard (valid until end of Oct. 2020)

***RNA Protein Interaction(RPI) Database***
# **RPIntDB**
![RNA Protein 결합 예시](http://swift-lang.org/case_studies/images/rna.png)

The database in order to check whether a certain RNA and protein molecules can be interacted or not. We can use it as developing machine learning model to solve classification problem of them.

## About our project
We use ensemble model as a classifier which bundles RandomForest, Support Vector Machine and several other classifiers up with soft voting.

We evaluate our model using accuracy (`Acc`), sensitivity (`Sn`), specificity (`Sp`), precision (`Pre`), Matthews correlation coefficient (`MCC`), and `AUC` (the area under the receiver operating characteristic curve (ROC).

You can see the best performance of our projects on `best_output.json` since `save_best_output.py` file tracks the best result when we get the highest Accuracy of each dataset. It is used to visualize the result of performance using AWS, ElasticSearch, Kibana.

We did visualize using AWS EC2 server and ElasticSearch, Kibana. The server reads `best_output.json` file and visualize the performances. On the dashboard of kibana, There are vertical bar graphes comparing our accuracy scores with other models made by other research labs, line graphes comparing other kinds of scores with them as well. 

## About the Raw Data
- In `data/` folder, there are files named ending `_pairs` which contain information of pairs of ID of RNAs and proteins with the label. Files named ending in `_pos_pairs` mean what are only consisted of interactable pairs. 
- In `data/sequence` folder, there are files which contain sequence information of RNAs and proteins.
- In `data/struct` folder, there are files which contain struct information of RNAs and proteins, which mean two-dimentional structures of molecules.

## Feature Preprocessing
![reduced Protein에 대한 CTF 예시](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSC2ecLGlTSPxoi4pm3YkgeXdOMi7U5A6CXtKaKrik4kOW1WcPs)

We use improved CTF(Conjoint Triad Feature) in order to preprocess both sequence and struct data of RNAs and proteins. 

CTF(Conjoint Triad Feature) is the way of preprocessing DNA-like data usually used in Bioinformatics. It makes several patterns consisted of elements of RNA and reduced protein with the maximum of 3 alphabetic-digits and uses them as a features. Improved CTF uses one more digit to express patterns. 

### Usage of making preprocessed file
`make_preprocessed_file.ipynb` file preprocesses sequence and struct data, and produces processed files of each dataset with `.npz` extension.

### Usage of making preprocessed file
`main.ipynb` file reads preprocessed files stored in `npz/` folder. It has binary classifier, splits the whole set into train and test one, returns the scores of performance of model with six criteria.

## References

[1] [https://github.com/Pengeace/RPITER](https://github.com/Pengeace/RPITER)
[2] PEDREGOSA, Fabian, et al. Scikit-learn: Machine learning in Python. _Journal of machine learning research_, 2011, 12.Oct: 2825-2830.
