#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import FloatImage


# In[ ]:


st.set_page_config(layout='wide')
st.title('Dashboard van regionale luchthavens in Nederland')
st.write("""***""")

page_names = ['Hoofdmenu', 'Luchthavens op de kaart', 'Air Traffic Movements', 'Commercieel & Niet-Commercieel', 'Soorten vluchten', 'Conclusies', 'Data cleaning & analyse']
page = st.sidebar.radio('Menu', page_names, index=0)

if page == 'Hoofdmenu':
    ###HET HOOFDMENU MET TEKST###
    st.subheader('Een kijk op de regionale luchtvaart')
    st.write('Veelal wordt er in de luchtvaart gekeken naar de grote spelers, zoals Amsterdam Airport Schiphol of Eindhoven Airport als het gaat om air traffic movements of bepaalde type vluchten. Maar wat zijn de cijfers bij de kleinere regionale luchthavens? Dit dashboard geeft inzicht in de cijfers van 10 regionale luchthavens in Nederland, van periode 2010 tot 2020. Wat zijn de grote spelers in de regionale Nederlandse luchtvaart?')
    st.write('Dit Dashboard is gemaakt met data verkregen van de "Luchtvaart; vliegtuigbewegingen op kleine luchthavens" dataset afkomstig van het CBS (Centraal Bureau voor Statistiek) Statline platform. Deze dataset is te verkrijgen via: https://opendata.cbs.nl/#/CBS/nl/dataset/60058ned/table?ts=1638476819567')
    st.write("""***""")
    st.write('Gemaakt door: Toine Smulders (500800028)')
    st.image('airplane.png', width=None)

