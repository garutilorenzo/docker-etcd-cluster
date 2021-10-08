#!/usr/bin/env python3

import etcd3

etcd = etcd3.client(host='127.0.0.1', port=2379)

etcd.put('/test/key1', 'hey key1')
etcd.put('/test/key2', 'hey key2')

keys = etcd.get_prefix('/test')

for key in keys:
    print(key[0].decode("utf-8"))