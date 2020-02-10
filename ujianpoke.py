from flask import Flask, render_template, request
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('pokemon.csv')
def Generation (x):
    if x['Generation'] == 1:
        return 'one'
    elif x['Generation'] == 2:
        return 'two'
    elif x['Generation'] == 3:
        return 'three'
    elif x['Generation'] == 4:
        return 'four'
    elif x['Generation'] == 5:
        return 'five'
    elif x['Generation'] == 6:
        return 'six'

dfpoke = df[['Name', 'Type 1', 'Generation', 'Legendary']]
dfpoke['name'] = df['Name'].apply(lambda x: x.lower())
dfpoke['Legendary'] = df['Legendary'].apply(lambda x: 'Legendary' if True else 'Not Legend')
dfpoke['Generation2'] = df.apply(Generation, axis =1)
dfpoke['merge'] = dfpoke['Type 1'] +',' + dfpoke['Generation2'] + ',' + dfpoke ['Legendary']
ext = CountVectorizer(
    tokenizer = lambda x: x.split(','))
factors = ext.fit_transform(dfpoke['merge'])
cosscore = cosine_similarity(factors)


app = Flask (__name__)

@app.route ('/', methods = ['POST', 'GET'])
def home():
    return render_template('pokehome.html')

@app.route('/hasil', methods = ['POST', 'GET'])
def hasil():
    bisa = True
    if request.method == "POST":
        input = request.form
        exist = input['pokename'].lower() in list(dfpoke['name'])
        if exist:
            favoritepoke = input['pokename']
            indexpoke = dfpoke[dfpoke['name'] == favoritepoke.lower()].index[0]
            pokesama = list(enumerate (cosscore [indexpoke]))
            pokesama = sorted (pokesama, key= lambda x:x[1], reverse=True)
            indexpokesama = []
            jumlah = 0
            for i in pokesama:
                if jumlah < 6:
                    if i[0] != indexpoke:
                        if len(dfpoke['Name'].iloc[i[0]].split(' ')) == 1: # ditambahkan if agar tidak merekomendasikan pokemon yg namanya lebih dari satu kata karena di pokeapi tidak bisa disearch gambarnya
                            indexpokesama.append(i[0])
                            jumlah += 1
            
            dfpokesama = pd.DataFrame(columns = list(dfpoke.columns))
            for i in range(6):
                dfpokesama = pd.concat([dfpokesama, dfpoke.iloc[[indexpokesama[i]]]])

            ## untuk dikirim ke html
            favoritepoke = favoritepoke
            poketype = dfpoke[dfpoke['name'] == favoritepoke.lower()]['Type 1']
            pokegen = dfpoke[dfpoke['name'] == favoritepoke.lower()]['Generation']
            pokelegend = dfpoke[dfpoke['name'] == favoritepoke.lower()]['Legendary']

            p1name = dfpokesama['Name'].iloc[0]
            p1type = dfpokesama['Type 1'].iloc[0]
            p1gen = dfpokesama['Generation'].iloc[0]
            p1legend = dfpokesama['Legendary'].iloc[0]

            p2name = dfpokesama['Name'].iloc[1]
            p2type = dfpokesama['Type 1'].iloc[1]
            p2gen = dfpokesama['Generation'].iloc[1]
            p2legend = dfpokesama['Legendary'].iloc[1]

            p3name = dfpokesama['Name'].iloc[2]
            p3type = dfpokesama['Type 1'].iloc[2]
            p3gen = dfpokesama['Generation'].iloc[2]
            p3legend = dfpokesama['Legendary'].iloc[2]

            p4name = dfpokesama['Name'].iloc[3]
            p4type = dfpokesama['Type 1'].iloc[3]
            p4gen = dfpokesama['Generation'].iloc[3]
            p4legend = dfpokesama['Legendary'].iloc[3]


            p5name = dfpokesama['Name'].iloc[4]
            p5type = dfpokesama['Type 1'].iloc[4]
            p5gen = dfpokesama['Generation'].iloc[4]
            p5legend = dfpokesama['Legendary'].iloc[4]

            p6name = dfpokesama['Name'].iloc[5]
            p6type = dfpokesama['Type 1'].iloc[5]
            p6gen = dfpokesama['Generation'].iloc[5]
            p6legend = dfpokesama['Legendary'].iloc[5]

            url0 = f"https://pokeapi.co/api/v2/pokemon/{favoritepoke.lower()}"    
            url1 = f"https://pokeapi.co/api/v2/pokemon/{p1name.lower()}"
            url2 = f"https://pokeapi.co/api/v2/pokemon/{p2name.lower()}"
            url3 = f"https://pokeapi.co/api/v2/pokemon/{p3name.lower()}"
            url4 = f"https://pokeapi.co/api/v2/pokemon/{p4name.lower()}"
            url5 = f"https://pokeapi.co/api/v2/pokemon/{p5name.lower()}"
            url6 = f"https://pokeapi.co/api/v2/pokemon/{p6name.lower()}"

            datapi0 = requests.get(url0)
            datapi0 = datapi0.json()
            datapi1 = requests.get(url1)
            datapi1 = datapi1.json()
            datapi2 = requests.get(url2)
            datapi2 = datapi2.json()
            datapi3 = requests.get(url3)
            datapi3 = datapi3.json()
            datapi4 = requests.get(url4)
            datapi4 = datapi4.json()
            datapi5 = requests.get(url5)
            datapi5 = datapi5.json()
            datapi6 = requests.get(url6)
            datapi6 = datapi6.json()

            urlp0 = datapi0['sprites']['front_default']
            urlp1 = datapi1['sprites']['front_default']
            urlp2 = datapi2['sprites']['front_default']
            urlp3 = datapi3['sprites']['front_default']
            urlp4 = datapi4['sprites']['front_default']
            urlp5 = datapi5['sprites']['front_default']
            urlp6 = datapi6['sprites']['front_default']
            
            
            bisa=True
        else:
            bisa=False
    if bisa: 
        return render_template('hasil.html', favpoke = dfpoke[dfpoke['name'] == favoritepoke.lower()]['Name'], 
        poketype = dfpoke[dfpoke['name'] == favoritepoke.lower()]['Type 1'],
        pokegen = dfpoke[dfpoke['name'] == favoritepoke.lower()]['Generation'],
        pokelegend = dfpoke[dfpoke['name'] == favoritepoke.lower()]['Legendary'],
        p1name = dfpokesama['Name'].iloc[0],
        p1type = dfpokesama['Type 1'].iloc[0],
        p1gen = dfpokesama['Generation'].iloc[0],
        p1legend = dfpokesama['Legendary'].iloc[0],
        p2name = dfpokesama['Name'].iloc[1],
        p2type = dfpokesama['Type 1'].iloc[1],
        p2gen = dfpokesama['Generation'].iloc[1],
        p2legend = dfpokesama['Legendary'].iloc[1],
        p3name = dfpokesama['Name'].iloc[2],
        p3type = dfpokesama['Type 1'].iloc[2],
        p3gen = dfpokesama['Generation'].iloc[2],
        p3legend = dfpokesama['Legendary'].iloc[2],
        p4name = dfpokesama['Name'].iloc[3],
        p4type = dfpokesama['Type 1'].iloc[3],
        p4gen = dfpokesama['Generation'].iloc[3],
        p4legend = dfpokesama['Legendary'].iloc[3],
        p5name = dfpokesama['Name'].iloc[4],
        p5type = dfpokesama['Type 1'].iloc[4],
        p5gen = dfpokesama['Generation'].iloc[4],
        p5legend = dfpokesama['Legendary'].iloc[4],
        p6name = dfpokesama['Name'].iloc[5],
        p6type = dfpokesama['Type 1'].iloc[5],
        p6gen = dfpokesama['Generation'].iloc[5],
        p6legend = dfpokesama['Legendary'].iloc[5],
        urlp0 = urlp0, urlp1 = urlp1, urlp2 = urlp2, urlp3 = urlp3, urlp4 = urlp4, urlp5 = urlp5, urlp6=urlp6)
    else: 
        return render_template('error.html')
    


if __name__== '__main__':
    app.run(debug=True, port=5000)



    

