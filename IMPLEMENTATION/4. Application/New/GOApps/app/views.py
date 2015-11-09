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
  print(relationship)
  result = None
  if relationship == "children":
    result = get_go_childrens(ontology, query)
  elif relationship == "parent":
    result = get_go_parents(ontology, query)
  elif relationship == "anchestor":
    result = get_go_ancesstors(ontology, query)
  elif relationship == "offspring":
    result = get_go_offsprings(ontology, query)

  return render_template('result.html', form=form, result = result)

def get_go_childrens(go_term_type, go_term):
  robjects.r('''
      library(GO.db)
  ''')

  child_map = robjects.r["GO%sCHILDREN" % (go_term_type)]
  children = []

  to_check = [go_term]

  while len(to_check) > 0:
        print(to_check)
        new_children = []
        for check_term in to_check:
            print(check_term)
            if check_term != 'all':
              if robjects.r.get(check_term, child_map):
                if len(robjects.r.get(check_term, child_map)) > 0:
                  new_children.extend(list(robjects.r.get(check_term, child_map)))

        new_children = list(set([c for c in new_children if c]))
        children.extend(new_children)
        to_check = []

  result = None
  if len(children) > 0:
    result = list(set(children))

  return result

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

def get_go_term(go_term, robjects):
  term = []
  return term

