name: title
layout: true
class: template-base, template-title, template-logo-big

---
name: transition
layout: true
class: template-base, template-title, template-logo

---
name: slide
layout: true
class: template-base, template-slide, template-logo

---
template: title
class: template-title-forms

# Projet Formidable
## Django && EmberJS

**Guillaume Camera**
<br/>
![icon-16](img/twitter.png) @moumoutt3
<br/>
![icon-16](img/mail.png) camera.g@gmail.com

**Guillaume Gérard**
<br/>
![icon-16](img/twitter.png) @ggerard88
<br/>
![icon-16](img/mail.png) guillaume.gerard88@gmail.com

---
template: slide

# Contexte

- ### PeopleDoc est un éditieur de logiciel R.H.

<br/>

--

- ### PeopleAsk, un produit de ticketing

<br/>
--

- ### Permet a un employer de remplir des forms spécifiques (mais pas seulement)

<br/>

--

- ### Laisser la main au client de générer ses propres forms spécifiques à son métier sans devoir repasser par la case R&D.


---
template: slide

# Pourquoi django-formidable ?

--

- ### Contraintes métiers fortes

--

    - #### Validations Métiers

    - #### Restriction d'accès

    - #### Simplicité d'utilisation (R.H.)

--

- ### Existant n'est pas complet (Role, ...)

<br/>
--

- ### Besoin d'intégration (UI, API..) pour **nos** applications


---
template: slide

# django-formidable
## A la recherche des standards

- ### Application Django

<br/>

--

- ### Un modèle de référence, formidable.models.Formidable

<br/>

--

- ### Méthode disponible pour récupérer un django form standard

---
template: transition
class: template-title-transition

# Django-formidable
## Communication vers le monde

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

- Champ django par défaut (CharField, TextField, ...)

- Possibilité d'intégerer de customiser les champs produits

```python

    from formidable.forms import field_builder

    class MyTextFieldFactory(field_builder.TextFieldBuilder):
        widget_class = B3Textarea


    class MyFormFieldFactory(field_builder.FormFieldFactory):
        field_maps.update({
            'text': MyTextFieldFactory,
        })

    form_class = formidable.get_django_form_class(field_factory=MyFormFieldFactory)

```

---
template: slide

# django-formidable
## Customisation
### Les validations

- ### Validations champs à champs

  - #### Validateurs django
  - #### Validateurs supplémentaires pour les dates (is\_age\_under, ...)


- ### Validations globales, des presets

  - #### Validation plus complexes (Fournit des validations génériques)
  - #### Ècrite en python
  - #### Ajout de validations métiers personnalisées

--
template: slide

# django-formidable
## Customisation
### Les Validations customs

- On s'assure que salaire + bonus inférieur à 100 000

```python

    from formidable.forms.validations import Presets, PresetValueArgument, PresetFieldArgument


    class CAC40limitation(Presets):

        slug = 'limitation-gain'
        label = 'Limitation du gain total'
        description = 'S'assurer que les gains ne sont pas trop élévé'
        message = '{salary} plus {bonus} cannot be greater than {limitation}'


        class MetaParameters:
            salary = PresetFieldArgument()
            bonus = PresetFieldArgument()
            limitation = PresetValueArgument()


        def run(self, salary, bonus, limitation):
            return salary + bonus < limitation

```

---
template: transition
class: template-title-bees

# API
## Communication vers le monde


---
template: slide

# API
## Communication vers le monde

- ### Django REST framework


--

- ### RESTful


--

- ### Deux namespaces :

  - ### API de Création / Edition de formulaire

  - ### API de récupération de formulaire selon un contexte


---
template: transition
class: template-title-transition

# Formidable-UI
## Une histoire de JS

---
template: slide

# Formidable-UI
## Interface

- ### Utilise l'API


--

- ### Framework EmberJS ![ember](img/emberjs.png)


--

- ### Deux composants: 

  - ### Constructeur de formulaire

  - ### Saisie utilisateur

---
template: slide

# Formidable-UI
## Form Builder - Création

- ### Barre d'outils (champs)


--

- ### Drag'n'drop


--

- ### Templates spécifiques


--

- ### Paramètres :

  - ### Affichage && saisie

  - ### Validation simple

  - ### Accès selon les contextes

---
template: slide

# Formidable-UI
## Form Builder - Preset de Validation

- ### CRUD sur les presets


--

- ### Preset => Mini formulaire dynamique


---
template: slide

# Formidable-UI
## Preview / Saisie utilisateur

- ### Affichage selon le contexte


--

- ### Validations sur les champs


--

- ### Vérifier que les saisies sont valides


---
template: slide

# Formidable-UI
## Démo Form Builder

[Démo]

---
template: slide

# Formidable-UI
## Démo Saisie

[Démo]

---
template: slide

# Formidable-UI
## Intégration

```html
<link rel="stylesheet" href=".../vendor.css">
<link rel="stylesheet" href=".../formidable.css">

<script src=".../vendor.js"></script>
<script src=".../formidable.js"></script>

<script>
  $(document).ready(function() {
      Formidable.on('form-is-valid', function(status) {
        // actions
        console.log(status);
      });
      Formidable.start({
        // options
        component: 'builder',
        namespace: 'api',
        lang: 'fr'
      });
  });
</script>
```

---
template: slide

# Voir plus

###


### Open source

- ### ...


---
template: title
class: template-title-poney, template-logo-big

# Merci à vous !
## Des questions ?

**Guillaume Camera**
<br/>
![icon-16](img/twitter.png) @moumoutt3
<br/>
![icon-16](img/mail.png) camera.g@gmail.com

**Guillaume Gérard**
<br/>
![icon-16](img/twitter.png) @ggerard88
<br/>
![icon-16](img/mail.png) guillaume.gerard88@gmail.com