elif page == 'Luchthavens op de kaart':
    ###DE INTERACTIEVE KAART###
    st.subheader('10 Nederlandse luchthavens in 2020')
    dfkaart = pd.read_csv('streamlitkaartdf.csv')
    
    def color_producer(type):
        if type == 'Ameland':
            return 'blue'
        if type == 'Budel':
            return 'green'
        if type == 'Drachten':
            return 'orange'
        if type == 'Hoogeveen':
            return 'red'
        if type == 'Hilversum':
            return 'darkviolet'
        if type == 'Lelystad':
            return 'springgreen'
        if type == 'Midden-Zeeland':
            return 'saddlebrown'
        if type == 'Seppe':
            return 'crimson'
        if type == 'Teuge':
            return 'dodgerblue'
        if type == 'Texel':
            return 'magenta'

    def add_categorical_legend(folium_map, title, colors, labels):
        if len(colors) != len(labels):
            raise ValueError("colors and labels must have the same length.")

        color_by_label = dict(zip(labels, colors))

        legend_categories = ""     
        for label, color in color_by_label.items():
            legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"

        legend_html = f"""
        <div id='maplegend' class='maplegend'>
          <div class='legend-title'>{title}</div>
          <div class='legend-scale'>
            <ul class='legend-labels'>
            {legend_categories}
            </ul>
          </div>
        </div>
        """
        script = f"""
            <script type="text/javascript">
            var oneTimeExecution = (function() {{
                        var executed = false;
                        return function() {{
                            if (!executed) {{
                                 var checkExist = setInterval(function() {{
                                           if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                              clearInterval(checkExist);
                                              executed = true;
                                           }}
                                        }}, 100);
                            }}
                        }};
                    }})();
            oneTimeExecution()
            </script>
          """


        css = """

        <style type='text/css'>
          .maplegend {
            z-index:9999;
            float:right;
            background-color: rgba(255, 255, 255, 1);
            border-radius: 5px;
            border: 2px solid #bbb;
            padding: 10px;
            font-size:12px;
            positon: relative;
          }
          .maplegend .legend-title {
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
            }
          .maplegend .legend-scale ul {
            margin: 0;
            margin-bottom: 5px;
            padding: 0;
            float: left;
            list-style: none;
            }
          .maplegend .legend-scale ul li {
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 2px;
            }
          .maplegend ul.legend-labels li span {
            display: block;
            float: left;
            height: 16px;
            width: 30px;
            margin-right: 5px;
            margin-left: 0;
            border: 0px solid #ccc;
            }
          .maplegend .legend-source {
            font-size: 80%;
            color: #777;
            clear: both;
            }
          .maplegend a {
            color: #777;
            }
        </style>
        """

        folium_map.get_root().header.add_child(folium.Element(script + css))

        return folium_map

    url = ("https://puu.sh/ICZBk/5bf19bcb32.png")
    m = folium.Map(location=[52.25526000513539, 5.446195311885129], zoom_start= 7, tiles='CartoDB positron')
    FloatImage(url, bottom=64, left=89).add_to(m)

    #create a marker for each airport
    for row in dfkaart.iterrows():
        row_values = row[1]
        location = [row_values['LAT'], row_values['LON']]

        marker = folium.vector_layers.CircleMarker(location = location, 
                                               radius=row_values['Totaal ATM']/5000, 
                                               popup='<strong>'+ row_values['Luchthaven'] +' airport statistieken'+'</strong>'+'<br>'+'<br>'+
                                               '•Totaal ATM: '+'<strong>'+ str(row_values['Totaal ATM'])+'</strong>' +'<br>'+'<br>'+ 
                                               '•Regio: ' +'<strong>'+ str(row_values['Regio'])+'</strong>' +'<br>'+'<br>'+ 
                                               '•Percentage ATMs v/d Regio: '+'<strong>'+ str(row_values['Percentage v/d Regio']) +'%'+'</strong>'+'<br>'+'<br>'+
                                               '•Percentage ATMs van NL: '+'<strong>'+ str(row_values['Percentage van NL']) +'%'+'</strong>',
                                               tooltip='<strong>'+row_values['Luchthaven']+' Airport'+'</strong>'+'<br>'+'<br>'+ 'Click voor info' , 
                                               color = color_producer(row_values['Luchthaven']), 
                                               fill=True)
        marker.add_to(m)

    m = add_categorical_legend(m, 'Luchthaven',
    colors = ['blue', 'green', 'orange', 'red', 'darkviolet', 'springgreen', 'saddlebrown', 'crimson', 'dodgerblue', 'magenta'],
    labels = ['Ameland', 'Budel', 'Drachten', 'Hoogeveen', 'Hilversum', 'Lelystad', 'Midden-Zeeland', 'Seppe', 'Teuge', 'Texel'])
    
    #m
    folium_static(m, width=1200, height=700)

elif page == 'Air Traffic Movements':
    ###DE TOTAAL AANTAL TRAFFIC MOVEMENT LIJNGRAFIEK EN BARCHART###
    df = pd.read_csv('streamlitdf.csv')

    fig1 = px.line(df,
             x='Jaartal',
             y='Totaal ATM',
             line_group='Luchthaven',
             color='Luchthaven')
    
    fig1.update_layout(title_text='Aantal traffic movements per luchthaven', title_x=0.5, width=800, height=625)          

    fig2 = px.bar(df,
             x='Jaartal',
             y=df['Totaal ATM'],
            color='Regio',barmode='group',
            hover_data={'Jaartal':True,'Luchthaven':True, 'Regio Totaal':True})         

    fig2.update_layout(title_text='Aantal traffic movements per regio', title_x=0.5, width=800, height=625)          
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(fig1)
    with col2:
        st.write(fig2)
        st.info('Regios zijn gemaakt op basis van de provincies waarin de luchthavens zich bevinden')
        

