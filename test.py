# Importing any of these would result in coverage issues ❌
import torchvision
# from transformers.models.distilbert import DistilBertModel

from main import foo


def test_foo():
    assert foo() == "bar"
