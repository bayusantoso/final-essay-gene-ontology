from flask import render_template, flash, redirect, request
from fastsemsim.Ontology import ontologies
from fastsemsim.SemSim import CosineSemSim
from fastsemsim.Ontology import AnnotationCorpus
from fastsemsim import data
from app import app
from .forms import SearchForm
from .forms import SimilarityForm
import rpy2.robjects as robjects
import app.model.TermModel as TermModel

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
  form = SearchForm()
  return render_template('index.html', form=form)

@app.route('/result', methods=['GET','POST'])
def result():
  form = SearchForm()
  query = form.query.data
  ontology = form.ontology.data

  state, dict_terms, messages = get_go_term(query)

  result = {}
  message = []

  child_result = []
  parent_result = []
  anccestor_result = []
  offspring_result = []

  if ontology != None and query != None and ontology != "" and query != "":
    child_result, message = get_go_childrens(ontology, query)
    parent_result, message = get_go_parents(ontology, query)
    anccestor_result, message = get_go_ancesstors(ontology, query)
    offspring_result, message = get_go_offsprings(ontology, query)

  result["children"] = child_result
  result["parent"] = parent_result
  result["anccestor"] = anccestor_result
  result["offspring"] = offspring_result

  return render_template('result.html', form=form, state = state, model = dict_terms, result = result, message = message)

@app.route('/similarity', methods=['GET','POST'])
def similarity():
    form = SimilarityForm()
    first_go_id = form.first_go_id.data
    second_go_id = form.second_go_id.data
    similarity_function = form.similarity_function.data

    first_state, first_dict_terms, first_message = get_go_term(first_go_id)
    second_state, second_dict_terms, second_message = get_go_term(second_go_id)

    state = False
    if first_state != False and second_state != False:
        state = True

    similarity_result = None
    if first_go_id != '' and first_go_id != None and second_go_id != '' and second_go_id != None    :
        similarity_obj = get_go_cosine_similarity_object()
        similarity_result = count_cosine_similarity(first_dict_terms,second_dict_terms,similarity_obj)

    return render_template('similarity.html', form = form, first_go = first_dict_terms, second_go = second_dict_terms, state = state, similarity_result = similarity_result)

@app.route('/detail', methods=['GET','POST'])
def detail():
  id = request.args.get('id')
  state, dict_terms, message = get_go_term(id)
  return render_template('detail.html',id = id, state = state, result = dict_terms, message = message)

#private method, need to refactor to another class
#Get childrens of a term
def count_cosine_similarity(first_go,second_go,similarity_obj):
    result = []
    if similarity_obj :
        if len(first_go) > 0:
            for item in first_go:
                item_similarity = []
                value_first = ''
                if len(item["value"]) > 0:
                    for value in item["value"]:
                        value_first = value_first + value + ' '

                value_second = ''
                for item_second in second_go:
                    if item["key"] == item_second["key"]:
                        if len(item_second["value"]) > 0:
                            for value in item_second["value"]:
                                value_second = value_second + value + ' '
                item_similarity.append(item["key"])
                item_similarity.append(similarity_obj._SemSim(value_first, value_second))
                result.append(item_similarity)
    return result

def get_go_cosine_similarity_object():
    ontology_type = 'GeneOntology'
    ignore_parameters = {'ignore':{}}
    source_type = 'obo'
    source = None

    ontology = ontologies.load(source=source, source_type = source_type, ontology_type = ontology_type, parameters=ignore_parameters)
    ac = AnnotationCorpus.AnnotationCorpus(ontology)

    cosine = CosineSemSim(ontology,ac)
    return cosine

def get_go_childrens(go_term_ontology, go_term):
  robjects.r('''library(GO.db)''')

  child_map = robjects.r["GO%sCHILDREN" % (go_term_ontology)]
  children = []

  to_check = [go_term]

  try:
    while len(to_check) > 0:
          new_children = []
          for check_term in to_check:
              if check_term != 'all':
                if robjects.r.get(check_term, child_map):
                  if len(robjects.r.get(check_term, child_map)) > 0:
                    new_children.extend(list(robjects.r.get(check_term, child_map)))

          new_children = list(set([c for c in new_children if c]))
          children.extend(new_children)
          to_check = []
    children_state = True
  except:
    children_state = False

  result = []
  messages = []
  if children_state:
    if len(children) > 0:
      results = list(set(children))
      for go_id in results:
        state, dict_terms, message = get_go_term(go_id)
        if state:
          result.append(dict_terms)
        else:
          messages.append(message)

  return result, messages

