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

PeopleDoc => Editieur de logiciel => PeopleAsk => RH

Permet a un employer de remplir des forms spécifiques (mais pas queue ;)

Laisser la main au client de généré ses propres forms spécifiques à son métier sans devoir repasser par la case R&D.

---
template: transition
class: template-title-transition

# Django-formidable
## Communication vers le monde

---
template: slide

# Django-formidable
## Formulaire dynamique

- Toujours fournir du standard (formulaire, validations, rendering)

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
