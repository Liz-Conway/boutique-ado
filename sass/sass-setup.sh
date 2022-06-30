touch main.sass
mkdir abstracts base components layout pages themes vendors
cd abstracts
touch _colours.sass _functions.sass _mixins.sass _variables.sass _media-queries.sass
cd ../base/
touch _animations.sass _base.sass _typography.sass _utilities.sass _reset.sass
cd ../components/
touch _button.sass
cd ../layout/
touch _grid.sass _header.sass _footer.sass _navbar.sass 
cd ../pages/
touch _home.sass
touch _404.sass

cd ..

echo "/*~~~~~~~  Typography  ~~~~~~~*/" >> base/_typography.sass
echo "@import url('https://fonts.googleapis.com/css2?family=Gabriela&family=Roboto+Slab:wght@100;200;300;400;500;600;700;800;900&display=swap')" >> base/_typography.sass
echo "" >> base/_typography.sass
echo body >> base/_typography.sass
echo $'\tfont:' >> base/_typography.sass
echo $'\t\tfamily: $baseFontFamily' >> base/_typography.sass
echo $'\t\tweight: $normalWt' >> base/_typography.sass
echo $'\t\t//size: $baseFontSize' >> base/_typography.sass
echo $'\t/* For accessibility - The WCAG criteria states that line-height should be at least 1.5*/' >> base/_typography.sass
echo $'\t/* The WCAG criteria is meant for "body" text, not headings.*/' >> base/_typography.sass
echo $'\t/* So we can calculate the proper line height for all elements :*/' >> base/_typography.sass
echo $'\t/* Instead of calculating the line height by multiplying the font-size with a number like 1.5, */' >> base/_typography.sass
echo $'\t/* this alternative uses the font-size as a base, and adds a fixed amount of space to each line. */' >> base/_typography.sass
echo $'\tline-height: $baseLineHeight' >> base/_typography.sass
echo $'\tcolor: $shadow' >> base/_typography.sass
echo $'\n\n' >> base/_typography.sass

echo "/*===== END  Typography  =====*/" >> base/_typography.sass

# Utilities
echo "/*~~~~~~~  Utilities  ~~~~~~~*/" >> base/_utilities.sass
echo .centreText >> base/_utilities.sass
echo $'\ttext-align: center' >> base/_utilities.sass
echo "" >> base/_utilities.sass
echo .marginBottom >> base/_utilities.sass
echo $'\t&Small' >> base/_utilities.sass
echo $'\t\tmargin-bottom: 1.5rem' >> base/_utilities.sass
echo $'\t&Medium' >> base/_utilities.sass
echo $'\t\t/* Mobile first - so smaller values first */' >> base/_utilities.sass
echo $'\t\tmargin-bottom: 3rem' >> base/_utilities.sass
echo $'\t\t@include respond(tabletLandscape)' >> base/_utilities.sass
echo $'\t\t\tmargin-bottom: 4rem' >> base/_utilities.sass
echo $'\t&Big' >> base/_utilities.sass
echo $'\t\tmargin-bottom: 5rem' >> base/_utilities.sass
echo $'\t\t@include respond(tabletLandscape)' >> base/_utilities.sass
echo $'\t\t\tmargin-bottom: 8rem' >> base/_utilities.sass
echo "" >> base/_utilities.sass
echo .marginTop >> base/_utilities.sass
echo $'\t&Small' >> base/_utilities.sass
echo $'\t\tmargin-top: 1.5rem' >> base/_utilities.sass
echo $'\t&Medium' >> base/_utilities.sass
echo $'\t\t\tmargin-top: 4rem' >> base/_utilities.sass
echo $'\t&Big' >> base/_utilities.sass
echo $'\t\tmargin-top: 8rem' >> base/_utilities.sass
echo $'\t&Huge' >> base/_utilities.sass
echo $'\t\t\tmargin-top: 10rem' >> base/_utilities.sass
echo "" >> base/_utilities.sass
echo .invisible >> base/_utilities.sass
echo $'\tdisplay: none' >> base/_utilities.sass

echo "/*===== END  Utilities  =====*/" >> base/_utilities.sass


echo "/*~~~~~~~  Reset  ~~~~~~~*/" >> base/_reset.sass

