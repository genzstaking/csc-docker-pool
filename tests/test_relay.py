import pytest
import os
import random

from csc_docker_pool.relay import create_relay_node
from csc_docker_pool.relay import is_relay_node


def test_create_relay_node(capsys):
    path = os.getcwd() + "/tmp/realy-" + str(random.random())
    relay = create_relay_node(path)
    assert relay is not None
    assert is_relay_node(path) is False


def test_create_relay_node_io_config(capsys):
    path = os.getcwd() + "/tmp/realy-" + str(random.random())
    
    relay = create_relay_node(path)
    assert relay is not None
    assert is_relay_node(path) is False
    
    key = "key"
    value = "Value" + str(random.random())
    relay.set(key, value)
    relay.save()
    assert is_relay_node(path) is True
    
    relay2 = create_relay_node(path)
    assert relay2 is not None
    assert relay2.get(key) == value
    
    assert relay2.get(key + str(random.random())) is None
