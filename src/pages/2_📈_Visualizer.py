import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from global_variables import *

# Création du graphe
net = Network(height="600px", width="100%", directed=True)

# Dossier contenant les fichiers
script_dir = os.path.dirname(os.path.abspath(__file__))
papers_dir = os.path.abspath(os.path.join(script_dir, "../../database/papers"))


# Ajout de noeuds avec lien vers fichier
for paper_file in os.listdir(papers_dir):
    if paper_file.endswith(".txt"):
        paper_id = paper_file.replace(".txt", "")
        file_path = f"{papers_dir}/{paper_file}"
        net.add_node(paper_id, label=paper_id, title="Double-cliquez pour ouvrir", file=file_path)

# Injecter le script JS dans le HTML généré
with open("graph.html", "r", encoding="utf-8") as f:
    htmlraw = f.read()

custom_js = """
<script type="text/javascript">
    network.on("doubleClick", function (params) {
        if (params.nodes.length > 0) {
            var nodeId = params.nodes[0];
            var nodeData = nodes.get(nodeId);
            if (nodeData.file) {
                window.open(nodeData.file, '_blank');
            }
        }
    });
</script>
"""

# Injecte le JS avant </body>
htmlraw = htmlraw.replace("</body>", custom_js + "\n</body>")

with open("graph.html", "w", encoding="utf-8") as f:
    f.write(htmlraw)

# Affichage du graphe
if os.path.exists("graph.html"):
    with open("graph.html", 'r', encoding='utf-8') as f:
        html_graph = f.read()
    html(html_graph, height=600)
else:
    st.info("No previously generated graph")