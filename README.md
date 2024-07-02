# phonon-tools
Usefull tools to perform phonon calculation by DFT

## Usage

### Postprocess

Run the following commands.

```shell
$ cp preprocess.json postprocess.json
$ sed -i 's/"mode": "preprocess"/"mode": "postprocess"/' postprocess.json
```

Fix `inputs_dir` in `postprocess.json`.
