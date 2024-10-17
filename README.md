
Setup
====

1. Copy vscode_repl.pth to the local venv.  This contains a link to the jupyter / nbconvert installation. 
2. The .env file sets up GHOST_STACK_PATH, JUPYTER_DATA_DIR, and PYTHONPATH variables
3. In VScode, create a python environment / use existing

### templates

We need to create symbolic links for the ghost template and its dependencies.

```bash
# create symbolic links to ghost and dependencies (e.g., base) termplates in the data directory
function set_templates() {
  source .env
  JUPYTER_PATH=$(PIPENV_PIPFILE=/home/dnlennon/Workspace/share/jupyter/jupyter3/Pipfile pipenv --venv)/share/jupyter

  pushd $(jupyter --data-dir)/nbconvert/templates
  ln -sf ${JUPYTER_PATH}/nbconvert/templates/base
  ln -sf ${GHOST_STACK_PATH}/templates/ghost
  popd
}
set_templates
unset -f set_templates
```

### ghost-data

The expectation is that there is a separate ghost-data directory.  


converting notebooks (command line interface)
====

```bash

# Run this from ./ghost-data.  Note, the relative paths are important.
export NOTEBOOK=hessenberg.ipynb
export MEDIA_PATH="content/images/notebooks/${NOTEBOOK%.ipynb}"

PIPENV_PIPFILE=/home/dnlennon/Workspace/repos/ghost-stack/Pipfile \
pipenv run jupyter nbconvert staging/notebooks/$NOTEBOOK \
  --to ghost \
  --NbConvertApp.output_files_dir=$MEDIA_PATH \
  --OutputMd5Preprocessor.prefix="http://localhost:2368"

```


programmatic ghost
====

```bash
version=v5.96 curl -H "Authorization: Ghost $token" -H "Accept-Version: $version" http://localhost:2368/ghost/api/admin/pages/
```


Leaving this bookmark for the [ghost Admin API](https://ghost.org/docs/admin-api/#posts) here.