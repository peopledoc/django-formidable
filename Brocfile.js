var autoprefixer = require('broccoli-autoprefixer');
var funnel = require('broccoli-funnel');
var mergeTrees = require('broccoli-merge-trees');
var path = require('path');
var sass = require('broccoli-sass-source-maps');

var dirs = {
  bower: 'bower_components',
  src: 'src',
  fonts: 'fonts',
  js: 'js',
  img: 'img',
  videos: 'videos'
};

var fontsFormats = ['*.eot', '*.svg', '*.ttf', '*.woff', '*.woff2'];
var jsFormats = ['*.js'];
var imagesFormats = ['**/*.png', '**/*.jpg', '**/*.gif', '**/*.svg'];
var videosFormats = ['**/*.mp4'];
var htmlFormats = ['*.html', '*.htm'];
var slidesFormats = ['**/*.md'];

// Fonts
var robotoFonts = funnel(path.join(dirs.bower, 'roboto-fontface', 'fonts'), {
  include: fontsFormats,
  destDir: dirs.fonts
});
var ubuntuFonts = funnel(path.join(dirs.bower, 'ubuntu-fontface', 'fonts'), {
  include: fontsFormats,
  destDir: dirs.fonts
});
var montserratFonts = funnel(path.join(dirs.bower, 'montserrat-webfont', 'fonts'), {
  include: fontsFormats,
  destDir: dirs.fonts
});

// Vendors
var jqueryJS = funnel(path.join(dirs.bower, 'jquery', 'dist'), {
  include: ['jquery.min.js'],
  destDir: dirs.js
});
var remarkJS = funnel(path.join(dirs.bower, 'remark', 'out'), {
  include: ['remark.min.js'],
  destDir: dirs.js
});

// CSS
var css = sass(
  [dirs.src, dirs.bower],
  'css/style.scss',
  'css/style.css',
  {
    sourceMap: true,
    sourceMapEmbed: true,
    outputStyle: 'compressed'
  }
);
var prefixedCss = autoprefixer(css, {
  browsers: ['firefox 44','firefox 43','edge 13','edge 12','ie 11','ie 10','ie 9','safari 7.1','chrome 47','chrome 48'],
  sourcemap: true
});

// JS
var js = funnel(path.join(dirs.src, dirs.js), {
  include: jsFormats,
  destDir: dirs.js
});

// Images
var images = funnel(path.join(dirs.src, dirs.img), {
  include: imagesFormats,
  destDir: dirs.img
});

// Images
var videos = funnel(path.join(dirs.src, dirs.videos), {
  include: videosFormats,
  destDir: dirs.videos
});

// Pages
var pages = funnel(dirs.src, {
  include: htmlFormats
});

// Slides
var slides = funnel(dirs.src, {
  include: slidesFormats
});

module.exports = mergeTrees([
  robotoFonts,
  ubuntuFonts,
  montserratFonts,
  jqueryJS,
  remarkJS,
  prefixedCss,
  js,
  images,
  videos,
  pages,
  slides
]);
