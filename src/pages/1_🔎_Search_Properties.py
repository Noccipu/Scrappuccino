import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from global_variables import *

# Page config
st.set_page_config(page_title="Search Properties", layout="wide")
st.title("🔎 Search Properties")

# Initialiser l'état global
if 'articleCount' not in st.session_state:
    st.session_state.articleCount = 0
if 'worksList' not in st.session_state:
    st.session_state.worksList = []


st.markdown("# Search Properties")
st.markdown("## Create graph")

# Selectbox for the From
selectFrom = st.selectbox("From", ["Paper", "Author", "Field", "Journal"], index=0)
userSearchConfig["selectFrom"] = selectFrom

# Selectbox for the Look for, locked if the From Selectbox has no value
if selectFrom:
    selectLookForOptions = optionsLookFor.get(selectFrom, [])
    selectLookFor = st.selectbox("Look for", [""] + selectLookForOptions, index=0)
    userSearchConfig["selectLookFor"] = selectLookFor
else:
    st.selectbox("Look for", ["Select a 'From' option"], disabled=True)
    selectLookFor = None

# When the two Selectboxes have correct values we show the corresponding parameters
if selectFrom and selectLookFor:

    # Parameters set determination according to the two Selectboxes values
    params = optionsParameters.get((selectFrom, selectLookFor), [])
    st.markdown("### Parameters")

    # The parameters are displayed
    if params:

        # Input type selecter
        if "Input type" in params:
            selectInputTypeOptions = optionsInputType.get(selectFrom, [])
            selectInputType = st.selectbox("Input type", selectInputTypeOptions, index=0)
            userSearchConfig["selectInputType"] = selectInputType
            pass
        
        # Initial input (can be a name, doi, etc...)
        initialInput = st.text_input(f"Enter a {selectInputType}", value=DEFAULT_INPUT)
        userSearchConfig["initialInput"] = initialInput
        userSearchConfig["initialInputFormatted"] = userSearchConfig["initialInput"].replace(" ", ("%20"))

        # Tree depth selecter
        if "Tree depth" in params:
            treeDepth = DEFAULT_DEPTH
            treeDepth = st.slider("Tree depth", 1, MAX_DEPTH, DEFAULT_DEPTH)
            userSearchConfig["treeDepth"] = treeDepth
            pass
        
        # Results quantity selecter
        if "Quantity" in params:
            resultsQuantity = DEFAULT_QUANTITY
            max_articles = st.slider(f"Number of {selectLookFor}", 1, MAX_QUANTITY, DEFAULT_QUANTITY)
            userSearchConfig["max_articles"] = max_articles
            pass

        # Button to search for the wanted content
        if st.button("Start search"):
            st.session_state.articleCount = 0
            st.session_state.worksList = []

            # Graph visual settings
            #net = Network(height='100%', width='100%', bgcolor='#222222', font_color='white')
            #net.barnes_hut()

            nx_graph = nx.cycle_graph(10)
            nx_graph.nodes[1]['title'] = 'Number 1'
            nx_graph.nodes[1]['group'] = 1
            nx_graph.nodes[3]['title'] = 'I belong to a different group!'
            nx_graph.nodes[3]['group'] = 10
            nx_graph.add_node(20, size=20, title='couple', group=2)
            nx_graph.add_node(21, size=15, title='couple', group=2)
            nx_graph.add_edge(20, 21, weight=5)
            nx_graph.add_node(25, size=25, label='lonely', title='lonely node', group=3)


            nt = Network(height="300px", width="100%",bgcolor='#222222', notebook=True,heading='')
            nt.from_nx(nx_graph)
            nt.show('networkx-pyvis2.html')


            print(userSearchConfig)

            
            
            """
            searchUrl = f"https://api.openalex.org/works?search={subjectToSearchFormatted}&per-page=5"
            searchResponse = requests.get(searchUrl)

            if searchResponse.status_code == 200:
                searchData = searchResponse.json()
                for work in searchData['results']:
                    get_paper_info_from_id(work['id'].split('/')[-1], net)

                net.show('recursive_graph.html')
                st.success("Scraping terminé !")
            else:
                st.error("Aucun article trouvé.")
            """
            
    else:
        st.info("No parameter for this combination")
else:
    st.markdown("### Parameters")
    st.info("Please select both 'From' and 'Look for' to see the parameters")