elif page == 'Commercieel & Niet-Commercieel':
    ###DE LIJNGRAFIEKEN BETREFFENDE COMMERCIEEL EN NIET COMMERCIEELE ATMs###
    df = pd.read_csv('streamlitdf.csv')
    
    # Code voor st.multiselect
    Luchthavens = df['Luchthaven'].unique()
    Luchthavens_geselecteerd = st.multiselect('Selecteer Luchthavens', Luchthavens,
                                              default=['Ameland', 'Budel', 'Drachten', 'Hoogeveen', 'Hilversum',
                                                       'Lelystad', 'Midden-Zeeland', 'Seppe', 'Teuge', 'Texel'])
    mask_luchthavens = df['Luchthaven'].isin(Luchthavens_geselecteerd)
    df = df[mask_luchthavens]
    
    fig3 = px.line(df,
             x='Jaartal',
             y='Totaal Commercieel ATM',
             line_group='Luchthaven',
             color='Luchthaven')          

    fig3.update_layout(title_text='Commerciële traffic movements per jaar', title_x=0.5, width=800, height=625)          
    
    fig4 = px.line(df,
             x='Jaartal',
             y='Totaal Non-Commercieel ATM',
             line_group='Luchthaven',
             color='Luchthaven',
             labels= {'Totaal Non-Commercieel ATM': 'Totaal Niet-Commercieel ATM'})         

    fig4.update_layout(title_text='Niet-commerciële traffic movements per jaar', title_x=0.5, width=800, height=625)          
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig3)
    with col2:
        st.plotly_chart(fig4)

