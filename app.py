from lib import corpus_generator_lib
from lib.corpus_generator_lib import *
import streamlit as st

@st.cache(suppress_st_warning=True)
def file_upload(df):
    fichier = st.sidebar.file_uploader("Choisir un fichier",['csv','txt'])
    if fichier is not None:
        fichier.seek(0)
        df = pd.read_csv(fichier, sep=';', decimal = ".", index_col=None, encoding = "utf-8")
        st.subheader("Aperçu des données")
        st.write(df.head())
    return df,fichier
            
def list_results(path):
    st.subheader("Consulter mes fichiers de résultats")
    l_all_files=list_files_in_dir(path, "*")
    for file in l_all_files:
        file=file.replace('./',os.getcwd()+"\\")
        st.markdown("<a href=file:\\\\\\///"+file+" target=\"_blank\">"+os.path.basename(file)+"</a>", unsafe_allow_html=True)
        
def generer_corpus(projet,menu_value,df,l_variables,l_variables_all):
    #############################
    # CREATION DES REPERTOIRES  #
    #############################
    path="./"+projet+"/"
    if not os.path.exists(path):
        os.makedirs(path)
    with st.spinner(">> "+str(len(df))+" lignes transmises avant nettoyage"):
        print(len(df),"lignes transmises avant nettoyage")
        df=df[list(l_variables_all)]
        df.dropna(how='all',inplace=True,subset=[menu_value])
    with st.spinner('1/2 - Nettoyage du texte'):
        print(">> Nettoyage du texte")
        df[menu_value]=df[menu_value].apply(clean_text)
        df.dropna(how='all', inplace=True,subset=[menu_value])
        print(len(df),"lignes retenues pour le corpus")  
    with st.spinner('2/2 - Création du corpus'):
        print(">> Création du corpus")
        corpus=create_corpus(df, menu_value,l_variables,path)
    st.subheader("Aperçu du corpus")
    st.write(str(len(df))+" lignes retenues pour le corpus")
    st.write(corpus[:10])
    print(">> Fin des traitements")
    # with open(os.path.join(path,"corpus.txt"), "w") as f:
    #     f.write('\n'.join(corpus))
    #     st.download_button('Download corpus', f)

    with open("corpus.txt", "w") as f:
        f.write('\n'.join(corpus))
        btn = st.download_button('Download corpus', f, file_name="corpus.txt",mime="application/octet-stream")
    
#     with open("ths.pdf", "rb") as file:
#     btn=st.download_button(
#     label="Generate Trivia Host Sheet",
#     data=file,
#     file_name="TriviaHostSheet.pdf",
#     mime="application/octet-stream"
# )
    

def main():
    
    st.set_page_config(
        page_title="Générer un corpus Iramuteq",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # st.set_option('deprecation.showfileUploaderEncoding', False)
    st.sidebar.title('Paramètres')
    st.title('Générer un corpus Iramuteq')   
    
    
    projet=st.sidebar.text_input("Donner un nom de projet", value='monProjet', max_chars=None, key=None, type='default')

    fichier = st.sidebar.file_uploader("Choisir un fichier",['csv','txt'])
    if fichier is not None:
        # Can be used wherever a "file-like" object is accepted:
#         fichier.seek(0)
        df = pd.read_csv(fichier, sep=';',index_col=None, encoding = "utf-8")
        st.write(df.head())
        st.write(fichier)
        menu_value = st.sidebar.selectbox('Quelle colonne correspond au texte à analyser ?',df.columns)
        options = st.sidebar.multiselect('Quelles sont les variables à retenir pour l\'analyse ?',df.columns)

        l_variables=set()
        l_variables_all=set()

        for item in options:
            l_variables.add(item)
            l_variables_all.add(item)

        l_variables_all.add(menu_value)
        if st.sidebar.button('Préparer le corpus'):
            generer_corpus(projet,menu_value,df,l_variables,l_variables_all)
            list_results(path=os.path.join(".", projet))

        
    
if __name__ == "__main__":
    main()