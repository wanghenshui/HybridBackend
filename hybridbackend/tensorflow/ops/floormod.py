# Copyright 2021 Alibaba Group Holding Limited. All Rights Reserved.
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
# =============================================================================

r'''Arithmetic operators for dense and sparse tensors.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.framework import dtypes
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import data_flow_ops
from tensorflow.python.ops import math_ops

from hybridbackend.tensorflow.pywrap import _ops


def floormod_partition(ids, num_partitions):
  r'''Partition IDs using floormod strategy.

   Args:
     ids: Input tensor to partition.
     num_partitions: Number of partitions.

  Return:
    output: Partitioned tensors.
    indices: Indices for stitching back.
  '''
  ids_shards_indices = math_ops.floormod(
    math_ops.cast(ids, dtypes.int32), num_partitions)
  partitioned_ids = data_flow_ops.dynamic_partition(
    ids, ids_shards_indices, num_partitions)
  ids_indices = math_ops.range(array_ops.size(ids))
  partitioned_indices = data_flow_ops.dynamic_partition(
    ids_indices, ids_shards_indices, num_partitions)
  partitioned_ids = tuple(
    array_ops.reshape(v, [-1]) for v in partitioned_ids)
  partitioned_indices = tuple(
    array_ops.reshape(v, [-1]) for v in partitioned_indices)
  return partitioned_ids, partitioned_indices


def floormod_shuffle(ids, num_partitions, name=None):
  r'''Shuffle IDs using floormod strategy.

  Args:
    ids: Input tensor to partition.
    num_partitions: Number of partitions.
    name: Name of the operator.

  Return:
    output: A tensor with shuffled IDs.
    sizes: Size of each shard in output.
    indices: Indices for gathering back.
  '''
  return _ops.floor_mod_shuffle(ids, num_partitions=num_partitions, name=name)


def group_floormod_shuffle(group_ids, num_partitions, name=None):
  r'''Shuffle multiple IDs using floormod strategy.

  Args:
    group_ids: Input tensors to partition.
    num_partitions: Number of partitions.
    name: Name of the operator.

  Return:
    outputs: Tensors with shuffled IDs.
    outputs_sizes: Size of each shard in outputs.
    outputs_indices: Indices for gathering back to group_ids.
  '''
  if not isinstance(group_ids, (tuple, list)):
    raise ValueError('group_ids must be a list')
  group_ids = list(group_ids)
  return _ops.group_floor_mod_shuffle(
    group_ids, num_partitions=num_partitions, name=name)
