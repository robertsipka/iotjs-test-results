# Copyright 2017-present Samsung Electronics Co., Ltd. and other contributors
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from API import builder
from API.common import utils, paths
from API.testrunner import testrunner


def load_testing_environment(options):
    '''
    Create a testing environment object that contains the
    module information and the user specified options.
    '''
    resources = utils.read_json_file(paths.RESOURCES_JSON)

    # Get the dependencies of the current device.
    deps = resources['targets'][options.device]
    # Update the deps list with user selected projects.
    deps.append(options.app)

    # Get the required module information.
    modules = {
        name: resources['modules'][name] for name in deps
    }

    # Update the path of the target application.
    if options.app_path:
        modules[options.app]['src'] = options.app_path
    # Add an 'app' named module that is just a reference
    # to the user defined target application.
    modules['app'] = modules[options.app]
    modules['app']['name'] = options.app

    # Create the testing environment object.
    environment = {
        'info': vars(options),
        'modules': modules,
        'paths': resources['paths']
    }

    _resolve_symbols(environment)

    return environment


def _resolve_symbols(env):
    '''
    Resolve all the symbols in the environment object.

    "%%src/test/" -> /home/user/iotjs/test/
    '''
    for key, value in env.iteritems():
        env[key] = _resolve(value, env)


def _resolve(node, env):
    '''
    Recursive function to loop the environment object
    and replace the symbols.
    '''
    if not isinstance(node, dict):
        return node

    for key, value in node.iteritems():
        if isinstance(value, dict):
            node[key] = _resolve(value, env)
        elif isinstance(value, list):
            ret = []
            for obj in value:
                ret.append(_resolve(obj, env))
            node[key] = ret
        elif isinstance(value, str) or isinstance(value, unicode):
            node[key] = _replacer(value, env)

    return node


def _replacer(string, env):
    '''
    Replace symbols with the corresponding string data.
    '''
    if '%' not in string:
        return string

    # These symbols always could be resolved.
    symbol_mapping = {
        '%app': env['info']['app'],
        '%device': env['info']['device'],
        '%build-type': env['info']['buildtype'],
        '%js-remote-test': paths.PROJECT_ROOT,
        '%result-path': paths.RESULT_PATH,
        '%build-path': paths.BUILD_PATH,
        '%patches': paths.PATCHES_PATH,
        '%config': paths.CONFIG_PATH
    }

    for symbol, value in symbol_mapping.items():
        string = string.replace(symbol, value)

    modules = env['modules']
    # Process the remaining symbols that are
    # reference to other modules.
    symbols = re.findall(r'%(.*?)/', string)

    for name in symbols:
        # Skip if the module does not exist.
        if name not in modules:
            continue

        string = string.replace('%' + name, modules[name]['src'])

    return string
