![](https://img.shields.io/github/languages/top/aseidelo/NLPolitica)
![](https://img.shields.io/github/languages/code-size/aseidelo/NLPolitica)
![](https://img.shields.io/apm/l/vim-mode)


# NLPolitica

NLP applied for augmented democracy in Portugal's parliament activity.

We process the minutes of the **portuguese official Journal of the Republic**, which includes all the information produced and exchanged in the parliamentarian sessions, in order to:
 
 1 - analyze and make sense of massive and complex amounts of data produced in the legislative body;

 2 - extract knowledge and sentiments related to anti-corruption political discourse and legislative initiatives;
 
 3 - create analytics and dashboards for citizens and organizations (e.g., press/journalists investigative authorities, researchers) to track and monitor the (anti)corruption ideas, initiatives and behaviors parliamentarians and their political parties produce, initiate and/or support. 

## Usage

Each package on ```src/``` folder is a self-contained step of the project. Please reffer to each packages README.md description ```src/<PKG_NAME>/README.md>``` and ipython notebooks at ```notebooks/<PKG_NAME>/``` for usage examples.

## Recent work

Currently we are working on models that can, accurately, define what is a continuity or an interruption in dialogue in a specific part of the minutes called "Declarações Políticas" in witch the political parties may initiate discussions about their interrest.

These part of the minutes don't necessarely have a continuous subject in discussion and the Chairman is who defines how far the discussion can goes on. So our main objective is to determine if, given a pronunciation of the Chairman, we have a interruption or an continuity of the subject in discussion.

## Our results

Currently working...

|Model|Lemmatization|Tokenization|Embedding|Accuracy|F1-Score|Precision|Recall|
|---|---|---|---|---|---|---|---|
|Random Florest|Yes|No|BERT|---|---|---|---|
|---|---|---|---|---|---|---|---|
|---|---|---|---|---|---|---|---|
|---|---|---|---|---|---|---|---|

## License

Currently using the MIT license avaiable at [this link](https://choosealicense.com/licenses/mit/)

## Cite the source

In case you are fully or partially using our code and corpus, quote us as shown below:

````
@article{AugmentedDemocracy,
   author={Anna Reali, Bruno Veloso, Rodrigo Gerber, Alexandre Alcoforato, André Seidel, Thomas Ferraz, Fernanda Kanazawa, Arthur, Enzo Bustos},
   title={~Título do nosso paper~ Augmented Democracy},
   journal={BRACIS 2021},
   volume={},
   year=2021,
   pages={~15~},
   url={~www.url_do_artigo.com~},
}
````