echo "/*" >> base/_reset.sass
echo "  Josh's Custom CSS Reset" >> base/_reset.sass
echo "  https://www.joshwcomeau.com/css/custom-css-reset*/" >> base/_reset.sass
echo $'\n\n' >> base/_reset.sass
echo $'*, *::before, *::after' >> base/_reset.sass
echo $'\tbox-sizing: inherit' >> base/_reset.sass
echo $'\ttext-decoration: none' >> base/_reset.sass
echo $'\tpadding: 0' >> base/_reset.sass
echo $'\tmargin: 0\n' >> base/_reset.sass
echo "/* The height of an element is calculated based on its CHILDREN. " >> base/_reset.sass
echo "    So setting height: 100% on an element will cause it to be 100% of the child's height." >> base/_reset.sass
echo "    This setting causes the height to be calculated from the parent*/" >> base/_reset.sass
echo "html, body" >> base/_reset.sass
echo $'\theight: 100%\n' >> base/_reset.sass
echo "body" >> base/_reset.sass
echo "	/* MacOS browsers like Chrome and Safari still use subpixel antialiasing by default.*/" >> base/_reset.sass
echo "	/* We need to explicitly turn it off.*/" >> base/_reset.sass
echo $'\t-webkit-font-smoothing: antialiased\n' >> base/_reset.sass
echo "img, picture, video, canvas, svg" >> base/_reset.sass
echo $'\t/*display: block*/      /* Will remove extra space from under an image - Use flexbox on its parent instead*/' >> base/_reset.sass
echo $'\t/* Keep large images from overflowing, if they're placed in a container that isn't wide enough to contain them. */' >> base/_reset.sass
echo $'\tmax-width: 100%\n' >> base/_reset.sass
echo "/* by default, buttons and inputs don't inherit typographical styles from their parents. */" >> base/_reset.sass
echo "/* Instead, they have their own weird styles. */" >> base/_reset.sass
echo "/* Form inputs shouldn't have their own typographical styles! */" >> base/_reset.sass
echo "input, button, textarea, select" >> base/_reset.sass
echo $'\tfont: inherit\n' >> base/_reset.sass
echo "/* The overflow-wrap property lets us tweak the line-wrapping algorithm, */" >> base/_reset.sass
echo "/* and give it permission to use hard wraps when no soft wrap opportunties can be found */" >> base/_reset.sass
echo "p, h1, h2, h3, h4, h5, h6" >> base/_reset.sass
echo $'\toverflow-wrap: break-word\n' >> base/_reset.sass

echo "/*===== END  Reset  =====*/" >> base/_reset.sass


echo "/*~~~~~~~  Button  ~~~~~~~*/" >> components/_button.sass
echo ".btn" >> components/_button.sass
echo $'\ttext-transform: uppercase' >> components/_button.sass
echo $'\tdisplay: inline-block' >> components/_button.sass
echo $'\tpadding: 1.5rem 4rem' >> components/_button.sass
echo $'\tborder-radius: 10rem' >> components/_button.sass
echo $'\tfont-size: $baseFontSize' >> components/_button.sass
echo $'\tbackground-color: $highlight' >> components/_button.sass
echo $'\tcolor: $shadow' >> components/_button.sass
echo $'\tborder: 3px solid $shadow' >> components/_button.sass
echo $'\ttext-align: center' >> components/_button.sass
echo $'\ttransition: all .2s\n' >> components/_button.sass
echo $'\t&:hover' >> components/_button.sass
echo $'\t\t/* Make the button pop up => 3D effect */' >> components/_button.sass
echo $'\t\ttransform: translateY(-.5rem)' >> components/_button.sass
echo $'\t\t/* Box Shadow X Y Blur Colour*/' >> components/_button.sass
echo $'\t\tbox-shadow: 0 1rem 2rem rgba($black, .2)\n' >> components/_button.sass
echo $'\t&:active' >> components/_button.sass
echo $'\t\tcolor: $accentDark' >> components/_button.sass
echo $'\t\tbackground-color: $shadow' >> components/_button.sass
echo $'\t\t/* Make the button appear to be pressed => 3D effect */' >> components/_button.sass
echo $'\t\ttransform: translateY(-.1rem)' >> components/_button.sass
echo $'\t\t/* Box Shadow X Y Blur Colour*/' >> components/_button.sass
echo $'\t\tbox-shadow: 0 1rem 2rem rgba($black, .2)\n' >> components/_button.sass
echo $'\t&:not(:last-child)' >> components/_button.sass
echo $'\t\tmargin-right: 1.5rem\n' >> components/_button.sass
echo $'\t&CTA' >> components/_button.sass
echo $'\t\tbackground-color: $accentDark\n' >> components/_button.sass
echo $'\t&Ghost' >> components/_button.sass
echo $'\t\tbackground-color: $white' >> components/_button.sass
echo $'\t\t&:hover' >> components/_button.sass
echo $'\t\t\tcolor: $black' >> components/_button.sass
echo $'\t\t&:active' >> components/_button.sass
echo $'\t\t\tcolor: $white\n' >> components/_button.sass
echo $'\t&TextOnly' >> components/_button.sass
echo $'\t\tborder: none' >> components/_button.sass
echo $'\t\tbackground-color: transparent' >> components/_button.sass
echo $'\t\t&:hover, &:active' >> components/_button.sass
echo $'\t\t\tbackground-color: transparent' >> components/_button.sass
echo $'\t\t\tcolor: $midtone' >> components/_button.sass
echo "/*===== END  Button  =====*/" >> components/_button.sass

