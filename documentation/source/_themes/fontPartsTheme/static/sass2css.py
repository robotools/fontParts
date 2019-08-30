# compile sass into css

import os
import os.path
import subprocess

# sass (CSS extension language) compiler
# http://sass-lang.com/install

# install postCSS and autoprixer with:
## npm install -g postcss-cli-simple
## npm install -g autoprefixer

def compileSass(sassPath):
    '''
    Compile a sass file (and dependencies) into a single css file.

    '''
    cssPath = os.path.splitext(sassPath)[0] + ".css"
    # subprocess.call(["sass", sassPath, cssPath])
    print("Compiling Sass")

    process = subprocess.Popen(["sass", sassPath, cssPath])
    process.wait()

def autoprefixCSS(sassPath):
    '''
    Take CSS file and automatically add browser prefixes with postCSS autoprefixer

    '''
    print("Autoprefixing CSS")
    cssPath = os.path.splitext(sassPath)[0] + ".css"
    command = "postcss --use autoprefixer --autoprefixer.browsers '> 5%' -o" + cssPath + " " + cssPath
    subprocess.call(command, shell=True)

# gets path for directory of sass2css.py
baseFolder = os.path.split(os.path.abspath(__file__))[0]

for f in os.listdir(baseFolder):
    name, extension = os.path.splitext(f)

    # note: be sure that you import files from /partials into the the main.sass file, or code won't make it into CSS
    if extension == ".sass":
        sassPath = os.path.join(baseFolder, f)
        compileSass(sassPath)
        autoprefixCSS(sassPath)
