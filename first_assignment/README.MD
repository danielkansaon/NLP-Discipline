# Objetivo:

Utilizar o algoritmo word2vec para criar modelos de linguagem. A ideia é testar diversos parametros do algoritmo, discutindo os resultados.

### Parâmetros Testados
- Windows Size (2, 4, 6, 8, 10)
- Dimensão (100, 300, 500)
- Arquitetura (Skip-Gram e CBOW)
- Epochs (5, 10, 15, 20)
- Base de Dados (Dataset 1, Dataset 2, Dataset 3) - 

### Informações e detalhes sobre a implementação:
- Desenvolvido em Python 3.6.9;
- Foi utilizada a versão Word2vec implementada pela biblioteca **gensim.models**;
- A base de dados **text8** foi utilizada para treinamento. http://mattmahoney.net/dc/text8.zip
- Foi feita avaliação intrínseca de cada modelo gerado, através da distância entre as palavras;

O notebook desenvolvido (fs1_word2vec_notebook) contém todos os códigos. 

# Links utilizados para consulta

evaluate_word_analogies
https://www.computersciencemaster.com.br/como-implementar-o-word2vec-em-python/#:~:text=Implementa%C3%A7%C3%A3o%20do%20word2vec%20em%20Python,processamento%20e%20cria%C3%A7%C3%A3o%20do%20modelo.&text=Podemos%20perceber%20que%20a%20palavra,causes%E2%80%9D%2C%20%E2%80%9Cenergy%E2%80%9D.

https://www.youtube.com/watch?v=T9mZvI8adqI
./ distance vectors.bin

https://www.youtube.com/watch?v=Q2NtCcqmIww

https://www.youtube.com/watch?v=Z1VsHYcNXDI

https://www.youtube.com/watch?v=64qSgA66P-8

https://stackoverflow.com/questions/32759712/how-to-find-the-closest-word-to-a-vector-using-word2vec

https://www.youtube.com/watch?v=MtM9QrCjuK4

https://www.kaggle.com/rootuser/worldnews-on-reddit