echo "/*~~~~~~~  Grid  ~~~~~~~*/" >> layout/_grid.sass
echo "/*===== END  Grid  =====*/" >> layout/_grid.sass

echo "/*~~~~~~~  Header  ~~~~~~~*/" >> layout/_header.sass
echo "/*===== END  Header  =====*/" >> layout/_header.sass

echo "/*~~~~~~~  Footer  ~~~~~~~*/" >> layout/_footer.sass
echo footer >> layout/_footer.sass
echo $'\t/*Sticky footer*/' >> layout/_footer.sass
echo $'\tmargin-top: auto' >> layout/_footer.sass
echo $'\tbackground-color: $shadow' >> layout/_footer.sass
echo $'\tcolor: $highlight' >> layout/_footer.sass
echo $'\tdisplay: flex' >> layout/_footer.sass
echo $'\talign-items: center' >> layout/_footer.sass
echo $'\t// Mobile 1st' >> layout/_footer.sass
echo $'\tflex-direction: column' >> layout/_footer.sass
echo "/*===== END  Footer  =====*/" >> layout/_footer.sass

echo "/*~~~~~~~  Navbar  ~~~~~~~*/" >> layout/_navbar.sass
echo "/*===== END  Navbar  =====*/" >> layout/_navbar.sass

echo "/*~~~~~~~  Home Page  ~~~~~~~*/" >> pages/_home.sass
echo "/*===== END  Home Page  =====*/" >> pages/_home.sass

echo "/*~~~~~~~  404 Page  ~~~~~~~*/" >> pages/_404.sass
echo ".error" >> pages/_404.sass
echo $'\t&Section'  >> pages/_404.sass
echo $'\t\tbackground-color: $midtone' >> pages/_404.sass
echo $'\t\tdisplay: flex' >> pages/_404.sass
echo $'\t\tflex-direction: column' >> pages/_404.sass
echo $'\t\talign-items: center\n' >> pages/_404.sass
echo $'\t&404' >> pages/_404.sass
echo $'\t\tfont:' >> pages/_404.sass
echo $'\t\t\tsize: 10rem' >> pages/_404.sass
echo $'\t\t\tweight: $lightWt' >> pages/_404.sass
echo $'\t\tcolor: $accentDark' >> pages/_404.sass
echo $'\t\tmargin: 3rem auto' >> pages/_404.sass
echo $'\t&Subtitle' >> pages/_404.sass
echo $'\t\tcolor: $shadow\n' >> pages/_404.sass
echo "/*===== END  404 Page  =====*/" >> pages/_404.sass


echo "// ORDER  Base + typography > general layout > grid > page layout > components" >> main.sass
echo @import \"abstracts/colours\" >> main.sass
echo @import \"abstracts/variables\" >> main.sass
echo @import \"abstracts/media-queries\" >> main.sass
echo @import \"abstracts/mixins\" >> main.sass
echo @import \"abstracts/functions\" >> main.sass
echo $'\n' >> main.sass
echo @import \"base/typography\" >> main.sass
echo $'@import "base/reset.sass"' >> main.sass
echo @import \"base/base\" >> main.sass
echo @import \"base/utilities\" >> main.sass

