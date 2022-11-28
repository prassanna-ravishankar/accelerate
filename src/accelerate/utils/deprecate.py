# Copyright 2022 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import warnings


def deprecate_value(old=None, new=None, version=None, warn=True, deprecate_str=None):
    """
    Will raise a `DeprecationWarning` with a message saying that `old` is deprecated and will be removed in version
    `version`

    Args:
        old (`str`): The old name of the function or class.
        new (`str`): The new name of the function or class.
        version (`str`): The version in which the function or class will be removed.
        warn (`bool`, optional): Whether to raise a warning or not.
        deprecate_str (`str`, optional):
            The message to display in the warning. If not provided, will use the default message.
    """
    if deprecate_str is None:
        deprecate_str = (
            f"{old} is deprecated and will be removed in version {version} of 🤗 Accelerate. Use {new} instead."
        )
    if warn:
        warnings.simplefilter("always", FutureWarning)
        warnings.warn(deprecate_str, category=FutureWarning, stacklevel=2)
        warnings.simplefilter("default", FutureWarning)
    return deprecate_str


class DeprecateAction(argparse.Action):
    """
    Will raise a `DeprecationWarning` with a message saying that `old` is deprecated and will be removed in version
    `version` if an argument is passed that should be deprecated
    """

    def __init__(self, new_argument, new_version, new_value=None, store_true=False, **kwargs):
        self.new_argument = new_argument
        self.new_value = new_value
        if new_value is not None:
            new_argument = f"{new_argument}={new_value}"
        self.deprecate_str = deprecate_value("This argument", f"`{new_argument}`", new_version, warn=False)
        kwargs["help"] = self.deprecate_str
        self.deprecate_str = self.deprecate_str.replace("This argument", f'`{kwargs["option_strings"][0]}`')
        if store_true:
            kwargs["const"] = True
            kwargs["nargs"] = 0
        super().__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        deprecate_value(deprecate_str=self.deprecate_str)
        if self.new_value is not None:
            setattr(namespace, self.new_argument, self.new_value)
        else:
            setattr(namespace, self.new_argument, self.dest)
        delattr(namespace, self.dest)
