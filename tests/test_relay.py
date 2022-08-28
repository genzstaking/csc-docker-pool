import pytest
import os
import random
import argparse

from csc_docker_pool.node import *


def test_create_relay_node(capsys):
    path = os.getcwd() + "/tmp/realy-" + str(random.random())
    relay = create_node(path)
    assert relay is not None
    assert is_node(path) is False


def test_create_relay_node_io_config(capsys):
    path = os.getcwd() + "/tmp/realy-" + str(random.random())
    
    relay = create_node(path)
    assert relay is not None
    assert is_node(path) is False
    
    key = "key"
    value = "Value" + str(random.random())
    relay.set(key, value)
    relay.save()
    assert is_node(path) is True
    
    relay2 = create_node(path)
    assert relay2 is not None
    assert relay2.get(key) == value
    
    assert relay2.get(key + str(random.random())) is None
    

def test_load_relay_node(capsys):
    path = os.getcwd() + "/tmp/realy-" + str(random.random())
    relay = create_node(path)
    assert relay is not None
    assert is_node(path) is False
    
    
    relay.load_from_args({"a": 100})
    assert relay.a  is 100
    
    args = argparse.Namespace()
    args.foo = 1
    relay.load_from_args(args)
    assert relay.foo  is 1
