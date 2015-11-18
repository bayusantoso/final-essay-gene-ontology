from flask import render_template, flash, redirect, request
from app import app
from .forms import SearchForm
import rpy2.robjects as robjects
import pdb

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
  form = SearchForm()
  return render_template('index.html', form=form)

@app.route('/result', methods=['GET','POST'])
def result():
  form = SearchForm()
  query = form.query.data
  relationship = form.relationship.data
  ontology = form.ontology.data

  state, dict_terms, messages = get_go_term(query)

  result = []
  message = []
  if relationship == "children":
    result, message = get_go_childrens(ontology, query)

  return render_template('result.html', form=form, state = state, model = dict_terms, result = result, message = message)

@app.route('/detail', methods=['GET','POST'])
def detail():
  id = request.args.get('id')
  state, dict_terms, message = get_go_term(id)
  return render_template('detail.html',id = id, state = state, result = dict_terms, message = message)

def get_go_childrens(go_term_type, go_term):
  robjects.r('''library(GO.db)''')

  child_map = robjects.r["GO%sCHILDREN" % (go_term_type)]
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

def get_go_parents(go_term_type, go_term):
  robjects.r('''
      library(GO.db)
  ''')

  child_map = robjects.r["GO%sPARENTS" % (go_term_type)]
  children = []

  to_check = [go_term]

  while len(to_check) > 0:
        print(to_check)
        new_children = []
        for check_term in to_check:
            if check_term != 'all':
              if robjects.r.get(check_term, child_map):
                if len(robjects.r.get(check_term, child_map)) > 0:
                  new_children.extend(list(robjects.r.get(check_term, child_map)))

        if len(new_children) > 0:
          new_children = list(set([c for c in new_children if c]))
          children.extend(new_children)
          to_check = new_children
        else:
          to_check = []

  result = None
  if len(children) > 0:
    result = list(set(children))

  return result

def get_go_ancesstors(go_term_type, go_term):
  robjects.r('''
      library(GO.db)
  ''')

  child_map = robjects.r["GO%sANCESTOR" % (go_term_type)]
  children = []

  to_check = [go_term]
  while len(to_check) > 0:
        print(to_check)
        new_children = []
        for check_term in to_check:
            if check_term != 'all':
              if len(robjects.r.get(check_term, child_map)) > 0:
                new_children.extend(list(robjects.r.get(check_term, child_map)))

        if len(new_children) > 0:
          new_children = list(set([c for c in new_children if c]))
          children.extend(new_children)
          to_check = new_children
        else:
          to_check = []

  result = None
  if len(children) > 0:
    result = list(set(children))

  return result

def get_go_offsprings(go_term_type, go_term):
  robjects.r('''
      library(GO.db)
  ''')

  child_map = robjects.r["GO%sOFFSPRING" % (go_term_type)]
  children = []

  to_check = [go_term]

  while len(to_check) > 0:
        print(to_check)
        new_children = []
        for check_term in to_check:
            if check_term != 'all':
              if len(robjects.r.get(check_term, child_map)) > 0:
                new_children.extend(list(robjects.r.get(check_term, child_map)))

        if len(new_children) > 0:
          new_children = list(set([c for c in new_children if c]))
          children.extend(new_children)
          to_check = new_children
        else:
          to_check = []

  result = None
  if len(children) > 0:
    result = list(set(children))

  return result

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

