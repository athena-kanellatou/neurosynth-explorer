"""Interactive companion to the reproducible Neurosynth exploration."""
from pathlib import Path
import csv
import tempfile
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import streamlit as st
from analysis import load_map, compare, validate_grid, MapData

ROOT = Path(__file__).parent
BUNDLED = {
    'emotion regulation': ROOT/'data/emotion_regulation.nii.gz',
    'reward': ROOT/'data/reward.nii.gz',
    'depression': ROOT/'data/depression.nii.gz',
}
st.set_page_config(page_title='Neurosynth Map Explorer', layout='wide')
st.title('🧠 Neurosynth Map Explorer')
st.caption('Exploratory comparison of published term association z maps. No individual or diagnostic inference.')
source = st.radio('Data source', ['Included research maps', 'Upload your own'], horizontal=True)

@st.cache_data(show_spinner=False)
def included(name):
    return load_map(BUNDLED[name], name)

maps = []
if source == 'Included research maps':
    names = st.multiselect('Compare two or three terms', list(BUNDLED),
                           default=['emotion regulation', 'reward'], max_selections=3)
    maps = [included(name) for name in names]
    st.caption('Included files are unthresholded association test maps retrieved 28 September 2026; see results/provenance.json.')
else:
    uploads = st.file_uploader('Upload 2–3 comparable .nii or .nii.gz association z maps',
                               type=['nii','gz'], accept_multiple_files=True)
    if uploads and len(uploads) > 3:
        st.error('Choose at most three maps.'); st.stop()
    for item in uploads or []:
        suffix = '.nii.gz' if item.name.endswith('.nii.gz') else '.nii'
        try:
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder)/('upload'+suffix)
                path.write_bytes(item.getvalue())
                maps.append(load_map(path, item.name))
        except Exception as exc:
            st.error(f'Could not read {item.name}: {exc}'); st.stop()
    st.caption('Record the map type, source release and thresholding before interpreting an uploaded comparison.')

if len(maps) < 2:
    st.info('Select or upload at least two maps.'); st.stop()
try:
    validate_grid(maps)
except ValueError as exc:
    st.error(str(exc)); st.stop()
threshold = st.slider('Positive z threshold', 1.0, 8.0, 3.0, 0.1)
axis = st.selectbox('View plane', ['axial', 'coronal', 'sagittal'])
axis_number = {'sagittal':0, 'coronal':1, 'axial':2}[axis]
slice_number = st.slider(f'{axis.capitalize()} voxel index', 0,
                         maps[0].array.shape[axis_number]-1,
                         maps[0].array.shape[axis_number]//2)
cols = st.columns(len(maps))
for column, item in zip(cols, maps):
    valid = np.isfinite(item.array)
    active = valid & (item.array >= threshold)
    with column:
        fig, ax = plt.subplots(figsize=(5,4))
        plane = lambda data: np.rot90(np.take(data, slice_number, axis=axis_number))
        footprint = np.isfinite(item.array) & (item.array != 0)
        ax.imshow(plane(footprint), cmap='Greys', vmin=-.5, vmax=2)
        overlay = np.ma.masked_where(~plane(active), plane(item.array))
        ax.imshow(overlay, cmap='autumn', vmin=threshold, vmax=max(8,threshold+1))
        ax.set(title=item.name, xticks=[], yticks=[])
        st.pyplot(fig); plt.close(fig)
        st.metric('Voxels ≥ threshold', f'{int(active.sum()):,}')

st.subheader('Pairwise spatial overlap')
for i, a in enumerate(maps):
    for b in maps[i+1:]:
        selected = compare(a, b, [threshold])[0]
        st.write(f"**{a.name} × {b.name}** — shared: {selected['shared_voxels']:,} voxels; "
                 f"Jaccard: {selected['jaccard']:.3f}; Dice: {selected['dice']:.3f}"
                 if selected['jaccard'] is not None else f'**{a.name} × {b.name}** — no supra-threshold voxels')
        st.dataframe(compare(a,b,[2,3,4,5]),hide_index=True)

if source == 'Included research maps':
    st.subheader('Research audit')
    with st.expander('Study-set overlap and atlas findings'):
        with (ROOT/'results/study_overlap.csv').open(encoding='utf-8') as f:
            st.write('Studies assigned to more than one term:')
            st.dataframe(list(csv.DictReader(f)), hide_index=True)
        st.write('Largest emotion regulation × reward overlap components at z ≥ 3 (AAL SPM12):')
        with (ROOT/'results/atlas_labels_z3.csv').open(encoding='utf-8') as f:
            st.dataframe(list(csv.DictReader(f))[:5], hide_index=True)
        st.caption('Atlas labels are template annotations. A peak label does not describe a whole component.')
    with st.expander('Read the interpretation and limitations'):
        st.markdown((ROOT/'results/REPORT.md').read_text(encoding='utf-8'))
    st.download_button('Download overlap table (CSV)',
                       (ROOT/'results/overlap.csv').read_bytes(),
                       file_name='neurosynth_overlap.csv', mime='text/csv')

st.warning('Thresholded map overlap is descriptive. It does not establish statistical significance, anatomical specificity, or clinical relevance.')