elif page == 'Soorten vluchten':
    ###DE BARCHARTS MET SELECTEERBARE LUCHTHAVEN EN TYPE COMMERICIELE OF NIET COMMERCIELE VLUCHT###
    df = pd.read_csv('streamlitdf.csv')
        
    # Code voor st.multiselect
    Luchthavens = df['Luchthaven'].unique()
    Luchthavens_geselecteerd = st.multiselect('Selecteer Luchthavens', Luchthavens, default='Lelystad')
    mask_luchthavens = df['Luchthaven'].isin(Luchthavens_geselecteerd)
    df = df[mask_luchthavens]
    
    fig5 = px.bar(df,
             x='Jaartal',
             y=['C. Geregeld PAX ATM','C. Geregeld Cargo ATM', 'C. Ongeregeld PAX ATM', 'C. Ongeregeld Cargo ATM',
                'C. Brandstof ATM', 'C. Positievlucht ATM', 'C. Taxivlucht ATM',
                'C. Fotovlucht ATM', 'C. Rondvlucht ATM','C. Reclamevlucht ATM', 'C. Spuitvlucht ATM',
                'C. Ambulancevlucht ATM','C. Overig ATM'],
             barmode='group',
             hover_data={'Jaartal':True,'Luchthaven':True},
             labels= {'value': "Aantal Commercieel ATM", 'variable': 'soort ATM'})          

    dropdown_buttons1=[{'label': 'C. Alle types ATM', 'method': 'update','args':[{'visible': [True, True,True,True,True,
                                                                                                   True,True,True,True,
                                                                                              True,True,True,True]}]},
                       {'label': 'C. Geregeld PAX ATM', 'method': 'update','args':[{'visible': [True, False,False,False,False,
                                                                                               False,False,False,False,
                                                                                                False,False,False,False]}]},
                      {'label': 'C. Geregeld Cargo ATM', 'method': 'update','args':[{'visible': [False, True,False,False,False,
                                                                                               False,False,False,False,
                                                                                                 False,False,False,False]}]},
                      {'label': 'C. Ongeregeld PAX ATM', 'method': 'update','args':[{'visible': [False, False,True,False,False,
                                                                                               False,False,False,False,
                                                                                                 False,False,False,False]}]},
                      {'label': 'C. Ongeregeld Cargo ATM', 'method': 'update','args':[{'visible': [False, False,False,True,False,
                                                                                               False,False,False,False,
                                                                                                   False,False,False,False]}]},
                      {'label': 'C. Brandstof ATM', 'method': 'update','args':[{'visible': [False, False,False,False,True,
                                                                                               False,False,False,False,
                                                                                            False,False,False,False]}]},
                      {'label': 'C. Positievlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               True,False,False,False,
                                                                                                False,False,False,False]}]},
                      {'label': 'C. Taxivlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               False,True,False,False,
                                                                                             False,False,False,False]}]},
                      {'label': 'C. Fotovlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               False,False,True,False,
                                                                                             False,False,False,False]}]},
                      {'label': 'C. Rondvlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               False,False,False,True,
                                                                                             False,False,False,False]}]},
                      {'label': 'C. Reclamevlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               False,False,False,False,
                                                                                                True,False,False,False]}]},
                      {'label': 'C. Spuitvlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               False,False,False,False,
                                                                                              False,True,False,False]}]},
                      {'label': 'C. Ambulancevlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               False,False,False,False,
                                                                                                  False,False,True,False]}]},
                      {'label': 'C. Overig ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               False,False,False,False,
                                                                                         False,False,False,True]}]}]

    fig5.update_layout({'updatemenus':[{'type': "dropdown",'x':1.2,'y':1.1,'showactive': True,'buttons': dropdown_buttons1}]})

    fig5.update_layout(title_text='Commerciële ATM selectie', title_x=0.5, width=800, height=625) 
    
    fig6 = px.bar(df,
             x='Jaartal',
             y=['NC. Zakenvlucht ATM','NC. Privévlucht ATM', 'NC. Valschermvlucht ATM', 'NC. Zweefsleepvlucht ATM',
                'NC. Politievlucht ATM', 'NC. Inspectievlucht ATM', 'NC. Maatschappelijke vlucht ATM',
                'NC. Les/Oefenvlucht ATM', 'NC. Proef/Testvlucht ATM','NC. Overig ATM'],
             barmode='group',
             hover_data={'Jaartal':True,'Luchthaven':True},
             labels= {'value': "Aantal Niet-Commercieel ATM", 'variable': 'soort ATM'})      

    dropdown_buttons0=[{'label': 'NC. Alle types ATM', 'method': 'update','args':[{'visible': [True, True,True,True,True,
                                                                                               True,True,True,True,True]}]},
                       {'label': 'NC. Zakenvlucht ATM', 'method': 'update','args':[{'visible': [True, False,False,False,False,
                                                                                               False,False,False,False,False]}]},
                      {'label': 'NC. Privévlucht ATM', 'method': 'update','args':[{'visible': [False, True,False,False,False,
                                                                                               False,False,False,False,False]}]},
                      {'label': 'NC. Valschermvlucht ATM', 'method': 'update','args':[{'visible': [False, False,True,False,False,
                                                                                               False,False,False,False,False]}]},
                      {'label': 'NC. Zweefsleepvlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,True,False,
                                                                                               False,False,False,False,False]}]},
                      {'label': 'NC. Politievlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,True,
                                                                                               False,False,False,False,False]}]},
                      {'label': 'NC. Inspectievlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               True,False,False,False,False]}]},
                      {'label': 'NC. Maatschappelijke vlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               False,True,False,False,False]}]},
                      {'label': 'NC. Les/Oefenvlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               False,False,True,False,False]}]},
                      {'label': 'NC. Proef/Testvlucht ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               False,False,False,True,False]}]},
                      {'label': 'NC. Overig ATM', 'method': 'update','args':[{'visible': [False, False,False,False,False,
                                                                                               False,False,False,False,True]}]}]

    fig6.update_layout({'updatemenus':[{'type': "dropdown",'x':1.4,'y':1.1,'showactive': True,'buttons': dropdown_buttons0}]})

    fig6.update_layout(title_text='Niet-commerciële ATM selectie', title_x=0.5,width=800, height=625)          
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(fig5)
    with col2:
        st.write(fig6)
    st.info('Zie bijgevoegde URL met definities van de verschillende soorten commerciële / niet-commerciële vluchten: https://www.cbs.nl/nl-nl/cijfers/detail/60058ned?q=commerci%C3%ABle%20dienstverlening#shortTableDescription ')

elif page == 'Conclusies':
    ###DE BEVINDINGEN###
    st.subheader('Conclusies')
    st.write('• Een eerste kijk op de kaart geeft aan dat Lelystad Airport de grootste speler is met 24% van het totaal aantal landelijke ATMs, gevolgd door Teuge- en Budel Airport (15%) en daaronder Hilversum Airport (13%).')
    st.write('• De traffic movement lijngrafiek bevestigd dat de bovenstaande luchthavens het meeste aantal ATMs genieten. Wel is er een sterke daling te zien in Lelystad. Deze kan verklaard worden doordat er vanaf deze luchthaven veel privé en les/oefenvluchten worden gevlogen, welke tijdens de COVID-19 pandemie tijdelijk zijn stilgelegd. Kijkend naar de regios valt op dat in het oosten van Nederland veel wordt gevlogen. De regios Zuid en West zijn nagenoeg gelijk aan elkaar en in de regio Noord wordt het minst gevlogen.')
    st.write('• Bij het vergelijken van de commerciële (20k maximaal) t.o.v. de niet-commerciële ATMs (120k maximaal), valt op dat vanaf de regionale luchthavens voornamelijk wordt gevlogen met niet-commerciële doeleinden. Teuge airport steekt met kop en schouders boven de andere uit qua commerciële vluchten. Via deze luchthaven worden veel rondvluchten gemaakt. Ook Texel en Lelystad hebben veel commerciële ATMs in vergelijking met de overigen. Ook deze bestaan voornamelijk uit rondvluchten. Bij Lelystad komen hier ook nog positioneringsvluchten bij.')
    st.write('• De niet-commerciële ATMs worden het meest gevlogen vanaf Lelystad, Budel, Hilversum, Teuge en Seppe. Over het algmeen vinden veel privé vluchten plaats, evenals les/oefenvluchten. Bij Teuge valt op dat deze luchthaven ook veel wordt gebruikt voor valschermvluchten/parachutespringen en Hilversum kent relatief veel zweefsleepvluchten.')
    st.write("""***""")

elif page == 'Data cleaning & analyse':
    ###UITLEG OVER DE DATA CLEANING EN ANALYSE###
    st.subheader('Data cleaning')
    st.write('1. Allereerst zijn de packages in geladen. Er wordt voornamelijk gebruik gemaakt van pandas, plotly express, folium en streamlit packages.')
    st.write('2. Het inladen van de datasets. Deze datasets zijn de CBS dataset en luchthavens coördinaten dataset welke van eigen makelij is.')
    st.write('3. Na het inladen van de datasets, is gekeken naar de lengte, datatypes van de kolommen, nulwaarden en uitschieters.')
    st.write('4. Om de dataset bruikbaar te maken, zijn kolomnamen leesbaar gemaakt, nulwaarden verwijdert en datatypes verandert.')
    st.subheader('Data analyse')
    st.write('• Om te beginnen zijn waardes in jaartal kolommen aangepast naar een uniforme layout.')
    st.write('• Ook zijn sommige luchthavens uit de dataset gehaald omdat deze weinig informatie bevatte.')
    st.write('• Er is een regio kolom aangemaakt welke weergeeft in welke regio een bepaalde luchthaven zich bevindt. Dit is gedaan op basis van de provincies die bij een bepaalde regio horen. vervolgens is via een groupby functie een totaal aantal ATMs op basis van regio en jaartal toegevoegd aan de dataset.')
    st.write('• De coördinaten- en CBS dataset zijn samengevoegd om de kaart te kunnen maken. Hierbij is een dataframe selectie gemaakt van het jaar 2020, omdat dit de meest actuele informatie weergeeft.')
    st.write('• Er zijn percentages berekend van de totale ATMs per luchthaven over de regio en ook t.o.v. het landelijk totaal. Deze zijn verwerkt in de kaart.')
    st.write('• Tot slot zijn de gemodificeerde dataframes opgeslagen als nieuwe .CSV bestanden (streamlitdf.CSV & streamlitkaartdf.CSV), zodat alle data cleaning / analyse stappen niet opnieuw uitgevoerd hoeven te worden door streamlit. Dit scheelt tijd met het inladen van de visualisaties.')
    st.write('• Omdat er gebruik wordt gemaakt van opgeschoonde datasets, is voor het streamlit dashboard een nieuw .ipynb bestand aangemaakt, puur voor de visualisatie van het dashboard. Echter in beide bestanden zijn de visualisaties aanwezig.')
    st.write("""***""")
    
    


# In[ ]:




