"""Regenerate the three NeuroQuery maps with the published pretrained model."""
import hashlib
import json
from pathlib import Path
import nibabel as nib
from neuroquery import fetch_neuroquery_model, NeuroQueryModel

root=Path(__file__).parent
model_dir=fetch_neuroquery_model(data_dir=str(root/'neuroquery_cache'))
encoder=NeuroQueryModel.from_data_dir(model_dir)
out=root/'neuroquery_maps';out.mkdir(exist_ok=True)
records={}
for term in ['emotion regulation','reward','depression']:
    image=encoder(term)['brain_map']
    path=out/(term.replace(' ','_')+'.nii.gz')
    nib.save(image,str(path))
    records[term]={'query':term,'path':str(path.relative_to(root)),
                   'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                   'shape':image.shape,'affine':image.affine.tolist()}
(root/'results/neuroquery_provenance.json').write_text(json.dumps({
    'pretrained_model_url':'https://osf.io/598tj/download',
    'package_version_used':'neuroquery 1.1.0',
    'model':'neuroquery_model',
    'map_type':'brain_map (model prediction, not Neurosynth association-test z)',
    'maps':records},indent=2),encoding='utf-8')
print('Generated NeuroQuery maps and provenance')
