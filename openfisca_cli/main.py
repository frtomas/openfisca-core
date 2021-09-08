from invoke import Collection, Program
from . import make
from . import tasks

namespace = Collection()
namespace.add_task(tasks.test)
namespace.add_task(tasks.serve)
namespace.add_collection(Collection.from_module(make))
program = Program(namespace = namespace)
