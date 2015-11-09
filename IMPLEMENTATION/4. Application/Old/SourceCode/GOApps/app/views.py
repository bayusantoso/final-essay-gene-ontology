from flask import render_template, flash, redirect, request
from app import app
from .forms import SearchForm
import rdflib

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
  form = SearchForm()
  return render_template('index.html', form=form)

@app.route('/result', methods=['GET','POST'])
def result():
  form = SearchForm()
  query =form.query.data
  query_result = None
  checker = "false"
  if query != None and query != "":
    graph = rdflib.Graph()
    graph.parse("go.owl")

    query_result = graph.query(
      """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

        SELECT
          ?id
          ?aspect
          ?label
          (group_concat(distinct ?synonym ; separator=", ") AS ?synonyms)
        WHERE {
          ?s oboInOwl:id ?id ;
             oboInOwl:hasOBONamespace ?aspect ;
             rdfs:label ?label ;
             oboInOwl:hasExactSynonym ?synonym .
          FILTER (REGEX(?aspect, """ '"' + form.query.data + '"' """, "i")
          || REGEX(?label, """ '"' + form.query.data + '"' """, "i")
          || REGEX(?synonym, """ '"' + form.query.data + '"' """, "i"))
        }
        GROUP BY ?id
        LIMIT 20
        """)

  return render_template('result.html', form = form, model = query_result)

@app.route('/resultnew', methods=['GET','POST'])
def resultnew():
  form = SearchForm()
  query =form.query.data
  query_result = None
  checker = "false"
  if query != None and query != "":
    graph = rdflib.Graph()
    graph.parse("go.owl")

    query_result = graph.query(
      """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

        SELECT
          ?id
          ?aspect
          ?label
          (group_concat(distinct ?synonym ; separator=", ") AS ?synonyms)
        WHERE {
          ?s oboInOwl:id ?id ;
             oboInOwl:hasOBONamespace ?aspect ;
             rdfs:label ?label ;
             oboInOwl:hasExactSynonym ?synonym .
          FILTER (REGEX(?aspect, """ '"' + form.query.data + '"' """, "i")
          || REGEX(?label, """ '"' + form.query.data + '"' """, "i")
          || REGEX(?synonym, """ '"' + form.query.data + '"' """, "i"))
        }
        GROUP BY ?id
        LIMIT 10
        """)

  return render_template('result_new.html', form = form, model = query_result)

@app.route('/detail', methods=['GET','POST'])
def detail():
  form = SearchForm()
  id_onto = request.args.get("id")
  id_onto.replace("%3A",":")
  query_result = None

  if id_onto != None and id_onto != "":
    graph = rdflib.Graph()
    graph.parse("go.owl")

    query_result = graph.query("""
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX owl: <http://www.w3.org/2002/07/owl#>
      PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
      PREFIX obo: <http://purl.obolibrary.org/obo/>
      PREFIX go: <http://purl.obolibrary.org/obo/go#>

      SELECT
        ?id
        ?aspect
        ?label
        ?synonym
        ?description
        ?comment
      WHERE {
        ?s oboInOwl:id ?id ;
           oboInOwl:hasOBONamespace ?aspect ;
           rdfs:label ?label ;
           oboInOwl:hasExactSynonym ?synonym ;
           obo:IAO_0000115 ?description;
				   rdfs:comment ?comment .
        FILTER (REGEX(?id, """ '"' + id_onto + '"' """))
      }
      """)

  return render_template('detail.html', form = form, model = query_result )