#Get parents of a term
def get_go_parents(go_term_ontology, go_term):
  robjects.r('''library(GO.db)''')

  child_map = robjects.r["GO%sPARENTS" % (go_term_ontology)]
  children = []

  to_check = [go_term]

  try:
    while len(to_check) > 0:
          new_children = []
          for check_term in to_check:
              if check_term != 'all':
                if robjects.r.get(check_term, child_map):
                  if len(robjects.r.get(check_term, child_map)) > 0:
                    new_children.extend(list(robjects.r.get(check_term, child_map)))

          new_children = list(set([c for c in new_children if c]))
          children.extend(new_children)
          to_check = []
    children_state = True
  except:
    children_state = False

  result = []
  messages = []
  if children_state:
    if len(children) > 0:
      results = list(set(children))
      for go_id in results:
        state, dict_terms, message = get_go_term(go_id)
        if state:
          result.append(dict_terms)
        else:
          messages.append(message)

  return result, messages

#Get ancesstors of a term
def get_go_ancesstors(go_term_ontology, go_term):
  robjects.r('''library(GO.db)''')

  child_map = robjects.r["GO%sANCESTOR" % (go_term_ontology)]
  children = []

  to_check = [go_term]

  try:
    while len(to_check) > 0:
          new_children = []
          for check_term in to_check:
              if check_term != 'all':
                if robjects.r.get(check_term, child_map):
                  if len(robjects.r.get(check_term, child_map)) > 0:
                    new_children.extend(list(robjects.r.get(check_term, child_map)))

          new_children = list(set([c for c in new_children if c]))
          children.extend(new_children)
          to_check = []
    children_state = True
  except:
    children_state = False

  result = []
  messages = []
  if children_state:
    if len(children) > 0:
      results = list(set(children))
      for go_id in results:
        state, dict_terms, message = get_go_term(go_id)
        if state:
          result.append(dict_terms)
        else:
          messages.append(message)

  return result, messages

#Get offsprings of a term
def get_go_offsprings(go_term_ontology, go_term):
  robjects.r('''library(GO.db)''')

  child_map = robjects.r["GO%sOFFSPRING" % (go_term_ontology)]
  children = []

  to_check = [go_term]

  try:
    while len(to_check) > 0:
          new_children = []
          for check_term in to_check:
              if check_term != 'all':
                if robjects.r.get(check_term, child_map):
                  if len(robjects.r.get(check_term, child_map)) > 0:
                    new_children.extend(list(robjects.r.get(check_term, child_map)))

          new_children = list(set([c for c in new_children if c]))
          children.extend(new_children)
          to_check = []
    children_state = True
  except:
    children_state = False

  result = []
  messages = []
  if children_state:
    if len(children) > 0:
      results = list(set(children))
      for go_id in results:
        state, dict_terms, message = get_go_term(go_id)
        if state:
          result.append(dict_terms)
        else:
          messages.append(message)

  return result, messages

#Get details of a term
def get_go_term(go_id):
  robjects.r('''library(GO.db)''')
  dict_terms = []
  message = ""
  try:
      go_term = robjects.r['GOTERM']
      obj_term = robjects.r.get(go_id,go_term)
      list_attrs = list(obj_term.list_attrs())
      if len(list_attrs) > 0:
          for attr in list_attrs:
              item_terms = {}
              prop_terms = obj_term.do_slot(attr)
              item_terms["key"] = attr
              values = []

              if len(prop_terms) > 0:
                  for prop in prop_terms:
                      values.append(prop)

              item_terms["value"] = values
              dict_terms.append(item_terms)
      state = True
  except:
      state = False
      message = "Term Not Found"
  return state, dict_terms, message

