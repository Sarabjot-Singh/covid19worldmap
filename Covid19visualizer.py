def get_data():
    import requests
    response = requests.get('https://opendata.ecdc.europa.eu/covid19/casedistribution/json/')
    jsonobj = response.json()
    return jsonobj


def makemap(df_dict):
    import pandas as pd
    import plotly
    df = pd.DataFrame(df_dict)
    country = df['country']
    countrycodes = df['code']
    cases = df['cases']
    print(df)

    data = [
        dict(
            type='choropleth',
            colorscale='Rainbow',
            locations=countrycodes,
            z = cases,
            text=country,

            colorbar=dict(
                title= 'Cases',
                titlefont=dict(size=18))
        )
    ]

    layout = dict(
        title='Covid 19 Cases',
        titlefont=dict(size=40),
        geo=dict(
            showframe=True,
            showcoastline=True,
            projection=dict(type='orthographic')
        )
    )

    fig = dict(data=data,
               layout=layout)
    plotly.offline.plot(fig,validate=False,filename='world.html')


if __name__ == '__main__':
    import datetime
    df_dict = {}
    country = []
    countrycode = []
    numberofcases = []
    tc = 0
    i = -1
    data = get_data()
    records = data['records']
    firstrecord = records[0]
    last_recorded_date = datetime.date(int(firstrecord['year']),int(firstrecord['month']), int(firstrecord['day']))
    todaydate = datetime.date.today()

    if(todaydate == datetime.date(int(firstrecord['year']), int(firstrecord['month']), int(firstrecord['day']))):
        for record in records:
            if(todaydate == datetime.date(int(record['year']), int(record['month']), int(record['day']))):
                country.append(record['countriesAndTerritories'])
                numberofcases.append(int(record['cases']))
                tc = int(record['cases'])
                countrycode.append(record['countryterritoryCode'])
                i += 1

            else:
                tc += int(record['cases'])
                numberofcases[i] = tc
    else:
        ch = input('DataFrame is yet not updated do you want to see last updated results (y/n):')
        if(ch == 'y'):
            todaydate = last_recorded_date
            for record in records:
                if(todaydate == datetime.date(int(record['year']), int(record['month']), int(record['day']))):
                    country.append(record['countriesAndTerritories'])
                    numberofcases.append(int(record['cases']))
                    tc = int(record['cases'])
                    countrycode.append(record['countryterritoryCode'])
                    i += 1
                else:
                    tc += int(record['cases'])
                    numberofcases[i] = tc
        else:
            exit()

    df_dict =  {
        'country':country,
        'code':countrycode,
        'cases':numberofcases
    }

    makemap(df_dict)
