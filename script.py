from urllib.request import urlopen
from contextlib import suppress
import json
import numpy as np

#esta biblioteca precisa estar na versão 3.4 ou mais
#se o script nao funcionar executar seguinte comando 
#!pip install seaborn --upgrade matplotlib
import matplotlib.pyplot as plt


# pega os dados do json
def getJsonData(url):
    response = urlopen(url)
    data_json = json.loads(response.read())
    # print(data_json)
    return data_json
  
# itera sobre o json formatando os dados e
# mapeando probes_distributions como {probe_id: [
#     {server1: qtd de vezes acionada},
#     {server2: qtd de vezes acionada},
#     ...
#     {servern: qtd de vezes acionada}
# ]}

def formatJsonDataH(data_json):
    probes_distributions = {}

    for measurement in data_json:
        id = measurement['prb_id']
        with suppress(KeyError):
            result = measurement['result']['answers'][0]['RDATA'][0]
            with suppress(IndexError):
                local = result.split('.')[1]
                if len(local) == 3:
                    if(id in probes_distributions.keys()):
                        if(local in probes_distributions[id].keys()):
                            probes_distributions[id][local] += 1
                        else:
                            probes_distributions[id][local] = 1
                    else:
                        probes_distributions[id] = {}
                        probes_distributions[id][local] = 1
    return probes_distributions


# itera sobre o json formatando os dados e
# mapeando probes_distributions como {probe_id: [
#     {server1: qtd de vezes acionada},
#     {server2: qtd de vezes acionada},
#     ...
#     {servern: qtd de vezes acionada}
# ]}

def formatJsonDataK(data_json):
    probes_distributions = {}

    for measurement in data_json:
        id = measurement['prb_id']
        with suppress(KeyError):
            result = measurement['result']['answers'][0]['RDATA'][0]
            with suppress(IndexError):
                local = result.split('.')[1].split('-')[1]
                if len(local) == 3:
                    if(id in probes_distributions.keys()):
                        if(local in probes_distributions[id].keys()):
                            probes_distributions[id][local] += 1
                        else:
                            probes_distributions[id][local] = 1
                    else:
                        probes_distributions[id] = {}
                        probes_distributions[id][local] = 1
    return probes_distributions


#pega os dados formatados do json e coloca em um array do tipo {local:qtd}

def formatDataFromBarChart(probes_distributions):

    probes_by_local = {}
    local_by_probes = {}
    locals = set()
    #itera sobre probes_distributions para pegar o server com maior numero de requisiões para cada probe id
    for probe, locals_probe in probes_distributions.items():
        maior = 0
        for local, quantity in locals_probe.items():
            if(quantity > maior):
                maior = quantity
                probes_by_local[probe] = local
        locals.add(probes_by_local[probe])

    for probe, local in probes_by_local.items():
        if(local in local_by_probes):
            local_by_probes[local].append(probe)
        else:
            local_by_probes[local] = []
            local_by_probes[local].append(probe)

    quantity_by_local = {}
    quantity_by_local['outros'] = 0
    for local in local_by_probes.keys():
        if len(local_by_probes[local]) >= 40:
            quantity_by_local[local] = len(local_by_probes[local])
        else:
            quantity_by_local['outros'] += len(local_by_probes[local])

    return quantity_by_local


def plotBarChart(quantity_by_local, title):
    quantity_by_local = dict(sorted(quantity_by_local.items(), key=lambda item: item[1], reverse=True))
    print(quantity_by_local)
    fig = plt.figure()
    ax = fig.add_axes([0,0,3,1])
    local_keys = list(quantity_by_local.keys())
    x_data = np.array(local_keys)

    local_values = list(quantity_by_local.values())
    y_data = np.array(local_values)
    ax.bar(x_data ,y_data)
    ax.bar_label(ax.bar(x_data ,y_data), label_type='edge')

    plt.ylabel('Quantidade de Probes')
    plt.xlabel('Local do Servidor')
    plt.title(title)
    plt.show()


#URL da medição ID 11315
#Servidor H
#IPV6
#start = GMT: Wednesday, 20 April 2022 15:00:00
#stop = GMT: Wednesday, 20 April 2022 15:43:20
url = "https://atlas.ripe.net/api/v2/measurements/11315/results/?start=1650466800&stop=1650469400&format=json"

# esse é pra teste
# url = "https://atlas.ripe.net/api/v2/measurements/11315/results/?start=1650466800&stop=1650466800&format=json"

data_json = getJsonData(url)
probes_distributions = formatJsonDataH(data_json)
quantity_by_local = formatDataFromBarChart(probes_distributions)
plotBarChart(quantity_by_local, 'Servidor H IPV6')



#URL da medição ID 10315
#Servidor H
#IPV4
#start = GMT: Wednesday, 20 April 2022 15:00:00
#stop = GMT: Wednesday, 20 April 2022 15:43:20
url = "https://atlas.ripe.net/api/v2/measurements/10315/results/?start=1650466800&stop=1650469400&format=json"
data_json = getJsonData(url)
probes_distributions = formatJsonDataH(data_json)
quantity_by_local = formatDataFromBarChart(probes_distributions)
plotBarChart(quantity_by_local, 'Servidor H IPV4')


#URL da medição ID 11301
#Servidor K
#IPV6
#start = GMT: Wednesday, 20 April 2022 15:00:00
#stop = GMT: Wednesday, 20 April 2022 15:43:20
url = "https://atlas.ripe.net/api/v2/measurements/11301/results/?start=1650466800&stop=1650469400&format=json"
data_json = getJsonData(url)
probes_distributions = formatJsonDataK(data_json)
quantity_by_local = formatDataFromBarChart(probes_distributions)
plotBarChart(quantity_by_local, 'Servidor K IPV6')


#URL da medição ID 10301
#Servidor K
#IPV4
#start = GMT: Wednesday, 20 April 2022 15:00:00
#stop = GMT: Wednesday, 20 April 2022 15:43:20
url = "https://atlas.ripe.net/api/v2/measurements/10301/results/?start=1650466800&stop=1650469400&format=json"
data_json = getJsonData(url)
probes_distributions = formatJsonDataK(data_json)
quantity_by_local = formatDataFromBarChart(probes_distributions)
plotBarChart(quantity_by_local, 'Servidor K IPV4')