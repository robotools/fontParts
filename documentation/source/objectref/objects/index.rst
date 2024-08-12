.. highlight:: python

################
Objects
################

FontParts scripts are built on with objects that represent fonts, glyphs, contours and so on. The objects are obtained through :ref:`fontparts-world`.

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

    <svg id="fp-object-tree" xmlns="http://www.w3.org/2000/svg" viewBox="-12 -12 797 589">
    <style>
        g a:focus {
            outline: none;
        }
        text, tspan {
            pointer-events: none;
            font-family: 'Source Sans Pro', Lucida Grande, Geneva, Arial, Verdana, sans-serif;
        }
        .circle {
            stroke-width: 0;
        }
        .circle:hover {
            transition: stroke-width .1s ease-in-out;
            stroke-width: 20;
        }
    </style>
    <g fill="none" fill-rule="evenodd" transform="translate(1 1)">
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M217.76,105.4912 L103.8512,230.04" transform="matrix(1 0 0 -1 0 335.531)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M217.76,54.48 L231.44,230.04" transform="matrix(1 0 0 -1 0 284.52)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M217.76,233.84 L50.56,230.04" transform="matrix(1 0 0 -1 0 463.88)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M217.76,362.1888 L101.5712,230.04" transform="matrix(1 0 0 -1 0 592.229)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M218,231 L392.4124,231" transform="matrix(1 0 0 -1 0 462)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M392,231 L553.4924,231" transform="matrix(1 0 0 -1 0 462)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M553.6572,62.4096 L485.0216,230.4" transform="matrix(1 0 0 -1 0 292.81)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M553.6572,51.0096 L620.0128,230.4" transform="matrix(1 0 0 -1 0 281.41)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M553.6572,160.2444 L720.1276,230.4" transform="matrix(1 0 0 -1 0 390.644)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M553.6572,290.6756 L720.1276,230.4" transform="matrix(1 0 0 -1 0 521.076)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M553.6572,390.7904 L634.4528,230.4" transform="matrix(1 0 0 -1 0 621.19)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M553.6572,392.3104 L492.6216,230.4" transform="matrix(1 0 0 -1 0 622.71)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M492.6216,394.1724 L350.8664,392.3104" transform="matrix(1 0 0 -1 0 786.483)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M492.6216,489.7964 L410.612,392.3104" transform="matrix(1 0 0 -1 0 882.107)"/>
        <path fill="#FFF" fill-rule="nonzero" stroke="#D5D5D5" stroke-dasharray="1" stroke-linecap="round" stroke-width="3.04" d="M492.6216,513.1124 L521.6232,392.3104" transform="matrix(1 0 0 -1 0 905.423)"/>
        <g transform="translate(53 55)">
        <a xlink:href="info.html" target="_parent">
        <path class="circle" fill="#3EBB53" fill-rule="nonzero" stroke="#3EBB53" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(35.431 38.554)">
            <tspan x=".947" y="18">info</tspan>
        </text>
        </g>
        <g transform="translate(335 179)">
        <a xlink:href="layer.html" target="_parent">
        <path class="circle" fill="#C4BF53" fill-rule="nonzero" stroke="#C4BF53" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(30.947 38.141)">
            <tspan x=".343" y="18">layer</tspan>
        </text>
        </g>
        <g transform="translate(52 312)">
        <a xlink:href="features.html" target="_parent">
        <path class="circle" fill="#3EBBBB" fill-rule="nonzero" stroke="#3EBBBB" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(18.911 38.249)">
            <tspan x=".864" y="18">features</tspan>
        </text>
        </g>
        <g transform="translate(300 344)">
        <a xlink:href="point.html" target="_parent">
        <path class="circle" fill="#DB68F7" fill-rule="nonzero" stroke="#DB68F7" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(30.122 38.227)">
            <tspan x=".948" y="18">point</tspan>
        </text>
        </g>
        <g transform="translate(670 240)">
        <a xlink:href="image.html" target="_parent">
        <path class="circle" fill="#F7689C" fill-rule="nonzero" stroke="#F7689C" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(26.104 38.74)">
            <tspan x=".843" y="18">image</tspan>
        </text>
        </g>
        <g transform="translate(670 110)">
        <a xlink:href="component.html" target="_parent">
        <path class="circle" fill="#F76878" fill-rule="nonzero" stroke="#F76878" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(6.824 38.303)">
            <tspan x=".021" y="18">component</tspan>
        </text>
        </g>
        <g transform="translate(181 4)">
        <a xlink:href="lib.html" target="_parent">
        <path class="circle" fill="#5DBB3E" fill-rule="nonzero" stroke="#5DBB3E" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(40.099 38.54)">
            <tspan x=".996" y="18">lib</tspan>
        </text>
        </g>
        <g transform="translate(442 342)">
        <a xlink:href="contour.html" target="_parent">
        <path class="circle" fill="#F768E4" fill-rule="nonzero" stroke="#F768E4" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(20.238 38.37)">
            <tspan x=".435" y="18">contour</tspan>
        </text>
        </g>
        <g transform="translate(582 340)">
        <a xlink:href="guideline.html" target="_parent">
        <path class="circle" fill="#F768C0" fill-rule="nonzero" stroke="#F768C0" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(15.275 38.85)">
            <tspan x=".499" y="18">guideline</tspan>
        </text>
        </g>
        <g transform="translate(0 183)">
        <a xlink:href="kerning.html" target="_parent">
        <path class="circle" fill="#3EBB87" fill-rule="nonzero" stroke="#3EBB87" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(21.458 38.901)">
            <tspan x=".524" y="18">kerning</tspan>
        </text>
        </g>
        <g transform="translate(434 12)">
        <a xlink:href="lib.html" target="_parent">
        <path class="circle" fill="#F79F68" fill-rule="nonzero" stroke="#F79F68" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(40.678 38.474)">
            <tspan x=".996" y="18">lib</tspan>
        </text>
        </g>
        <g transform="translate(130 142)">
        <a xlink:href="font.html" target="_parent">
        <path class="circle" fill="#91BB3E" fill-rule="nonzero" stroke="#91BB3E" stroke-width=".76" d="M150.1323,25.7583 C184.4767,60.1027 184.4767,115.7879 150.1323,150.1323 C115.7879,184.4767 60.1027,184.4767 25.7583,150.1323 C-8.5861,115.7879 -8.5861,60.1027 25.7583,25.7583 C60.1027,-8.5861 115.7879,-8.5861 150.1323,25.7583 Z" transform="matrix(1 0 0 -1 0 175.89)"/>
        <text fill="#FFF" font-size="50" transform="translate(44.895 53.185)">
            <tspan x=".275" y="49">font</tspan>
        </text>
        </g>
        <g transform="translate(471 462)">
        <a xlink:href="segment.html" target="_parent">
        <path class="circle" fill="#7B68F7" fill-rule="nonzero" stroke="#7B68F7" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(17.718 39.168)">
            <tspan x=".429" y="18">segment</tspan>
        </text>
        </g>
        <g transform="translate(569)">
        <a xlink:href="anchor.html" target="_parent">
        <path class="circle" fill="#F77B68" fill-rule="nonzero" stroke="#F77B68" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(24.435 39.074)">
            <tspan x=".468" y="18">anchor</tspan>
        </text>
        </g>
        <g transform="translate(360 441)">
        <a xlink:href="bpoint.html" target="_parent">
        <path class="circle" fill="#AB68F7" fill-rule="nonzero" stroke="#AB68F7" stroke-width=".76" d="M86.4177,14.8257 C106.1853,34.5933 106.1853,66.6425 86.4177,86.4177 C66.6501,106.1853 34.6009,106.1853 14.8257,86.4177 C-4.9419,66.6501 -4.9419,34.6009 14.8257,14.8257 C34.5933,-4.9419 66.6425,-4.9419 86.4177,14.8257 Z" transform="matrix(1 0 0 -1 0 101.243)"/>
        <text fill="#FFF" font-size="18" transform="translate(24.31 38.856)">
            <tspan x=".98" y="18">bPoint</tspan>
        </text>
        </g>
        <g transform="translate(466 142)">
        <a xlink:href="glyph.html" target="_parent">
        <path class="circle" fill="#F7C368" fill-rule="nonzero" stroke="#F7C368" stroke-width=".76" d="M150.1323,25.7583 C184.4767,60.1027 184.4767,115.7879 150.1323,150.1323 C115.7879,184.4767 60.1027,184.4767 25.7583,150.1323 C-8.5861,115.7879 -8.5861,60.1027 25.7583,25.7583 C60.1027,-8.5861 115.7879,-8.5861 150.1323,25.7583 Z" transform="matrix(1 0 0 -1 0 175.89)"/>
        <text fill="#FFF" font-size="50" transform="translate(30.673 53.545)">
            <tspan x=".875" y="49">glyph</tspan>
        </text>
        </g>
    </g>
    </svg>


