#first, define a model
from cqlengine import columns
from cqlengine.models import Model
import uuid

class ExampleModel(Model):
    read_repair_chance = 0.05 # optional - defaults to 0.1
    example_id      = columns.UUID(primary_key=True, default=uuid.uuid4)
    example_type    = columns.Integer(index=True)
    created_at      = columns.DateTime()
    description     = columns.Text(required=False)

#next, setup the connection to your cassandra server(s)...
from cqlengine import connection
connection.setup(['localhost:9160'], 
  username='cassandra', 
  password='cassandra'
)

#...and create your CQL table
from cqlengine.management import sync_table
sync_table(ExampleModel)

#now we can create some rows:
em1 = ExampleModel.create(example_type=0, description="example1", created_at=datetime.now())
em2 = ExampleModel.create(example_type=0, description="example2", created_at=datetime.now())
em3 = ExampleModel.create(example_type=0, description="example3", created_at=datetime.now())
em4 = ExampleModel.create(example_type=0, description="example4", created_at=datetime.now())
em5 = ExampleModel.create(example_type=1, description="example5", created_at=datetime.now())
em6 = ExampleModel.create(example_type=1, description="example6", created_at=datetime.now())
em7 = ExampleModel.create(example_type=1, description="example7", created_at=datetime.now())
em8 = ExampleModel.create(example_type=1, description="example8", created_at=datetime.now())

#and now we can run some queries against our table
ExampleModel.objects.count()
# 8

q = ExampleModel.objects(example_type=1)
q.count()
#4

for instance in q:
    print instance.description
#example5
#example6
#example7
#example8

#here we are applying additional filtering to an existing query
#query objects are immutable, so calling filter returns a new
#query object
q2 = q.filter(example_id=em5.example_id)

q2.count()
#1
for instance in q2:
    print instance.description
#example5
