# Default sub-repository branches when GEMS is built outside the DevEnv.
# DevEnv or caller environment variables (if already set) take precedence.

: "${MD_Utils_BRANCH:=md-test}"
: "${GM_Utils_BRANCH:=gm-test}"
: "${gmml_BRANCH:=gmml-test}"
: "${gmml2_BRANCH:=main}"
