# Native manuscript typography

```latex
\usepackage{graphicx}
\usepackage{needspace}
\usepackage{etoolbox}
\usepackage{listings}
\captionsetup[figure]{font=small,labelfont=bf,justification=raggedright,singlelinecheck=false,skip=5pt}
\AtBeginDocument{\floatplacement{figure}{H}}
\let\EOriginalContents\tableofcontents
\newcommand{\Econtents}{\floatplacement{figure}{tbp}\begingroup\fontsize{9}{10}\selectfont\setlength{\parskip}{0pt}\EOriginalContents\endgroup}
\renewcommand{\tableofcontents}{}
\renewenvironment{quote}{%
  \list{}{\setlength{\leftmargin}{1.6em}\setlength{\rightmargin}{1em}%
    \setlength{\topsep}{4pt}\setlength{\parsep}{0pt}}%
  \item\relax\begin{minipage}{\linewidth}\itshape
}{\end{minipage}\endlist\nopagebreak[4]}
\setcitestyle{authoryear,round,semicolon}
\definecolor{ELink}{HTML}{9C302C}
\hypersetup{colorlinks=true,linkcolor=ELink,citecolor=ELink,urlcolor=ELink}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\clubpenalty=10000
\widowpenalty=10000
\displaywidowpenalty=10000
\setlength{\emergencystretch}{3em}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
```
