
nbconvert
====

```bash
export DOC_IPYNB=notebooks/hessenberg.ipynb
export TEMPLATE=ghost
export PUB_DATE=2024/10
export MEDIA_PATH="content/images/${PUB_DATE}/${FROM_DOC%.ipynb}"

# html, getting less messy
PYTHONPATH=/home/dnlennon/Workspace/share/jupyter/custom \
jupyter nbconvert $DOC_IPYNB \
  --to html \
  --NbConvertApp.output_files_dir=$MEDIA_PATH \
  --template $TEMPLATE

```


programmatic ghost
====

Leaving this bookmark for the [ghost Admin API](https://ghost.org/docs/admin-api/#posts) here.