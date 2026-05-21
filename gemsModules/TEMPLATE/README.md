# Readme for `{{cookiecutter.gems_module}}`

This module produces a skeleton module that follows various conventions and structures in GEMS.

Among some other things, it:

- Creates one or more of each type of file that is expected for normal GEMS modules.
- Populates those with some imports, declarations and such that follow GEMS naming, etc.

You will still need to write your module. It can't do that for you. But, you have a structural outline.

## Usage Overview

If you are new to cookiecutter, please read through this entire document before proceeding. This overview is designed
to help people who already know it but who use it rarely.

You will need to install cookiecutter:

    pip install cookiecutter

Change to the gemsModules directory.

    cd $GEMSHOME/gemsModules

Review the contents of the file `TEMPLATE/cookiecutter.json`:

    cat TEMPLATE/cookiecutter.json

- Each entry between the curly braces is called an 'attribute'.
- If you do not know the meaning of each attribute, see below.

Run cookiecutter on the TEMPLATE:

    cookiecutter TEMPLATE

## Attributes

Cookiecutter will ask you to provide values for the entries in `TEMPLATE/cookiecutter.json`.

At the time of this writing, the file contains this:

```
{{cookiecutter.gems_module}} entity.{
    "gems_module": "newgemsmodule",
    "entity_name": "New_Gems_Module",
    "parent_entity": "",
    "service_name": "SomeService",
    "service_id": "ss",
    "implicit_inputkey": "default",
    "implicit_inputvalue": ""
}
```

If the file you reviewed (in Usage Overview, above) does not match the contents just above, see below.

Descriptions of each attribute:

- `gems_module` : The name of the directory under `$GEMSHOME/gemsModules` that will contain your module.
- `entity_name` : The name your Entity should be called in the JSON API, e.g., Sequence or Glycoprotein.
- `parent_entity` : If this is a submodule, give the parent directory's name. Else, use the `gems_module`.
- `service_name` : The name of a service the entity will offer. Making it up is ok. Example: Build or Analyze.
- `service_id` : The brief name of the subdirectory where output is stored, e.g.: gp, cb, gm, md.
- `implicit_inputkey` : Accept default or see description below.
- `implicit_inputvalue` : Accept default or see description below.

### The implicit attributes:

One feature of GEMS is that it will attempt to determine the desired service based on the inputs. For example,
if the Entity is Sequence, and the `inputs` section contains a `payload` containing a sequence, Sequence will
assume that you want a computed 3D structure for the sequence. This is called an 'implied' or 'implicit' service.

If you want your tests to contain a test for an implied service, include the key and value here.

For example, to generate a test implying a build of DManpa1-OH to the Sequence entity, the answers would be:

- `implicit_inputkey` : payload
- `implicit_inputvalue` : DManpa1-OH

#### Brief notes on implied services

Services can be implied in several ways. This is an important part of the GEMS architecture. For example, assume
someone requests a computed 3D structure for some sequence (like DManpa1-OH). Whether that service itself was
implied or not, GEMS will add the _implied_ service 'Evaluate'. That is, GEMS will always perform an evaluation
if a build is requested. Because (almost) every action in GEMS is a Service, the Evaluation will be put into the
queue of Services right before the requested Build service.

Note that this part of the TEMPLATE only applies to implied Services that can be accessed via the JSON API. It 
does not apply to Services that are automatically run by a GEMS module.

Further information about GEMS architecture is beyond the scope of this document. If in doubt, it is reasonable
to accept the defaults.

If your service will not have any implied Services, accept the defaults. 

### If your `TEMPLATE/cookiecutter.json` file differs from the one above

If this document is out of sync with the current `cookiecutter.json` file, the best way to learn the use the new
attributes is to find where they are used in the TEMPLATE. 

In this situation, the following grep command can be useful. For example, if you need to learn about the `service_id`
attribute, try this:

```
cd $GEMSHOME/gemsModules
grep -rws service_id TEMPLATE
```

Ignoring any entries in this file itself, the output is:

```
TEMPLATE/cookiecutter.json:    "service_id": "ss",
TEMPLATE/{{cookiecutter.gems_module}}/main_api_project.py:        self.project_type = "{{cookiecutter.service_id}}" # This is the same as service_id, and is used in the deprecated code as such
TEMPLATE/{{cookiecutter.gems_module}}/main_api_project.py:        self.service_id = "{{cookiecutter.service_id}}" # This becomes the subdirectory output paths (like cb, gp, ad, gm, pdb, etc)
```

The final two lines contain useful information. The first confirms its presence in the cookiecutter json file.

