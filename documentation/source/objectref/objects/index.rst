.. highlight:: python

################
Objects
################

FontParts scripts are built on with objects that represent fonts, glyphs, contours and so on. The objects are obtained through :ref:`fontParts.world`.

.. toctree::
   :maxdepth: 1
   :hidden:

   font
   info
   groups
   kerning
   features
   lib
   layer
   glyph
   contour
   segment
   bpoint
   point
   component
   anchor
   image
   guideline

.. _fontparts-objects:


.. raw:: html

   <?xml version="1.0" encoding="UTF-8"?>
   <svg width="100%" viewBox="0 0 860 630" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">

   <defs>
   <style>@import "https://static.typemytype.com/robofont/font.css";</style>
   <style>
      text {
         font-family: 'Source Sans Pro', Lucida Grande, Geneva, Arial, Verdana, sans-serif;
         fill: white;
         pointer-events: none;
      }
      .connection {
         stroke: rgb(204, 204, 204);
         stroke-width: 5;
      }
      .object {
         stroke-width: 0;
      }
      .object:hover {
         transition: stroke-width .1s ease-in-out;
         stroke-width: 20;
      }
   </style>
   </defs>

   <!-- lines -->
   <path class='connection' d="M250,373 l-43.55,174.65" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M250,373 l105.8,145.62" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M250,373 l-161.78,78.91" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M250,373 l-164.44,-73.21" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M250,373 l-49.61,-173.03" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M250,373 l180,0" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M430,373 l180,0" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M610,373 l-103.24,147.45" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M610,373 l46.59,173.87" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M610,373 l163.14,76.07" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M610,373 l163.14,-76.07" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M610,373 l46.59,-173.87" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M610,373 l-103.24,-147.45" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M506.76,225.55 l-155,0.0" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M506.76,225.55 l-85.55,-129.25" transform="matrix(1,0,0,-1,0,630)"/>
   <path class='connection' d="M506.76,225.55 l60.56,-142.68" transform="matrix(1,0,0,-1,0,630)"/>

   <!-- font -->
   <g>
   <a xlink:href="font.html" target="_parent">
      <path class='object' d="M310.1,312.9 c33.19,33.19,33.19,87.01,0,120.21 c-33.19,33.19,-87.01,33.19,-120.21,0.0 c-33.19,-33.19,-33.19,-87.01,-0.0,-120.21 c33.19,-33.19,87.01,-33.19,120.21,-0.0 Z M310.1,312.9" fill="rgb(145,187,62)" stroke="rgb(145,187,62)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,165,-288)">
         <tspan font-size="32" x="51.1" y="551.2">font</tspan>
      </text>
   </a>
   </g>

   <!-- font lib -->
   <g>
   <a xlink:href="lib.html" target="_parent">
      <path class='object' d="M398.23,476.2 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M398.23,476.2" fill="rgb(97,187,62)" stroke="rgb(97,187,62)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,295.8013454126452,-458.62305898749037)">
         <tspan font-size="18" x="26.74" y="574.2">font lib</tspan>
      </text>
   </a>
   </g>

   <!-- info -->
   <g>
   <a xlink:href="info.html" target="_parent">
      <path class='object' d="M248.88,505.23 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M248.88,505.23" fill="rgb(62,187,74)" stroke="rgb(62,187,74)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,146.4540587920598,-487.6532307296793)">
         <tspan font-size="18" x="42.04" y="574.2">info</tspan>
      </text>
   </a>
   </g>

   <!-- groups -->
   <g>
   <a xlink:href="groups.html" target="_parent">
      <path class='object' d="M130.64,409.48 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,-0.0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M130.64,409.48" fill="rgb(62,187,122)" stroke="rgb(62,187,122)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,28.217071666149934,-391.9068064220339)">
         <tspan font-size="18" x="28.14" y="574.2">groups</tspan>
      </text>
   </a>
   </g>

   <!-- kerning -->
   <g>
   <a xlink:href="kerning.html" target="_parent">
      <path class='object' d="M127.99,257.36 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,-0.0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M127.99,257.36" fill="rgb(62,187,170)" stroke="rgb(62,187,170)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,25.561817624331837,-239.7874042463559)">
         <tspan font-size="18" x="24.88" y="574.2">kerning</tspan>
      </text>
   </a>
   </g>

   <!-- features -->
   <g>
   <a xlink:href="features.html" target="_parent">
      <path class='object' d="M242.81,157.55 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M242.81,157.55" fill="rgb(62,156,187)" stroke="rgb(62,156,187)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,140.3852759529402,-139.97289473110254)">
         <tspan font-size="18" x="21.04" y="574.2">features</tspan>
      </text>
   </a>
   </g>

   <!-- layer -->
   <g>
   <a xlink:href="layer.html" target="_parent">
      <path class='object' d="M472.43,330.57 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M472.43,330.57" fill="rgb(196,191,83)" stroke="rgb(196,191,83)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,370.0,-313.0)">
         <tspan font-size="18" x="36.74" y="574.2">layer</tspan>
      </text>
   </a>
   </g>

   <!-- glyph -->
   <g>
   <a xlink:href="glyph.html" target="_parent">
      <path class='object' d="M670.1,312.9 c33.19,33.19,33.19,87.01,0,120.21 c-33.19,33.19,-87.01,33.19,-120.21,0.0 c-33.19,-33.19,-33.19,-87.01,0,-120.21 c33.19,-33.19,87.01,-33.19,120.21,-0.0 Z M670.1,312.9" fill="rgb(247,195,104)" stroke="rgb(247,195,104)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,525.0,-288.0)">
         <tspan font-size="32" x="41.64" y="551.2">glyph</tspan>
      </text>
   </a>
   </g>

   <!-- glyph lib -->
   <g>
   <a xlink:href="lib.html" target="_parent">
      <path class='object' d="M549.18,478.02 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M549.18,478.02" fill="rgb(247,159,104)" stroke="rgb(247,159,104)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,446.7562414568117,-460.4473679720186)">
         <tspan font-size="18" x="21.43" y="574.2">glyph lib</tspan>
      </text>
   </a>
   </g>

   <!-- anchor -->
   <g>
   <a xlink:href="anchor.html" target="_parent">
      <path class='object' d="M699.01,504.44 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M699.01,504.44" fill="rgb(247,123,104)" stroke="rgb(247,123,104)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,596.5874281184538,-486.86664873203244)">
         <tspan font-size="18" x="27.5" y="574.2">anchor</tspan>
      </text>
   </a>
   </g>

   <!-- component -->
   <g>
   <a xlink:href="component.html" target="_parent">
      <path class='object' d="M815.56,406.64 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M815.56,406.64" fill="rgb(247,104,120)" stroke="rgb(247,104,120)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,713.135401666597,-389.07128711332587)">
         <tspan font-size="18" x="8.61" y="574.2">component</tspan>
      </text>
   </a>
   </g>

   <!-- image -->
   <g>
   <a xlink:href="image.html" target="_parent">
      <path class='object' d="M815.56,254.5 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M815.56,254.5" fill="rgb(247,104,156)" stroke="rgb(247,104,156)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,713.135401666597,-236.92871288667413)">
         <tspan font-size="18" x="32.18" y="574.2">image</tspan>
      </text>
   </a>
   </g>

   <!-- guideline -->
   <g>
   <a xlink:href="guideline.html" target="_parent">
      <path class='object' d="M699.01,156.71 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M699.01,156.71" fill="rgb(247,104,192)" stroke="rgb(247,104,192)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,596.5874281184538,-139.13335126796767)">
         <tspan font-size="18" x="18.02" y="574.2">guideline</tspan>
      </text>
   </a>
   </g>

   <!-- contour -->
   <g>
   <a xlink:href="contour.html" target="_parent">
      <path class='object' d="M549.18,183.13 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0.0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M549.18,183.13" fill="rgb(247,104,228)" stroke="rgb(247,104,228)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,446.7562414568117,-165.55263202798153)">
         <tspan font-size="18" x="23.42" y="574.2">contour</tspan>
      </text>
   </a>
   </g>

   <!-- point -->
   <g>
   <a xlink:href="point.html" target="_parent">
      <path class='object' d="M394.18,183.13 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,0 Z M394.18,183.13" fill="rgb(219,104,247)" stroke="rgb(219,104,247)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,291.7562414568117,-165.55263202798153)">
         <tspan font-size="18" x="35.84" y="574.2">point</tspan>
      </text>
   </a>
   </g>

   <!-- bPoint -->
   <g>
   <a xlink:href="bpoint.html" target="_parent">
      <path class='object' d="M463.63,53.87 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,-0.0 Z M463.63,53.87" fill="rgb(171,104,247)" stroke="rgb(171,104,247)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,361.2060087334427,-36.30032960757046)">
         <tspan font-size="18" x="30.15" y="574.2">bPoint</tspan>
      </text>
   </a>
   </g>

   <!-- segment -->
   <g>
   <a xlink:href="segment.html" target="_parent">
      <path class='object' d="M609.75,40.45 c23.43,23.43,23.43,61.42,0,84.85 c-23.43,23.43,-61.42,23.43,-84.85,0 c-23.43,-23.43,-23.43,-61.42,0,-84.85 c23.43,-23.43,61.42,-23.43,84.85,-0.0 Z M609.75,40.45" fill="rgb(123,104,247)" stroke="rgb(123,104,247)" transform="matrix(1,0,0,-1,0,630)"/>
      <text text-anchor="start" transform="matrix(1,0,0,1,507.3195663726491,-22.874379742853193)">
         <tspan font-size="18" x="21.21" y="574.2">segment</tspan>
      </text>
   </a>
   </g>

   </svg>


