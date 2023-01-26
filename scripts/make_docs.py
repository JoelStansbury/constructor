import sys
from os.path import join, dirname
from os.path import dirname, join

import jinja2

from constructor import construct
from constructor.conda_interface import SUPPORTED_PLATFORMS, VALID_PLATFORMS

REPO_ROOT = dirname(dirname(__file__))

sys.path.insert(0, REPO_ROOT)


valid_selectors = construct.ns_platform(sys.platform)
unsupported_platforms = list(set(VALID_PLATFORMS) - set(SUPPORTED_PLATFORMS))

template = """
<!--
DO NOT EDIT THIS FILE MANUALLY
Edit scripts/make_docs.py and/or constructor/construct.py
and regenerate.
-->

# The `construct.yaml` specification

The `construct.yaml` file is the primary mechanism for controlling
the output of the Constructor package. The file contains a list of
key/value pairs in the standard [YAML](https://yaml.org/) format.
Each configuration option is listed in its own subsection below.

Constructor employs the Selector enhancement of the YAML format
first employed in the
[conda-build](https://docs.conda.io/projects/conda-build/en/latest/)
project. Selectors are specially formatted YAML comments that Constructor
uses to customize the specification for different platforms. The precise
syntax for selectors is described in
[this section](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html#preprocessing-selectors)
of the `conda-build` documentation. The list of selectors available
for use in Constructor specs is given in the section
[Available selectors](#available-selectors) below.

Finally, `construct.yaml` is parsed as a `jinja2` template and so any valid
`jinja2` templating directives may be used. The current shell environment
is available as the `jinja2` variable `environ`. As an example, setting the
`version` key from an environment variable called `VERSION` would look like:
`version: {%raw%}{{ environ["VERSION"] }}{%endraw%}`. Note that the special
environment variables available in `meta.yaml` when running `conda-build`
are not available here.

> Note: This content is also available in the CLI as `constructor --help-construct`

## Available keys

{%- for key_info in keys %}
### `{{key_info[0]}}`

_required:_ {{key_info[1]}}<br/>
_type{{key_info[4]}}:_ {{key_info[2]}}<br/>
{{key_info[3]}}
{%- endfor %}

## Available selectors

{%- for key, val in selectors|dictsort %}
- `{{key}}`
{%- endfor %}

## Available Platforms
Specify which platform to build for via the `--platform` argument. If provided, this argument must be formated as `<platform>-<architecture>`
{%- for platform in supported_platforms %}
- `{{platform}}`
{%- endfor %}

The following options are valid but not actively tested.
{%- for platform in unsupported_platforms %}
- `{{platform}}`
{%- endfor %}
""" # noqa

key_info_list = construct.generate_key_info_list()

output = jinja2.Template(template).render(
    selectors=valid_selectors,
    keys=key_info_list,
    supported_platforms=SUPPORTED_PLATFORMS,
    unsupported_platforms=unsupported_platforms,
)

with open(join(REPO_ROOT, 'CONSTRUCT.md'), 'w') as f:
    f.write(output)

with open(join(REPO_ROOT, 'docs', 'source', 'construct-yaml.md'), 'w') as f:
    f.write(output)
