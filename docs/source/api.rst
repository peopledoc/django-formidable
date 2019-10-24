==================
API Specifications
==================

.. This file has mimic Swagger UI without any http requests.
   The specifications are translated from YAML into JSON.

.. raw:: html

      <!-- Assets from Swagger UI -->
      <link href='_static/swagger-ui/swagger-ui.css' media='screen' rel='stylesheet' type='text/css'>

      <!-- API Specifications - Formidable -->
      <!-- <script src='_static/specs/formidable.js' type='text/javascript'></script> -->

      <script src="_static/swagger-ui/swagger-ui-bundle.js"> </script>
      <script src="_static/swagger-ui/swagger-ui-standalone-preset.js"> </script>
      <script>
      window.onload = function() {
        // Begin Swagger UI call region
        const ui = SwaggerUIBundle({
          url: "_static/specs/formidable.json",
          dom_id: '#swagger-ui',
          deepLinking: true,
          presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIStandalonePreset
          ],
          plugins: [
            SwaggerUIBundle.plugins.DownloadUrl
          ],
          layout: "StandaloneLayout"
        })
        // End Swagger UI call region

        window.ui = ui
      }
    </script>

    <div id="swagger-ui"></div>