echo "\$white: #FFFFFF" >> abstracts/_colours.sass
echo "\$black: #000000" >> abstracts/_colours.sass
echo "\$midtone: #777777 // Background on Navbar & Footer" >> abstracts/_colours.sass
echo "\$highlight: \$white // Callout Background" >> abstracts/_colours.sass
echo "\$shadow: \$black // Text & Navbar" >> abstracts/_colours.sass
echo $'\n$error: #cc0000' >> abstracts/_colours.sass
echo $'\n// Transparencies' >> abstracts/_colours.sass
echo "\$semiTransparent: rgba(0, 0, 0, 0.5)" >> abstracts/_colours.sass
echo "\$quarterTransparent: rgba(0, 0, 0, 0.25)" >> abstracts/_colours.sass
echo "\$greyTransparency: rgba(0,0,0,0.2)" >> abstracts/_colours.sass

echo "// BASE FONT" >> abstracts/_variables.sass
echo "\$baseFontSize: 1.6rem" >> abstracts/_variables.sass
echo "\$baseFontFamily: Gabriela" >> abstracts/_variables.sass
echo "\$baseLineHeight: calc(1em + 0.7rem)" >> abstracts/_variables.sass
echo "\$roboto : 'Roboto Slab', 'Helvetica Neue', sans-serif" >> abstracts/_variables.sass
echo "" >> abstracts/_variables.sass
echo "// FONT WEIGHTS" >> abstracts/_variables.sass
echo \$lightWt: 100 >> abstracts/_variables.sass
echo \$slimWt: 200 >> abstracts/_variables.sass
echo \$thinWt: 300 >> abstracts/_variables.sass
echo \$normalWt: 400 >> abstracts/_variables.sass
echo \$thickWt: 500 >> abstracts/_variables.sass
echo \$heavyWt: 600 >> abstracts/_variables.sass
echo \$boldWt: 700 >> abstracts/_variables.sass
echo $'\n$boxShadow: 0 1.5rem 4rem rgba($black, .15)' >> abstracts/_variables.sass
echo $'\n$bodyPadding: 3rem' >> abstracts/_variables.sass


echo "" >> base/_base.sass
echo html >> base/_base.sass
echo $'\t/* Since browser default font-size is 16px*/' >> base/_base.sass
echo $'\t/* Set it to 10px (on a desktop) to make converting px to rem easier. */' >> base/_base.sass
echo $'\t/* Use a percentage so that if a user changes the font size */' >> base/_base.sass
echo $'\t/* on their browser or zooms the font sizes,  */' >> base/_base.sass
echo $'\t/* paddings and margins adjust accordingly. */' >> base/_base.sass
echo $'\t/* This defines what 1rem is */' >> base/_base.sass
echo $'\t/* For mobile 1st design we will use 8px for the mobile device */' >> base/_base.sass
echo $'\tfont-size: 50%    /*1rem = 8px  8px/16px= 50%*/' >> base/_base.sass
echo "" >> base/_base.sass
echo $'\t@include respond(tabletLandscape)' >> base/_base.sass
echo $'\t\tfont-size: 56.25%    /*1rem = 9px  9px/16px= 56.25%*/' >> base/_base.sass
echo $'\t@include respond(desktop)' >> base/_base.sass
echo $'\t\tfont-size: 62.5%    /*1rem = 10px  10px/16px= 62.5%*/' >> base/_base.sass
echo $'\t@include respond(XL)' >> base/_base.sass
echo $'\t\tfont-size: 75%    /*1rem = 12px  12px/16px= 75%*/' >> base/_base.sass

echo "" >> base/_base.sass
echo body >> base/_base.sass
echo $'\t/* Inheritable properties*/' >> base/_base.sass
echo $'\tbox-sizing: border-box' >> base/_base.sass
echo $'\t/* Set up page for sticky footer*/' >> base/_base.sass
echo $'\tdisplay: flex' >> base/_base.sass
echo $'\tflex-direction: column' >> base/_base.sass
echo "" >> base/_base.sass
echo $'\tmin-height: 100vh\n' >> base/_base.sass
echo $'\t/* Non-inheritable properties */' >> base/_base.sass
echo $'\tpadding: $bodyPadding' >> base/_base.sass

# Functions
echo "@function pixelToEm(\$value, \$base:16)" >> abstracts/_functions.sass
echo $'\t@return ($value / $base) + em' >> abstracts/_functions.sass

