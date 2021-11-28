Objetivo:

Utilizar o algoritmo word2vec para criar modelos de linguagem.

O que fazer:
- usar skip-gram e CBOW
- variar dimensões (100, 300, 500)
- variar janela (3,4,5,10)

Resultados
- comparar os diferentes modelos e criar gráficos


evaluate_word_analogies
https://www.computersciencemaster.com.br/como-implementar-o-word2vec-em-python/#:~:text=Implementa%C3%A7%C3%A3o%20do%20word2vec%20em%20Python,processamento%20e%20cria%C3%A7%C3%A3o%20do%20modelo.&text=Podemos%20perceber%20que%20a%20palavra,causes%E2%80%9D%2C%20%E2%80%9Cenergy%E2%80%9D.

https://www.youtube.com/watch?v=T9mZvI8adqI

https://www.youtube.com/watch?v=Q2NtCcqmIww

https://www.youtube.com/watch?v=Z1VsHYcNXDI

https://www.youtube.com/watch?v=64qSgA66P-8

Avaliação
https://stackoverflow.com/questions/32759712/how-to-find-the-closest-word-to-a-vector-using-word2vec

>>> model.most_similar(positive=['woman', 'king'], negative=['man'])
[('queen', 0.50882536), ...]

loss
https://www.youtube.com/watch?v=MtM9QrCjuK4