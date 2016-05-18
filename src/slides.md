name: title
layout: true
class: template-base, template-title, template-logo-big

---
name: slide
layout: true
class: template-base, template-slide, template-logo

---
template: title
class: template-title-coffee

# Projet Formidable
## Django && EmberJS

**Guillaume Camera**
<br/>
![icon](img/twitter.png) @moumoutt3
<br/>
![icon](img/mail.png) camera.g@gmail.com

**Guillaume Gérard**
<br/>
![icon](img/twitter.png) @ggerard88
<br/>
![icon](img/mail.png) guillaume.gerard88@gmail.com

---
template: slide

# Contexte

- PeopleDoc est un éditieur de logiciel R.H.

- PeopleAsk, un produit de ticketing

- Permet a un employer de remplir des forms spécifiques (mais pas seulement)

- Laisser la main au client de générer ses propres forms spécifiques à son métier sans devoir repasser par la case R&D.

---
template: slide

# Pourquoi django-formidable ?

- Contraintes métiers fortes

    - Validations Métiers

    - Restriction d'accès

    - Simplicité d'utilisation (R.H.)

- Existant n'est pas complet (Role, ...)

- Besoin d'intégration (UI, API..) pour **nos** applications


---
template: slide

# django-formidable
## A la recherche des standards

- Application Django

- Un modèle de référence formidable.models.Formidable

- Méthode disponible pour récupérer un django form standard

---
template: slide

# django-formidable
## A la recherche des standards
### Des formulaires Django


```python

    >>> formidable = Formidable.objects.get(pk=42)
    >>> form_class = formidable.get_django_form_class(role='jedi')
    >>> form = form_class(data={'last_name': 'Kenobi'})
    >>> isinstance(form, forms.Form)
    True
    >>> form.is_valid()
    False
    >>> form = form_class(data={'first_name': 'Obiwan', 'last_name': 'Kenobi'})
    >>> form.is_valid()
    True

```

---
template: slide

# django-formidable
## A la recherche des standards
### Des formulaires Django


```python

    {{ form.as_p }}

```


---
template: slide

# django-formidable
## Customisation
### L'usine à champs

- Widgets par défaut django

- Possibilité d'intégerer des widgets spécifiques

```python

    from formidable.forms.field_builder import FieldBuilder

    class MyFieldFactory()


```


---
template: slide

# django-formidable
## 

- Customisation fortes \o/

  - Widget spécifique

  - Validateurs personnalisé

  - Presets

- Builder full python

- Builder full API

```python
if lol == "tamere":
```

---
template: slide

# API
## Communication vers le monde

- Django REST framework

- RESTful

- API de Création / Edition

- API de récupération de formulaire


---
template: slide

# Formidable-UI
## Interface

- ### Framework EmberJS


--

- ### Utilise l'API


--

- ### Deux composants: 
  - Saisie 
  - Builder

--

- Integration

  - Copie static

  - Un peu de code pour les parametres et gerer les evenements

---
template: slide

# Formidable-UI
## Form Builder

- ### Barre de composant


--

- ### Drag'n'drop pour ajout et tri


--

- ### Mise en page


--

- ### Paramètres pour chaque champ
  - ### Affichage && saisie
  - ### Validation simple
  - ### Accès selon les contextes


---
template: slide

# Formidable-UI
## Form Builder

[Builder]

---
template: slide

# Formidable-UI
## Preset de Validation

- ### Ajout des validations


- ### Supression des validations


- ### Edition des validations


--

- ### Chaque preset est affiché sous forme de formulaire


---
template: slide

# Formidable-UI
## Preset de Validation

[Validations]

---
template: slide

# Formidable-UI
## Preview

- ### Affichage des formulaire avec validations


--

- ### Changement de contexte


--

- ### Vérifier que vos formulaires sont correct


---
template: slide

# Formidable-UI
## Preview

[Preview]

---
template: slide

# Formidable-UI
## Preview

[Inputs]

---
template: slide

# Voir plus

###


### Open source

- ### ...


---
template: title
class: template-title-desk

# Merci à vous !
## Des questions ?

**Guillaume Camera**
<br/>
![icon](img/twitter.png) @moumoutt3
<br/>
![icon](img/mail.png) camera.g@gmail.com

**Guillaume Gérard**
<br/>
![icon](img/twitter.png) @ggerard88
<br/>
![icon](img/mail.png) guillaume.gerard88@gmail.com

