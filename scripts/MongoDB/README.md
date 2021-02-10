# MongoDB

## Data Model :
Database : ```BigDataDB```

```json
resume : [
    {
         description: "She is ...",
         job_id: 42
    },
    {
        description: "Donald is ...",
        job_id: 3
    }
]
```

## Requirements :
- **Python3** and librairies :
  - boto3
- MongoDB

## Installation :
Nothing is to be installed

## Configuration :
You can configure :
- file names
- bucket names
- FIFO URL
To do that, modify variable on first lines of this python file : ```script.py```

## Start :
- Make sure MongoDB is started
- Start script : ```python script.py```
