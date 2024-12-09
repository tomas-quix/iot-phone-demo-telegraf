import os
from quixstreams import Application

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(consumer_group="telegraf-norm-v1", auto_offset_reset="earliest")

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)


#sdf = sdf.set_timestamp(lambda row, *_: row["timestamp"])

sdf = sdf.apply(lambda row: {
    **row["fields"],
    "tags": row["tags"],
    "name": row["name"]
})

sdf.print()

sdf.to_topic(output_topic, key=lambda row: row["name"])

if __name__ == "__main__":
    app.run()