# Mixins
echo "@mixin flexCentre(\$direction:row)" >> abstracts/_mixins.sass
echo $'\tdisplay: flex' >> abstracts/_mixins.sass
echo $'\tjustify-content: center' >> abstracts/_mixins.sass
echo $'\talign-items: center' >> abstracts/_mixins.sass
echo $'\tflex-direction: $direction' >> abstracts/_mixins.sass

# Media Queries - mobile 1st
echo $'// Media Query Manager\n' >> abstracts/_media-queries.sass
echo $'//\t\t\t\t\t\t\t\t\tPixels\t\t\t\t$breakpoint argument choices' >> abstracts/_media-queries.sass
echo $'// Phone\t\t\t\t\t\t320 - 600\t\t[phone]' >> abstracts/_media-queries.sass
echo $'// Tablet Portrait\t\t\t601 - 800\t\ttabletPortrait' >> abstracts/_media-queries.sass
echo $'// Tablet Landscape\t\t801 - 950\t\ttabletLandscape' >> abstracts/_media-queries.sass
echo $'// Desktop\t\t\t\t\t951 - 1200\t\tdesktop' >> abstracts/_media-queries.sass
echo $'// XL Desktop\t\t\t\t1200+\t\t\t\tXL' >> abstracts/_media-queries.sass
echo $'\n// Phone is the default in Mobile 1st approach' >> abstracts/_media-queries.sass
echo "// So we do not need to specify any \$breakpoint for the phone size" >> abstracts/_media-queries.sass
echo $'\n//1em = 16px' >> abstracts/_media-queries.sass
echo $'\n$breakpoints:('tabletPortrait': (min-width: 37.5em), 'tabletLandscape': (min-width: 50em), 'desktop': (min-width: 59.375em), 'XL': (min-width: 75em)) !default' >> abstracts/_media-queries.sass
echo "//\$breakpoints: (" >> abstracts/_media-queries.sass
echo $'//	"tabletPortrait":  only screen and (min-width:  600px),\t\t\t\t\t//37.5em\t\t\t// 600px / 16px = 37.5em' >> abstracts/_media-queries.sass
echo $'//	"tabletLandscape": only screen and (min-width:  800px),\t\t\t\t//50em\t\t\t// 800px / 16px = 50em' >> abstracts/_media-queries.sass
echo $'//	"desktop":  only screen and (min-width:  950px),\t\t\t\t\t\t\t//59.375em\t\t// 950px / 16px = 59.375em' >> abstracts/_media-queries.sass
echo $'//	"XL":  only screen and (min-width: 1200px)\t\t\t\t\t\t\t\t\t//75em\t\t\t\t// 1200px / 16px = 75em' >> abstracts/_media-queries.sass
echo $'//) !default\n\n' >> abstracts/_media-queries.sass

echo "/// Mixin to manage responsive breakpoints" >> abstracts/_media-queries.sass
echo "/// @author Kitty Giraudel wrote the original version" >> abstracts/_media-queries.sass
echo "/// @param {String} $breakpoint - Breakpoint name" >> abstracts/_media-queries.sass
echo "/// @require $breakpoints" >> abstracts/_media-queries.sass
echo "@mixin respond(\$breakpoint)" >> abstracts/_media-queries.sass
echo $'\t// If the key exists in the map' >> abstracts/_media-queries.sass
echo $'\t@if map-has-key($breakpoints, $breakpoint)' >> abstracts/_media-queries.sass
echo $'\t\t// Prints a media query based on the value' >> abstracts/_media-queries.sass
echo $'\t\t@media only screen and #{inspect(map-get($breakpoints, $breakpoint))}' >> abstracts/_media-queries.sass
echo $'\t\t\t@content' >> abstracts/_media-queries.sass
echo $'\t@else if type-of($breakpoint) == number' >> abstracts/_media-queries.sass
echo $'\t\t@media only screen and (min-width: #{pixelToEm($breakpoint)})' >> abstracts/_media-queries.sass
echo $'\t\t\t@content' >> abstracts/_media-queries.sass
echo $'\t@else' >> abstracts/_media-queries.sass
echo $'\t// If the key doesn\'t exist in the map' >> abstracts/_media-queries.sass
echo $'\t\t@warn "Unfortunately, no value could be retrieved from `#{$breakpoint}`. "' >> abstracts/_media-queries.sass
echo $'\t\t\t\t+ "Available breakpoints are: #{map-keys($breakpoints)}."' >> abstracts/_media-queries.sass
