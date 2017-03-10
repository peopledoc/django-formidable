==================
API Specifications
==================

.. This file has mimic Swagger UI without any http requests.
   The specifications are translated from YAML into JSON.

.. raw:: html

      <!-- Assets from Swagger UI -->
      <link href='_static/swagger-ui/css/typography.css' media='screen' rel='stylesheet' type='text/css'>
      <link href='_static/swagger-ui/css/reset.css' media='screen' rel='stylesheet' type='text/css'>
      <link href='_static/swagger-ui/css/screen.css' media='screen' rel='stylesheet' type='text/css'>
      <link href='_static/swagger-ui/css/reset.css' media='print' rel='stylesheet' type='text/css'>
      <link href='_static/swagger-ui/css/print.css' media='print' rel='stylesheet' type='text/css'>

      <script src='_static/swagger-ui/lib/object-assign-pollyfill.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/lib/jquery.slideto.min.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/lib/jquery.wiggle.min.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/lib/jquery.ba-bbq.min.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/lib/handlebars-4.0.5.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/lib/lodash.min.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/lib/backbone-min.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/swagger-ui.min.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/lib/highlight.9.1.0.pack.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/lib/highlight.9.1.0.pack_extended.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/lib/jsoneditor.min.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/lib/marked.js' type='text/javascript'></script>
      <script src='_static/swagger-ui/lib/swagger-oauth.js' type='text/javascript'></script>

      <!-- API Specifications - Formidable -->
      <script src='_static/specs/formidable.js' type='text/javascript'></script>

      <script type="text/javascript">
        $(function () {
          hljs.configure({
            highlightSizeThreshold: 5000
          });
          window.swaggerUi = new SwaggerUi({
            url: "",
            spec: spec,
            dom_id: "swagger-ui-container",
            docExpansion: "default",
            defaultModelRendering: 'schema',
            showRequestHeaders: false,
            validatorUrl: null
          });
          window.swaggerUi.load();
      });
      </script>

    <div class="swagger-section">
      <div id="message-bar" class="swagger-ui-wrap" data-sw-translate>&nbsp;</div>
      <div id="swagger-ui-container" class="swagger-ui-wrap"></div>
    </div>
