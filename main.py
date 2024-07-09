import streamlit as st
import pandas as pd

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

# st.set_page_config(layout="wide")

st.header("Machine Learning and Natural Language Processing in Clinical Trial Eligibility Criteria Parsing")
st.subheader("A Scoping Review")

st.markdown("""
- **Klaudia Kantor**, Roche Poland & Doctoral School of Poznan University of Technology
- **Mikołaj Morzy**, Poznan University of Technology
""")

st.success("""
           This page contains supplementary material to the paper 'Machine Learning and Natural Language Processing in Clinical Trial Eligibility Criteria Passing'. The tabs below offer access to three tables containing list of all papers included in the scoping review, breakdown of papers by the country of author/research and general type of publication, and the full feature extraction from all included studies.
           """)

st.divider()

df_tab1 = pd.read_table('data/table_1.tsv')
df_tab2 = pd.read_table('data/table_2.tsv')
df_tab3 = pd.read_table('data/table_3.tsv')


tab1, tab2, tab3 = st.tabs(
        [
            ":violet-background[List of all articles]",
            ":violet-background[Articles by country and type]",
            ":violet-background[Detailed features extracted from articles]"
            ]
        )

with tab1:

    st.info("""
    Use the slider to limit the year range of publications
    """)

    year_min, year_max = st.slider("", 2000, 2024, (2000, 2024))

    data = df_tab1[(df_tab1.year >= year_min) & (df_tab1.year <= year_max)].sort_values(by="year")
    st.dataframe(data, column_config={
        "year": st.column_config.NumberColumn(format="%d")
    })

    csv1 = convert_df(data)

    st.download_button(
       "Download table",
       csv1,
       "list-of-articles.csv",
       "text/csv",
       key='download-csv-tab1'
    )

with tab2:

    st.info("""
    If you want to limit the list articles to a specific country, therapeutic area
    or general publication type, simply use the widgets below to enter filtering criteria.
    """
    )


    _lst_countries_author = df_tab2["country (author)"].tolist()
    lst_countries_author = [c.strip() for b in _lst_countries_author for c in b.split(',')]
    ca = st.multiselect("Country (author)", sorted(set(lst_countries_author)))

    _lst_countries_research = df_tab2["country (research)"].tolist()
    lst_countries_research = [c.strip() for b in _lst_countries_research for c in b.split(',')if b]
    cr = st.multiselect("Country (research)", sorted(set(lst_countries_research)))

    _lst_therapeutic_area = df_tab2["therapeutic area"].tolist()
    lst_therapeutic_area = [t.strip() for w in _lst_therapeutic_area for t in w.split(',')]
    ta = st.multiselect("Therapeutic area", sorted(set(lst_therapeutic_area)))

    lst_general_character = df_tab2["general character"].str.strip().unique()
    gc = st.multiselect("General character", sorted(lst_general_character))

    if ca:
        ca_idx = df_tab2["country (author)"].apply(lambda x: any(y in x for y in ca))
    else:
        ca_idx = df_tab2["country (author)"].apply(lambda x: True)

    if cr:
        cr_idx = df_tab2["country (research)"].apply(lambda x: any(y in x for y in cr))
    else:
        cr_idx = df_tab2["country (research)"].apply(lambda x: True)

    if ta:
        ta_idx = df_tab2["therapeutic area"].apply(lambda x: any(y in x for y in ta))
    else:
        ta_idx = df_tab2["therapeutic area"].apply(lambda x: True)

    if gc:
        gc_idx = df_tab2["general character"].apply(lambda x: any(y in x for y in gc))
    else:
        gc_idx = df_tab2["general character"].apply(lambda x: True)

    data = df_tab2[ca_idx & cr_idx & ta_idx & gc_idx]
    st.dataframe(data)

    csv2 = convert_df(data)

    st.download_button(
       "Download table",
       csv2,
       "articles-by-country.csv",
       "text/csv",
       key='download-csv-tab2'
    )

with tab3:

    st.dataframe(df_tab3)
